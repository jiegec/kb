# CUDA

参考文档：

- [CUDA C Programming Guide](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html)
- [API synchronization behavior](https://docs.nvidia.com/cuda/cuda-runtime-api/api-sync-behavior.html#api-sync-behavior__memcpy-async)
- [Page-Locked Host Memory for Data Transfer](https://leimao.github.io/blog/Page-Locked-Host-Memory-Data-Transfer/)
- [How to Optimize Data Transfers in CUDA C/C++](https://developer.nvidia.com/blog/how-optimize-data-transfers-cuda-cc/)

## CUDA Stream

CUDA Stream 是用来给 CUDA 上的异步任务保序的 API。

### 异步任务

CUDA 上的异步任务包括：

- Kernel Launch
- 同一个 Device 内的 Memcpy（`Memory copies within a single device’s memory`）
- Host to Device 并且小于 64KB 的 Memcpy（`Memory copies from host to device of a memory block of 64 KB or less`）
- 使用 Async 后缀的 CUDA Memcpy 函数（`Memory copies performed by functions that are suffixed with Async`）
- Memset（`Memory set function calls`）

这些任务和 Host 代码是异步的，也就是说，任务还没有完成的时候，函数就返回了，Host 可以继续执行后面的代码。GPU 也支持同时执行不同任务，例如可以同时执行多个 Kernel（`Some devices of compute capability 2.x and higher can execute multiple kernels concurrently.`），在执行 Kernel 的同时进行异步的 Memcpy（`Some devices can perform an asynchronous memory copy to or from the GPU concurrently with kernel execution.`）。

### Memcpy 异步问题

针对 Memcpy 的异步问题，这里需要涉及到一些设计细节：对于 Host to Device Memcpy，由于数据所在的页默认是可换出的（pageable），因此如果要把数据 DMA 到 device，有可能 DMA 到中途，页被操作系统换出，数据被替换成了别的页的内容，此时就会传输错误的数据。因此实际上会先复制一份 src 数组的内容到 staging memory 上，再从 staging memory DMA 到 Device（`the pageable buffer has been copied to the staging memory for DMA transfer to device memory`）。自然，staging memory 会放在 pinned/page-locked（不可换出） 内存上，保证在 DMA 的时候，数据一直在内存中。这个过程可以看 [How to Optimize Data Transfers in CUDA C/C++](https://developer.nvidia.com/blog/how-optimize-data-transfers-cuda-cc/) 的图解。也可以直接在 CUDA 中分配 pinned 内存，这样在 memcpy 的时候就不会多一个拷贝的开销，但是 pinned 内存也不建议开太多，否则在内存吃紧的时候，会发现无页可换。

而 64KB 可能是一个阈值，如果要复制的数据小于 64KB，可能就不走 DMA 的方式，而是直接由 CPU 把数据通过 PCIe 复制到 GPU 上。但是为什么小于 64KB 就是异步，大于 64KB 是“同步”，我并没有想明白。在 [API synchronization behavior](https://docs.nvidia.com/cuda/cuda-runtime-api/api-sync-behavior.html#api-sync-behavior__memcpy-async) 对于 memcpy 的同步/异步性质有另一份表述：

对于“同步”的 Memcpy 来说：

- 从 Pageable Host 内存拷贝到 Device 内存，首先会同步 stream，在把数据复制到 staging memory 后，memcpy 函数就返回，不会等到 DMA 完成（`For transfers from pageable host memory to device memory, a stream sync is performed before the copy is initiated. The function will return once the pageable buffer has been copied to the staging memory for DMA transfer to device memory, but the DMA to final destination may not have completed.`）
- 从 Pinned Host 内存拷贝到 Device 内存，等到拷贝完成才返回（`For transfers from pinned host memory to device memory, the function is synchronous with respect to the host.`）
- 从 Device 内存拷贝到 Host 内存，无论是 Pageable 还是 Pinned，等到拷贝完成才返回（`For transfers from device to either pageable or pinned host memory, the function returns only once the copy has completed.`）
- 从 Device 内存拷贝到 Device 内存是异步的（`For transfers from device memory to device memory, no host-side synchronization is performed.`）
- 从 Host 内存拷贝到 Host 内存，等到拷贝完成才返回（`For transfers from any host memory to any host memory, the function is fully synchronous with respect to the host.`）

对于“异步”的 Memcpy 来说：

- 在 Device 内存和 Pageable Host 内存之间拷贝，即使用了异步 Memcpy，也可能会同步（`For transfers between device memory and pageable host memory, the function might be synchronous with respect to host.`）
- 在 Host 内存和 Host 内存之间拷贝，即使用了异步 Memcpy，也一定会同步（`For transfers from any host memory to any host memory, the function is fully synchronous with respect to the host.`）
- 如果在拷贝的时候，Pageable Memory 的内容必须首先拷贝到 staging memory，那么异步的 Memcpy 可能会同步 stream 并且把数据复制到 staging memory（`If pageable memory must first be staged to pinned memory, the driver may synchronize with the stream and stage the copy into pinned memory.`）
- 其他情况下，异步 Memcpy 是异步的（`For all other transfers, the function should be fully asynchronous.`）

我认为这一份表述应该反映了比较新的 CUDA 的实际设定，只不过为了兼容旧版本/旧设备，也保留了那个奇怪的 64KB 的表述。

### 异步任务间的依赖

但很多时候，异步任务之间是有依赖的，例如 launch kernel 需要用到在它之前的 memcpy 所写入的数据。既希望这两个有依赖的异步任务之间按照顺序执行以保证正确性，又希望和其他没有依赖的异步任务可以同时在 GPU 上执行，这时候就可以用 CUDA stream 来保证部分异步任务的顺序。同一个 CUDA Stream 内的任务保证顺序（`A stream is a sequence of commands (possibly issued by different host threads) that execute in order`），不同 CUDA Stream 的任务不保证顺序（`Different streams, on the other hand, may execute their commands out of order with respect to one another or concurrently`）。

创建 CUDA stream 使用的是 `cudaStreamCreate` 函数。使用异步任务时，通常有一个可选的 stream 参数，可以传入自己创建的 CUDA stream。销毁 CUDA stream 使用的是 `cudaStreamDestroy` 函数。

CUDA stream 在创建的时候会被绑定到创建时的当前 CUDA device（`A host thread can set the device it operates on at any time by calling cudaSetDevice(). Device memory allocations and kernel launches are made on the currently set device; streams and events are created in association with the currently set device.`）。如果 Launch kernel 时指定的 stream 不属于当前 CUDA device，就会失败（`A kernel launch will fail if it is issued to a stream that is not associated to the current device`），而 memcpy 没有这个限制（`A memory copy will succeed even if it is issued to a stream that is not associated to the current device.`）。

如果异步任务在启动时，没有指定 stream（`Kernel launches and host <-> device memory copies that do not specify any stream parameter`），或者指定了 stream 等于 0（`or equivalently that set the stream parameter to zero`），实际上会加入到 default stream 中。默认情况下，default stream 是一个特殊的 NULL stream，每个设备有一个唯一的 NULL stream，它的规则是特殊的（`the default stream is a special stream called the NULL stream and each device has a single NULL stream used for all host threads.`），也就是所谓的 Implicit Synchronization（`The NULL stream is special as it causes implicit synchronization as described in Implicit Synchronization.`）。后面会讨 Explicit Synchronization 和 Implicit Synchronization。

如果编译时传递了 `--default-stream per-thread` 参数，那么 default stream 就是一个普通的 stream，并且每个 Host thread 都有自己的 default stream（`For code that is compiled using the --default-stream per-thread compilation flag (or that defines the CUDA_API_PER_THREAD_DEFAULT_STREAM macro before including CUDA headers (cuda.h and cuda_runtime.h)), the default stream is a regular stream and each host thread has its own default stream.`）。

虽然 stream 之间不保证顺序，但有时候，又希望在 stream 之间建立一个临时的依赖关系。此时可以用 event 来实现：首先用 `cudaEventRecord` 函数，把一个 stream 上的任务记录下来（`Captures in event the contents of stream at the time of this call. event and stream must be on the same CUDA context. Calls such as cudaEventQuery() or cudaStreamWaitEvent() will then examine or wait for completion of the work that was captured`），之后就可以用 `cudaStreamWaitEvent` 函数在另一个 stream 上等待 event 记录下来的任务完成（`cudaStreamWaitEvent() takes a stream and an event as parameters (see Events for a description of events) and makes all the commands added to the given stream after the call to cudaStreamWaitEvent() delay their execution until the given event has completed.`）。

## Implicit/Explicit Synchronization

Stream 保证了任务在 GPU 上执行的顺序，但是它们和 Host 代码依然是异步的。为了让 Host 代码可以等待 GPU 上的任务完成，可以用 `cudaDeviceSynchronize` 等待所有 stream 上的任务完成（`cudaDeviceSynchronize() waits until all preceding commands in all streams of all host threads have completed.`），或者用 `cudaStreamSynchronize` 来等待具体某个 stream 上的任务完成（`cudaStreamSynchronize()takes a stream as a parameter and waits until all preceding commands in the given stream have completed. It can be used to synchronize the host with a specific stream, allowing other streams to continue executing on the device.`）。

此外，还有上面提到过的 `cudaStreamWaitEvent` 函数，它可以用来在多个 stream 之间做同步（`cudaStreamWaitEvent() takes a stream and an event as parameters (see Events for a description of events) and makes all the commands added to the given stream after the call to cudaStreamWaitEvent() delay their execution until the given event has completed.`）。上述同步方法，都需要在 Host 上执行对应的函数，因此是 Explicit Synchronization。

另一种同步方法是 Implicit Synchronization：一些操作会被认为是同步点，在同步点之前的任务不会和同步点之后的任务同时进行（`Two commands from different streams cannot run concurrently if any one of the following operations is issued in-between them by the host thread:`）：

- Host page-locked 内存分配（`a page-locked host memory allocation`）
- Device 内存分配（`a device memory allocation`）
- Device 内存 memset（`a device memory set`）
- 同一个 Device 内存上的 memcpy（`a memory copy between two addresses to the same device memory`）
- 发送到 NULL stream 的 CUDA 命令（`any CUDA command to the NULL stream`）
- 修改 L1 和 Shared memory 大小的配置（`a switch between the L1/shared memory configurations described in Compute Capability 7.x`）

Implicit Synchronization 用在 NULL stream 上，也就是不设置 per-thread 参数时的 default stream，也就是 cudaStreamLegacy。我理解这个是为了照顾旧 CUDA 代码而保留的设定，因为它做了很多同步的保证，导致异步的程度比较低，所以旧的 CUDA 代码可能假设了这些保证，而没有插入显式的同步调用。

根据 [Stream synchronization behavior](https://docs.nvidia.com/cuda/cuda-runtime-api/stream-sync-behavior.html#stream-sync-behavior)，它会生成一个隐式的全局 Barrier：在 NULL(legacy) stream 上提交任务的时候，会首先等待所有的 blocking stream，然后提交自己这个任务，然后所有的 blocking stream 再等待 legacy stream 上的任务（`The legacy default stream is an implicit stream which synchronizes with all other streams in the same CUcontext except for non-blocking streams, described below. (For applications using the runtime APIs only, there will be one context per device.) When an action is taken in the legacy stream such as a kernel launch or cudaStreamWaitEvent(), the legacy stream first waits on all blocking streams, the action is queued in the legacy stream, and then all blocking streams wait on the legacy stream.`）。blocking stream 指的是在 stream 创建时，没有指定 cudaStreamNonBlocking 参数的 stream（`Non-blocking streams which do not synchronize with the legacy stream can be created using the cudaStreamNonBlocking flag with the stream creation APIs.`）。页面上给了一个例子：

```c
k_1<<<1, 1, 0, s>>>();
k_2<<<1, 1>>>();
k_3<<<1, 1, 0, s>>>();
```

`k_2` 在 NULL(legacy) stream 上提交，因此会等待 `k_1` 完成，而其后的 `k_3` 又会等 `k_2` 完成。

可以看到，这其实都是在打补丁：现成代码不能破坏，怎么办？默认用 legacy stream 机制，不得不四处同步，如果程序要想要逃离这个困境，就得创建一个 nonblocking 的 stream。对于新代码，要么打开 per thread 参数，把默认 thread 都换成正常的 stream；要么每次 launch 的时候，都显式指定一个 stream。


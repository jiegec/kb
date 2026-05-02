# ASan 不同选项下的行为

结论：

- 如果可执行文件没有链接 ASan，但是动态库使用了 ASan，为了保证 ASan 运行时能够第一个被加载，通常需要设置 `LD_PRELOAD` 环境变量
- 只要有 ASan 运行时，就能检测内存泄漏和 Double-Free 等只需要 hook malloc/free 等内存管理函数即可检测的错误；但对于越界访问等，只有在编译时打开 ASan，让编译器插桩才能检测
- 即使没有编译或链接 ASan，也可以用 `LD_PRELOAD` 加载 ASan，不过此时只有 ASan 运行时，没有编译器插桩
- 不要加载多个 ASan 运行时（比如一个静态链接、一个动态链接），也不要混合来自不同编译器的 ASan（比如一个来来自 GCC、一个来自 Clang），否则会遇到 `Your application is linked against incompatible ASan runtimes.` 报错

特定编译器行为：

- GCC 默认动态链接 `libasan.so.x`，通常在 `/usr/lib/$arch-linux-gnu` 目录下，通过 `gcc -print-file-name=libasan.so` 命令可以找到；如果想要静态链接，可以传入 `-static-libasan` 链接参数；GCC 不支持 `-shared-libasan` 链接参数
- Clang 默认静态链接 `libclang_rt.asan-$arch.a`，通常在 `/usr/lib/llvm-$ver/lib/clang/$ver/lib/linux` 目录下，通过 `clang -print-file-name=libclang_rt.asan-$arch.a` 命令可以找到；如果想要动态链接，可以传入 `-shared-libasan` 链接参数；Clang 也支持 `-static-libasan` 链接参数
- GCC 默认会在可执行程序和动态库中都动态链接 ASan 运行时库，利用动态链接的特性保证只有一份 ASan 运行时库；Clang 默认不会在动态库中链接 ASan 运行时库，而是在可执行程序中静态链接 ASan 运行时库，这样也保证了只有一份 ASan 运行时库
- Clang 使用 `-shared-libasan` 动态链接 ASan 时，它的运行时库 `libclang_rt.asan-$arch.so` 通常不在默认的动态库搜索路径下，需要添加 `libclang_rt.asan-$arch.so` 所在路径到 `LD_LIBRARY_PATH` 当中；而 GCC 的 ASan 运行时库 `libasan.so.x` 通常就在默认的 `/usr/lib/$arch-linux-gnu` 动态库搜索路径下，因此通常不需要设置 `LD_LIBRARY_PATH` 环境变量

# 华为昇腾 NPU

## CANN 安装

<https://www.hiascend.com/cann/download>

CANN 9.1.0 下载：

```shell
wget https://ascend-cann-open.obs.cn-north-4.myhuaweicloud.com/CANN/CANN%209.1.0/Ascend-cann_9.1.0_linux-x86_64.run
wget https://ascend-repo.obs.cn-east-2.myhuaweicloud.com/CANN/CANN%209.1.0/Ascend-cann-950-ops_9.1.0_linux-x86_64.run
```

在 Docker 里安装：

```dockerfile
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN sed -i \
        's@//archive.ubuntu.com@//mirrors.tuna.tsinghua.edu.cn@g; \
         s@//security.ubuntu.com@//mirrors.tuna.tsinghua.edu.cn@g' \
        /etc/apt/sources.list \
    && apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-dev \
        build-essential gcc g++ make cmake git wget curl \
        libssl-dev zlib1g-dev libffi-dev libgmp-dev \
        numactl libnuma1 kmod unzip tar bc \
        file vim less \
    && rm -rf /var/lib/apt/lists/*

COPY Ascend-cann_9.1.0_linux-x86_64.run /tmp/Ascend-cann_9.1.0_linux-x86_64.run
COPY Ascend-cann-950-ops_9.1.0_linux-x86_64.run /tmp/Ascend-cann-950-ops_9.1.0_linux-x86_64.run

RUN chmod +x /tmp/Ascend-cann_9.1.0_linux-x86_64.run \
    && /tmp/Ascend-cann_9.1.0_linux-x86_64.run --quiet --install \
        --install-for-all

RUN chmod +x /tmp/Ascend-cann-950-ops_9.1.0_linux-x86_64.run \
    && /tmp/Ascend-cann-950-ops_9.1.0_linux-x86_64.run --quiet --install --install-for-all
```

### vector_add 样例

构建并用 cannsim 跑样例：

```shell
source /usr/local/Ascend/cann-9.1.0/set_env.sh
# Setup CANN-Samples
git clone https://gitcode.com/cann/cann-samples
cd cann-samples
cmake -S . -B build -DNPU_ARCH=dav-3510
# Compile vector_add example
cmake --build build --target vector_add
# Run vector_add example in cannsim
cannsim record ./build/Samples/0_Introduction/vector_add/vector_add -s Ascend950 -o ./sim_out
# Generate report
cannsim report -e ./sim_out/npusim_TIMESTAMP_vector_add
```

在 `./sim_out/npusim_TIMESTAMP_vector_add` 目录下得到结果：

- `record/instr.bin`：执行的指令历史，二进制格式，可以用 cannsim 解析，源码在 `/usr/local/Ascend/cann-9.1.0/python/site-packages/cannsim/prof/src/backend/calog_handlers/instr_calog_bin_reader_simple.py`，内部是多个 `<QIIQ200s200s` 结构体，对应的字段是 tick、core、sub、pc、dec、exe；日志样例：`(PC: 0x9000d0d000) SCALAR   : (Binary: 0x02004880) (ID: 000000) MOV_XD_SPR`，猜测是从特殊寄存器（SPR）移动（MOV）数据到通用寄存器（XD）
- `report/results/kernel_0_reports/core_0/trace_core0.json`：Chrome trace 格式，可以看到 NPU 各部分在做什么事情，可以在 `chrome://tracing` 页面里加载

这个样例主要做的事情是，从 GM 拷贝数据到 UB，在 UB 上读取数据，向量求和后，写入 UB，再从 UB 拷贝数据到 GM，类似 CUDA 上，先把数据从 GM 拷贝到 SM，在 SM 上进行向量求和，写入 SM 后，再从 SM 拷贝数据到 GM。不过这里实际上是有多个单元在协作，从 Chrome tracing 来看：

1. 标量单元 AIV0_SCALAR 执行一些未知的初始化指令
2. AIV0_MTE2 执行两个 MOV_SRC_TO_DST_ALIGNv2 指令，从 GM 拷贝两个向量的数据到 UB 上
3. AIV0_RVECLD 执行 RV_VLD 指令，应该是把 UB 的数据读取到寄存器里；AIV0_RVECEX 单元执行 RV_PLT 和 RV_VADD，不确定 PLT 代表啥，VADD 进行的是实际的向量求和；最后 AIV0_RVECST 单元执行 RV_VST 指令把数据从寄存器写到 UB 里
4. 最后 AIV0_MTE3 执行 MOV_SRC_TO_DST_ALIGNv2 指令，从 UB 拷贝输出向量的值到 GM

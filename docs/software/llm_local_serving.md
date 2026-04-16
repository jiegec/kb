# LLM 本地部署

## 环境配置

### 安装 uv

```shell
pipx install uv
set -x PATH ~/.local/bin $PATH
```

### 安装 llama.cpp

```shell
# build latest llama.cpp
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-cli llama-mtmd-cli llama-server llama-gguf-split llama-bench
cp llama.cpp/build/bin/llama-* llama.cpp
```

### 安装 lmstudio

```shell
curl -fsSL https://lmstudio.ai/install.sh | bash
```

### 安装 MLX-LM

```shell
# setup venv in $PWD/.venv
uv venv
uv pip install mlx-lm
```

## 部署模型

### Qwen3.6

llama.cpp:

```shell
# download gguf from hf
# Qwen3.6-35B-A3B
uv run hf download \
    --local-dir unsloth/Qwen3.6-35B-A3B-GGUF \
    unsloth/Qwen3.6-35B-A3B-GGUF \
    Qwen3.6-35B-A3B-UD-Q3_K_XL.gguf
./llama.cpp/llama-server \
    --model unsloth/Qwen3.6-35B-A3B-GGUF/Qwen3.6-35B-A3B-UD-Q3_K_XL.gguf \
    --jinja --ctx-size 262144 \
    --temp 1.0 --top-p 0.95 --top-k 20 --min-p 0.00
```

### Qwen3.5

llama.cpp:

```shell
# follow https://unsloth.ai/docs/models/qwen3.5

# download gguf from hf
# Qwen3.5-27B
uv run hf download \
    --local-dir unsloth/Qwen3.5-27B-GGUF \
    unsloth/Qwen3.5-27B-GGUF \
    Qwen3.5-27B-UD-Q4_K_XL.gguf
./llama.cpp/llama-server \
    --model unsloth/Qwen3.5-27B-GGUF/Qwen3.5-27B-UD-Q4_K_XL.gguf \
    --jinja --ctx-size 262144 \
    --temp 1.0 --top-p 0.95 --top-k 20 --min-p 0.00

# Qwen3.5-35B-A3B
uv run hf download \
    --local-dir unsloth/Qwen3.5-35B-A3B-GGUF \
    unsloth/Qwen3.5-35B-A3B-GGUF \
    Qwen3.5-35B-A3B-UD-Q3_K_XL.gguf
./llama.cpp/llama-server \
    --model unsloth/Qwen3.5-35B-A3B-GGUF/Qwen3.5-35B-A3B-UD-Q3_K_XL.gguf \
    --jinja --ctx-size 262144 \
    --temp 1.0 --top-p 0.95 --top-k 20 --min-p 0.00

# Qwen3.5-9B
uv run hf download \
    --local-dir unsloth/Qwen3.5-9B-GGUF \
    unsloth/Qwen3.5-9B-GGUF \
    Qwen3.5-9B-Q8_0.gguf
uv run hf download \
    --local-dir unsloth/Qwen3.5-9B-GGUF \
    unsloth/Qwen3.5-9B-GGUF \
    Qwen3.5-9B-UD-Q4_K_XL.gguf

# Qwen3.5-4B
uv run hf download \
    --local-dir unsloth/Qwen3.5-4B-GGUF \
    unsloth/Qwen3.5-4B-GGUF \
    Qwen3.5-4B-UD-Q4_K_XL.gguf
```

MLX-LM:

```shell
# Qwen3.5-4B
# for MLX on Apple Silicon
uv run hf download \
    --local-dir mlx-community/Qwen3.5-4B-MLX-4bit \
    mlx-community/Qwen3.5-4B-MLX-4bit 
uv run python3 -m mlx_lm server --model ./mlx-community/Qwen3.5-4B-MLX-4bit --log-level DEBUG
```

SGLang:

```shell
# setup venv in $PWD/.venv
uv venv

# first released in sglang 0.5.9, but 0.5.10 is required
uv pip install -U sglang>=0.5.10 --prerelease=allow
# fix pytorch 2.9.1 & cudnn 9.10 incompat
uv pip install nvidia-cudnn-cu12==9.16.0.29

# Qwen3.5-4B
# some additional args may be required
uv run sglang serve \
  --model Qwen/Qwen3.5-4B \
  --reasoning-parser qwen3 \
  --tool-call-parser qwen3_coder \
  --speculative-algorithm EAGLE \
  --speculative-num-steps 3 \
  --speculative-eagle-topk 1 \
  --speculative-num-draft-tokens 4 \
  --enable-flashinfer-allreduce-fusion \
  --mem-fraction-static 0.8
```

vLLM:

```shell
# setup venv in $PWD/.venv
uv venv

# install latest stable vllm
uv pip install -U vllm --torch-backend=auto
# or nightly vllm
uv pip install -U vllm \
    --torch-backend=auto \
    --extra-index-url https://wheels.vllm.ai/nightly 

# Qwen3.5-4B
# w/o mtp
uv run vllm serve Qwen/Qwen3.5-4B \
  --reasoning-parser qwen3
# w/ mtp
uv run vllm serve Qwen/Qwen3.5-4B \
  --speculative-config '{"method": "mtp", "num_speculative_tokens": 1}' \
  --reasoning-parser qwen3
```

### GLM-4.7-Flash

[zai-org/GLM-4.7-Flash](https://huggingface.co/zai-org/GLM-4.7-Flash)

SGLang:

```shell
# setup venv in $PWD/.venv
uv venv
# if system python too old: uv venv --python 3.10

# https://github.com/sgl-project/sglang/pull/17247
# released in sglang 0.5.8
uv pip install sglang==0.5.8
# https://github.com/huggingface/transformers/pull/43031
# https://github.com/sgl-project/sglang/pull/17381
uv pip install git+https://github.com/huggingface/transformers.git@76732b4e7120808ff989edbd16401f61fa6a0afa

uv run python3 -m sglang.launch_server \
  --model-path zai-org/GLM-4.7-Flash \
  --tp-size 4 \
  --tool-call-parser glm47 \
  --reasoning-parser glm45 \
  --speculative-algorithm EAGLE \
  --speculative-num-steps 3 \
  --speculative-eagle-topk 1 \
  --speculative-num-draft-tokens 4 \
  --mem-fraction-static 0.8 \
  --served-model-name glm-4.7-flash \
  --host 127.0.0.1 \
  --port 8000

# without speculative decoding
uv run python3 -m sglang.launch_server \
  --model-path zai-org/GLM-4.7-Flash \
  --tp-size 4 \
  --tool-call-parser glm47 \
  --reasoning-parser glm45 \
  --mem-fraction-static 0.8 \
  --served-model-name glm-4.7-flash \
  --host 127.0.0.1 \
  --port 8000
```

LM Studio:

```shell
$ ~/.lmstudio/bin/lms get

✔ Select a model to download zai-org/glm-4.7-flash
   ↓ To download: model zai-org/glm-4.7-flash - 14.72 KB
   └─ ↓ To download: GLM 4.7 Flash Q4_K_M [GGUF] - 18.13 GB
$ ~/.lmstudio/bin/lms server start
$ ~/.lmstudio/bin/lms load glm-4.7-flash [--context-length=1-N]
$ ~/.lmstudio/bin/lms ps
$ ~/.lmstudio/bin/lms log stream
```

llama.cpp:

```shell
# follow https://unsloth.ai/docs/models/glm-4.7-flash
# download gguf from hf
uv run hf download \
    --local-dir unsloth/GLM-4.7-Flash-GGUF \
    unsloth/GLM-4.7-Flash-GGUF \
    --include "*UD-Q2_K_XL*"
# serve
./llama.cpp/llama-server \
    --model unsloth/GLM-4.7-Flash-GGUF/GLM-4.7-Flash-UD-Q2_K_XL.gguf \
    --jinja --ctx-size 202752 \
    --temp 0.7 --top-p 1.0 --min-p 0.01 --fit on
./llama.cpp/llama-bench \
    --model unsloth/GLM-4.7-Flash-GGUF/GLM-4.7-Flash-UD-Q2_K_XL.gguf
```

### 常见环境变量

- `HF_HUB_OFFLINE=1`
- `CUDA_VISIBLE_DEVICES`

## 推理性能测试

NVIDIA GeForce RTX 4090:

```shell
# llama-bench
$ llama-bench -p 1024 -n 64 -d 0,16384,32768,65536 --model unsloth/Qwen3.5-9B-GGUF/Qwen3.5-9B-Q8_0.gguf
ggml_cuda_init: found 1 CUDA devices (Total VRAM: 24210 MiB):
  Device 0: NVIDIA GeForce RTX 4090, compute capability 8.9, VMM: yes, VRAM: 24210 MiB
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| qwen35 9B Q8_0                 |   8.86 GiB |     8.95 B | CUDA       |  99 |          pp1024 |      9548.98 ± 24.67 |
| qwen35 9B Q8_0                 |   8.86 GiB |     8.95 B | CUDA       |  99 |            tg64 |         90.95 ± 0.55 |
| qwen35 9B Q8_0                 |   8.86 GiB |     8.95 B | CUDA       |  99 | pp1024 @ d16384 |       5931.42 ± 7.07 |
| qwen35 9B Q8_0                 |   8.86 GiB |     8.95 B | CUDA       |  99 |   tg64 @ d16384 |         85.38 ± 0.61 |
| qwen35 9B Q8_0                 |   8.86 GiB |     8.95 B | CUDA       |  99 | pp1024 @ d32768 |       4335.11 ± 5.79 |
| qwen35 9B Q8_0                 |   8.86 GiB |     8.95 B | CUDA       |  99 |   tg64 @ d32768 |         78.86 ± 0.45 |
| qwen35 9B Q8_0                 |   8.86 GiB |     8.95 B | CUDA       |  99 | pp1024 @ d65536 |       2574.67 ± 0.46 |
| qwen35 9B Q8_0                 |   8.86 GiB |     8.95 B | CUDA       |  99 |   tg64 @ d65536 |         68.48 ± 0.24 |

build: d12cc3d1c (8720)
$ llama-bench -p 1024 -n 64 -d 0,8192,16384,32768 --model unsloth/Qwen3.5-27B-GGUF/Qwen3.5-27B-UD-Q4_K_XL.gguf
ggml_cuda_init: found 1 CUDA devices (Total VRAM: 24210 MiB):
  Device 0: NVIDIA GeForce RTX 4090, compute capability 8.9, VMM: yes, VRAM: 24210 MiB
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| qwen35 27B Q4_K - Medium       |  16.40 GiB |    26.90 B | CUDA       |  99 |          pp1024 |       2848.32 ± 4.20 |
| qwen35 27B Q4_K - Medium       |  16.40 GiB |    26.90 B | CUDA       |  99 |            tg64 |         44.60 ± 0.29 |
| qwen35 27B Q4_K - Medium       |  16.40 GiB |    26.90 B | CUDA       |  99 |  pp1024 @ d8192 |       2358.23 ± 2.44 |
| qwen35 27B Q4_K - Medium       |  16.40 GiB |    26.90 B | CUDA       |  99 |    tg64 @ d8192 |         43.13 ± 0.22 |
| qwen35 27B Q4_K - Medium       |  16.40 GiB |    26.90 B | CUDA       |  99 | pp1024 @ d16384 |       1914.03 ± 1.28 |
| qwen35 27B Q4_K - Medium       |  16.40 GiB |    26.90 B | CUDA       |  99 |   tg64 @ d16384 |         41.15 ± 0.18 |
| qwen35 27B Q4_K - Medium       |  16.40 GiB |    26.90 B | CUDA       |  99 | pp1024 @ d32768 |       1430.67 ± 0.49 |
| qwen35 27B Q4_K - Medium       |  16.40 GiB |    26.90 B | CUDA       |  99 |   tg64 @ d32768 |         37.42 ± 0.16 |

build: d12cc3d1c (8720)
$ llama-bench -p 1024 -n 64 -d 0,8192,16384,32768 --model unsloth/Qwen3.5-35B-A3B-GGUF/Qwen3.5-35B-A3B-UD-Q3_K_XL.gguf
ggml_cuda_init: found 1 CUDA devices (Total VRAM: 24210 MiB):
  Device 0: NVIDIA GeForce RTX 4090, compute capability 8.9, VMM: yes, VRAM: 24210 MiB
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| qwen35moe 35B.A3B Q3_K - Medium |  15.45 GiB |    34.66 B | CUDA       |  99 |          pp1024 |      6432.11 ± 29.38 |
| qwen35moe 35B.A3B Q3_K - Medium |  15.45 GiB |    34.66 B | CUDA       |  99 |            tg64 |        164.36 ± 3.63 |
| qwen35moe 35B.A3B Q3_K - Medium |  15.45 GiB |    34.66 B | CUDA       |  99 |  pp1024 @ d8192 |      5233.23 ± 38.16 |
| qwen35moe 35B.A3B Q3_K - Medium |  15.45 GiB |    34.66 B | CUDA       |  99 |    tg64 @ d8192 |        158.46 ± 4.25 |
| qwen35moe 35B.A3B Q3_K - Medium |  15.45 GiB |    34.66 B | CUDA       |  99 | pp1024 @ d16384 |      4306.44 ± 11.84 |
| qwen35moe 35B.A3B Q3_K - Medium |  15.45 GiB |    34.66 B | CUDA       |  99 |   tg64 @ d16384 |        147.76 ± 2.64 |
| qwen35moe 35B.A3B Q3_K - Medium |  15.45 GiB |    34.66 B | CUDA       |  99 | pp1024 @ d32768 |       3250.25 ± 3.26 |
| qwen35moe 35B.A3B Q3_K - Medium |  15.45 GiB |    34.66 B | CUDA       |  99 |   tg64 @ d32768 |        127.84 ± 1.92 |

build: d12cc3d1c (8720)
$ llama-bench -p 1024 -n 64 -d 0,8192,16384,32768 --model unsloth/Qwen3.5-35B-A3B-GGUF/Qwen3.5-35B-A3B-UD-Q4_K_XL.gguf
ggml_cuda_init: found 1 CUDA devices (Total VRAM: 24210 MiB):
  Device 0: NVIDIA GeForce RTX 4090, compute capability 8.9, VMM: yes, VRAM: 24210 MiB
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| qwen35moe 35B.A3B Q4_K - Medium |  20.70 GiB |    34.66 B | CUDA       |  99 |          pp1024 |      6259.64 ± 28.70 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.70 GiB |    34.66 B | CUDA       |  99 |            tg64 |        158.04 ± 2.80 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.70 GiB |    34.66 B | CUDA       |  99 |  pp1024 @ d8192 |      5101.32 ± 20.83 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.70 GiB |    34.66 B | CUDA       |  99 |    tg64 @ d8192 |        152.96 ± 3.09 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.70 GiB |    34.66 B | CUDA       |  99 | pp1024 @ d16384 |       4191.15 ± 4.66 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.70 GiB |    34.66 B | CUDA       |  99 |   tg64 @ d16384 |        142.27 ± 2.26 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.70 GiB |    34.66 B | CUDA       |  99 | pp1024 @ d32768 |       3186.38 ± 9.74 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.70 GiB |    34.66 B | CUDA       |  99 |   tg64 @ d32768 |        124.07 ± 1.73 |

build: d12cc3d1c (8720)
# llama-server + llama-benchy
# llama-server version: 8720 (d12cc3d1c)
$ llama-server \
  --model unsloth/Qwen3.5-35B-A3B-GGUF/Qwen3.5-35B-A3B-UD-Q3_K_XL.gguf \
  --jinja --ctx-size 262144 \
  --temp 1.0 --top-p 0.95 --top-k 20 --min-p 0.00
$ uvx llama-benchy@v0.3.5 --base-url http://127.0.0.1:8080 --no-cache --model Qwen/Qwen3.5-35B-A3B --depth 0 8192 16384 32768 --runs 5
| model                |            test |              t/s |      peak t/s |        ttfr (ms) |     est_ppt (ms) |    e2e_ttft (ms) |
|:---------------------|----------------:|-----------------:|--------------:|-----------------:|-----------------:|-----------------:|
| Qwen/Qwen3.5-35B-A3B |          pp2048 | 3786.98 ± 207.45 |               |   544.36 ± 27.51 |   542.62 ± 27.51 |   544.48 ± 27.50 |
| Qwen/Qwen3.5-35B-A3B |            tg32 |    149.19 ± 2.89 | 154.77 ± 2.95 |                  |                  |                  |
| Qwen/Qwen3.5-35B-A3B |  pp2048 @ d8192 | 5144.76 ± 167.18 |               |  1994.39 ± 61.87 |  1992.66 ± 61.87 |  1994.51 ± 61.87 |
| Qwen/Qwen3.5-35B-A3B |    tg32 @ d8192 |    141.84 ± 1.94 | 147.45 ± 1.85 |                  |                  |                  |
| Qwen/Qwen3.5-35B-A3B | pp2048 @ d16384 |  5327.42 ± 65.03 |               |  3462.31 ± 42.22 |  3460.58 ± 42.22 |  3462.43 ± 42.22 |
| Qwen/Qwen3.5-35B-A3B |   tg32 @ d16384 |    139.06 ± 0.73 | 144.58 ± 0.68 |                  |                  |                  |
| Qwen/Qwen3.5-35B-A3B | pp2048 @ d32768 | 5229.41 ± 105.39 |               | 6662.22 ± 130.77 | 6660.49 ± 130.77 | 6662.34 ± 130.77 |
| Qwen/Qwen3.5-35B-A3B |   tg32 @ d32768 |    131.29 ± 0.85 | 136.84 ± 0.64 |                  |                  |                  |
$ llama-server \
  --model unsloth/Qwen3.5-4B-GGUF/Qwen3.5-4B-Q8_0.gguf \
  --jinja --ctx-size 262144 \
  --temp 1.0 --top-p 0.95 --top-k 20 --min-p 0.00
$ uvx llama-benchy@v0.3.5 --base-url http://127.0.0.1:8080 --no-cache --model Qwen/Qwen3.5-4B --depth 0 8192 16384 32768 --runs 5
| model           |            test |              t/s |      peak t/s |        ttfr (ms) |     est_ppt (ms) |    e2e_ttft (ms) |
|:----------------|----------------:|-----------------:|--------------:|-----------------:|-----------------:|-----------------:|
| Qwen/Qwen3.5-4B |          pp2048 | 5759.84 ± 496.22 |               |   359.57 ± 27.56 |   358.11 ± 27.56 |   359.70 ± 27.53 |
| Qwen/Qwen3.5-4B |            tg32 |    134.83 ± 1.00 | 139.57 ± 1.01 |                  |                  |                  |
| Qwen/Qwen3.5-4B |  pp2048 @ d8192 | 8933.77 ± 543.64 |               |  1151.89 ± 67.29 |  1150.44 ± 67.29 |  1152.01 ± 67.28 |
| Qwen/Qwen3.5-4B |    tg32 @ d8192 |    129.25 ± 0.29 | 133.94 ± 0.28 |                  |                  |                  |
| Qwen/Qwen3.5-4B | pp2048 @ d16384 | 8760.80 ± 365.59 |               |  2109.05 ± 83.15 |  2107.59 ± 83.15 |  2109.18 ± 83.16 |
| Qwen/Qwen3.5-4B |   tg32 @ d16384 |    123.38 ± 0.84 | 128.23 ± 0.70 |                  |                  |                  |
| Qwen/Qwen3.5-4B | pp2048 @ d32768 | 8379.69 ± 413.69 |               | 4165.87 ± 191.72 | 4164.41 ± 191.72 | 4165.99 ± 191.70 |
| Qwen/Qwen3.5-4B |   tg32 @ d32768 |    114.95 ± 0.58 | 119.65 ± 0.45 |                  |                  |                  |

# sglang 0.5.10
# w/o mtp
$ uv run sglang serve \
  --model-path Qwen/Qwen3.5-4B \
  --reasoning-parser qwen3 \
  --tool-call-parser qwen3_coder \
  --enable-flashinfer-allreduce-fusion \
  --mem-fraction-static 0.8
$ uvx llama-benchy@v0.3.5 --base-url http://127.0.0.1:30000/v1 --no-cache --model Qwen/Qwen3.5-4B --depth 0 8192 16384 32768 --runs 5
| model           |            test |               t/s |     peak t/s |       ttfr (ms) |    est_ppt (ms) |   e2e_ttft (ms) |
|:----------------|----------------:|------------------:|-------------:|----------------:|----------------:|----------------:|
| Qwen/Qwen3.5-4B |          pp2048 | 9296.18 ± 2671.79 |              | 261.84 ± 130.02 | 257.83 ± 130.02 | 261.95 ± 130.03 |
| Qwen/Qwen3.5-4B |            tg32 |      92.16 ± 0.14 | 95.22 ± 0.14 |                 |                 |                 |
| Qwen/Qwen3.5-4B |  pp2048 @ d8192 | 13406.82 ± 299.83 |              |  768.24 ± 16.66 |  764.24 ± 16.66 |  768.36 ± 16.64 |
| Qwen/Qwen3.5-4B |    tg32 @ d8192 |      90.15 ± 0.05 | 93.12 ± 0.05 |                 |                 |                 |
| Qwen/Qwen3.5-4B | pp2048 @ d16384 | 13279.58 ± 102.18 |              | 1392.14 ± 10.63 | 1388.14 ± 10.63 | 1392.26 ± 10.63 |
| Qwen/Qwen3.5-4B |   tg32 @ d16384 |      87.97 ± 0.10 | 90.88 ± 0.11 |                 |                 |                 |
| Qwen/Qwen3.5-4B | pp2048 @ d32768 |  12285.20 ± 24.03 |              |  2838.07 ± 5.55 |  2834.07 ± 5.55 |  2838.20 ± 5.55 |
| Qwen/Qwen3.5-4B |   tg32 @ d32768 |      83.11 ± 0.07 | 85.85 ± 0.07 |                 |                 |                 |
# w/ mtp
# Add --mamba-scheduler-strategy extra_buffer and set SGLANG_ENABLE_SPEC_V2=1 to fix error: 
# ValueError: Speculative decoding for Qwen3_5ForConditionalGeneration is not compatible with radix cache when using --mamba-scheduler-strategy no_buffer. To use radix cache with speculative decoding, please use --mamba-scheduler-strategy extra_buffer and set SGLANG_ENABLE_SPEC_V2=1.
$ SGLANG_ENABLE_SPEC_V2=1 uv run sglang serve \
  --model-path Qwen/Qwen3.5-4B \
  --reasoning-parser qwen3 \
  --tool-call-parser qwen3_coder \
  --speculative-algorithm EAGLE \
  --speculative-num-steps 3 \
  --speculative-eagle-topk 1 \
  --speculative-num-draft-tokens 4 \
  --enable-flashinfer-allreduce-fusion \
  --mem-fraction-static 0.95 \
  --mamba-scheduler-strategy extra_buffer
$ uvx llama-benchy@v0.3.5 --base-url http://127.0.0.1:30000/v1 --no-cache --model Qwen/Qwen3.5-4B --depth 0 8192 16384 32768 --runs 5
| model           |            test |               t/s |     peak t/s |       ttfr (ms) |    est_ppt (ms) |   e2e_ttft (ms) |
|:----------------|----------------:|------------------:|-------------:|----------------:|----------------:|----------------:|
| Qwen/Qwen3.5-4B |          pp2048 | 7835.05 ± 2950.85 |              | 374.17 ± 295.34 | 370.40 ± 295.34 | 374.29 ± 295.36 |
| Qwen/Qwen3.5-4B |            tg32 |      53.04 ± 0.09 | 58.26 ± 0.36 |                 |                 |                 |
| Qwen/Qwen3.5-4B |  pp2048 @ d8192 | 11527.59 ± 271.35 |              |  892.61 ± 20.69 |  888.84 ± 20.69 |  892.74 ± 20.69 |
| Qwen/Qwen3.5-4B |    tg32 @ d8192 |      51.45 ± 0.75 | 56.62 ± 0.95 |                 |                 |                 |
| Qwen/Qwen3.5-4B | pp2048 @ d16384 |  11610.54 ± 13.01 |              |  1591.40 ± 1.80 |  1587.63 ± 1.80 |  1591.52 ± 1.82 |
| Qwen/Qwen3.5-4B |   tg32 @ d16384 |      50.78 ± 0.14 | 56.39 ± 0.12 |                 |                 |                 |
| Qwen/Qwen3.5-4B | pp2048 @ d32768 |  10953.04 ± 47.04 |              | 3182.57 ± 13.66 | 3178.79 ± 13.66 | 3182.68 ± 13.66 |
| Qwen/Qwen3.5-4B |   tg32 @ d32768 |      48.48 ± 0.06 | 53.67 ± 0.51 |                 |                 |                 |


# vllm 0.19.0
# w/o mtp
$ uv run vllm serve Qwen/Qwen3.5-4B \
  --reasoning-parser qwen3
$ uvx llama-benchy@v0.3.5 --base-url http://127.0.0.1:8000/v1 --no-cache --model Qwen/Qwen3.5-4B --depth 0 8192 16384 32768 --runs 5
| model           |            test |               t/s |      peak t/s |       ttfr (ms) |    est_ppt (ms) |   e2e_ttft (ms) |
|:----------------|----------------:|------------------:|--------------:|----------------:|----------------:|----------------:|
| Qwen/Qwen3.5-4B |          pp2048 | 9718.83 ± 3620.94 |               | 301.31 ± 237.11 | 297.99 ± 237.11 | 301.41 ± 237.13 |
| Qwen/Qwen3.5-4B |            tg32 |      99.01 ± 0.30 | 102.26 ± 0.31 |                 |                 |                 |
| Qwen/Qwen3.5-4B |  pp2048 @ d8192 | 13664.97 ± 231.99 |               |  752.98 ± 12.83 |  749.67 ± 12.83 |  753.09 ± 12.83 |
| Qwen/Qwen3.5-4B |    tg32 @ d8192 |     100.95 ± 0.33 | 104.28 ± 0.34 |                 |                 |                 |
| Qwen/Qwen3.5-4B | pp2048 @ d16384 |  13727.61 ± 86.88 |               |  1346.09 ± 8.50 |  1342.78 ± 8.50 |  1346.21 ± 8.49 |
| Qwen/Qwen3.5-4B |   tg32 @ d16384 |      99.42 ± 0.72 | 102.83 ± 0.79 |                 |                 |                 |
| Qwen/Qwen3.5-4B | pp2048 @ d32768 |  12749.47 ± 43.07 |               |  2734.23 ± 9.21 |  2730.92 ± 9.21 |  2734.35 ± 9.20 |
| Qwen/Qwen3.5-4B |   tg32 @ d32768 |      93.94 ± 0.90 |  97.36 ± 0.93 |                 |                 |                 |
# w/ mtp
$ uv run vllm serve Qwen/Qwen3.5-4B \
  --speculative-config '{"method": "mtp", "num_speculative_tokens": 1}' \
  --reasoning-parser qwen3
$ uvx llama-benchy@v0.3.5 --base-url http://127.0.0.1:8000/v1 --no-cache --model Qwen/Qwen3.5-4B --depth 0 8192 16384 32768 --runs 5
| model           |            test |               t/s |     peak t/s |       ttfr (ms) |    est_ppt (ms) |   e2e_ttft (ms) |
|:----------------|----------------:|------------------:|-------------:|----------------:|----------------:|----------------:|
| Qwen/Qwen3.5-4B |          pp2048 | 8959.31 ± 4289.51 |              | 387.48 ± 355.22 | 384.49 ± 355.22 | 387.58 ± 355.21 |
| Qwen/Qwen3.5-4B |            tg32 |      67.79 ± 0.10 | 71.78 ± 0.17 |                 |                 |                 |
| Qwen/Qwen3.5-4B |  pp2048 @ d8192 | 13527.91 ± 192.59 |              |  760.18 ± 11.01 |  757.18 ± 11.01 |  760.27 ± 11.03 |
| Qwen/Qwen3.5-4B |    tg32 @ d8192 |      54.43 ± 1.32 | 57.75 ± 1.51 |                 |                 |                 |
| Qwen/Qwen3.5-4B | pp2048 @ d16384 | 13351.83 ± 129.89 |              | 1383.68 ± 13.44 | 1380.69 ± 13.44 | 1383.88 ± 13.47 |
| Qwen/Qwen3.5-4B |   tg32 @ d16384 |      45.05 ± 1.16 | 47.70 ± 1.62 |                 |                 |                 |
| Qwen/Qwen3.5-4B | pp2048 @ d32768 |  12225.52 ± 60.48 |              | 2850.96 ± 14.10 | 2847.97 ± 14.10 | 2851.06 ± 14.11 |
| Qwen/Qwen3.5-4B |   tg32 @ d32768 |      34.23 ± 0.09 | 36.31 ± 0.11 |                 |                 |                 |
```

结论：Qwen3.5-35B-A3B 的推理速度相较于 Qwen3.5 稠密模型（27B/9B）显著更快；在长上下文推理性能方面，Qwen3.5 相较于 GLM-4.7-Flash 优势明显，具体表现为前者性能随上下文长度增加衰减很少，后者则衰减显著。这大概是因为 Qwen3.5 引入了线性注意力机制。随着 llama.cpp 版本的更新，推理性能也在逐渐提升，因此安装最新版是很有必要的。

Apple M4:

```shell
$ llama-bench -p 1024 -n 64 --model unsloth/Qwen3.5-9B-GGUF/Qwen3.5-9B-UD-Q4_K_XL.gguf
| model                          |       size |     params | backend    | threads |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | ------: | --------------: | -------------------: |
| qwen35 9B Q4_K - Medium        |   5.55 GiB |     8.95 B | MTL,BLAS   |       4 |          pp1024 |        175.35 ± 6.61 |
| qwen35 9B Q4_K - Medium        |   5.55 GiB |     8.95 B | MTL,BLAS   |       4 |            tg64 |         14.83 ± 0.70 |

build: 054d8b0f2 (8396)
$ llama-bench -p 1024 -n 64 --model unsloth/Qwen3.5-4B-GGUF/Qwen3.5-4B-UD-Q4_K_XL.gguf
| model                          |       size |     params | backend    | threads |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | ------: | --------------: | -------------------: |
| qwen35 4B Q4_K - Medium        |   2.70 GiB |     4.21 B | MTL,BLAS   |       4 |          pp1024 |        323.95 ± 7.13 |
| qwen35 4B Q4_K - Medium        |   2.70 GiB |     4.21 B | MTL,BLAS   |       4 |            tg64 |         24.44 ± 0.28 |

build: 054d8b0f2 (8396)
# mlx-lm 0.31.1
$ uv run python3 -m mlx_lm.benchmark --model ./mlx-community/Qwen3.5-4B-MLX-4bit -p 1024 -g 64
Running warmup..
Timing with prompt_tokens=1024, generation_tokens=64, batch_size=1.
Trial 1:  prompt_tps=361.322, generation_tps=39.657, peak_memory=3.502
Trial 2:  prompt_tps=358.414, generation_tps=38.724, peak_memory=3.503
Trial 3:  prompt_tps=356.888, generation_tps=39.224, peak_memory=3.503
Trial 4:  prompt_tps=359.941, generation_tps=38.759, peak_memory=3.504
Trial 5:  prompt_tps=359.376, generation_tps=38.754, peak_memory=3.504
Averages: prompt_tps=359.188, generation_tps=39.023, peak_memory=3.503
```

## 模型能力测试

### MMLU-Pro

```shell
git clone https://github.com/TIGER-AI-Lab/MMLU-Pro
cd MMLU-Pro
uv venv
uv pip install openai datasets anthropic google.generativeai ai21
uv run python3 evaluate_from_apiX.py --url http://127.0.0.1:8080 -m MODEL_NAME_HERE -o results --num_workers NUM_WORKERS
```

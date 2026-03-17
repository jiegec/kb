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

### Qwen3.5 series

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

# released in sglang 0.5.9, but latest main branch is required
uv pip install 'git+https://github.com/sgl-project/sglang.git#subdirectory=python'
# fix pytorch 2.9.1 & cudnn 9.10 incompat
uv pip install nvidia-cudnn-cu12==9.16.0.29

# Qwen3.5-4B
# some additional args may be required
uv run python -m sglang.launch_server \
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

# install latest vllm
uv pip install -U vllm --torch-backend=auto

# Qwen3.5-4B
uv run vllm serve Qwen/Qwen3.5-4B \
  --speculative-config '{"method": "mtp", "num_speculative_tokens": 1}' \
  --reasoning-parser qwen3
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
| qwen35 9B Q8_0                 |   8.86 GiB |     8.95 B | CUDA       |  99 |          pp1024 |       9512.79 ± 7.42 |
| qwen35 9B Q8_0                 |   8.86 GiB |     8.95 B | CUDA       |  99 |            tg64 |         84.54 ± 0.56 |
| qwen35 9B Q8_0                 |   8.86 GiB |     8.95 B | CUDA       |  99 | pp1024 @ d16384 |       5972.57 ± 7.84 |
| qwen35 9B Q8_0                 |   8.86 GiB |     8.95 B | CUDA       |  99 |   tg64 @ d16384 |         79.93 ± 0.45 |
| qwen35 9B Q8_0                 |   8.86 GiB |     8.95 B | CUDA       |  99 | pp1024 @ d32768 |       4336.19 ± 3.40 |
| qwen35 9B Q8_0                 |   8.86 GiB |     8.95 B | CUDA       |  99 |   tg64 @ d32768 |         74.09 ± 0.30 |
| qwen35 9B Q8_0                 |   8.86 GiB |     8.95 B | CUDA       |  99 | pp1024 @ d65536 |       2572.80 ± 0.83 |
| qwen35 9B Q8_0                 |   8.86 GiB |     8.95 B | CUDA       |  99 |   tg64 @ d65536 |         64.83 ± 0.19 |

build: 054d8b0f2 (8396)
$ llama-bench -p 1024 -n 64 -d 0,8192,16384,32768 --model unsloth/Qwen3.5-27B-GGUF/Qwen3.5-27B-UD-Q4_K_XL.gguf
ggml_cuda_init: found 1 CUDA devices (Total VRAM: 24210 MiB):
  Device 0: NVIDIA GeForce RTX 4090, compute capability 8.9, VMM: yes, VRAM: 24210 MiB
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| qwen35 27B Q4_K - Medium       |  16.40 GiB |    26.90 B | CUDA       |  99 |          pp1024 |       2881.33 ± 3.62 |
| qwen35 27B Q4_K - Medium       |  16.40 GiB |    26.90 B | CUDA       |  99 |            tg64 |         41.48 ± 0.24 |
| qwen35 27B Q4_K - Medium       |  16.40 GiB |    26.90 B | CUDA       |  99 |  pp1024 @ d8192 |       2368.01 ± 0.86 |
| qwen35 27B Q4_K - Medium       |  16.40 GiB |    26.90 B | CUDA       |  99 |    tg64 @ d8192 |         40.26 ± 0.20 |
| qwen35 27B Q4_K - Medium       |  16.40 GiB |    26.90 B | CUDA       |  99 | pp1024 @ d16384 |       1915.24 ± 0.76 |
| qwen35 27B Q4_K - Medium       |  16.40 GiB |    26.90 B | CUDA       |  99 |   tg64 @ d16384 |         38.52 ± 0.17 |
| qwen35 27B Q4_K - Medium       |  16.40 GiB |    26.90 B | CUDA       |  99 | pp1024 @ d32768 |       1427.17 ± 0.45 |
| qwen35 27B Q4_K - Medium       |  16.40 GiB |    26.90 B | CUDA       |  99 |   tg64 @ d32768 |         35.23 ± 0.13 |

build: 054d8b0f2 (8396)
$ llama-bench -p 1024 -n 64 -d 0,8192,16384,32768 --model unsloth/Qwen3.5-35B-A3B-GGUF/Qwen3.5-35B-A3B-UD-Q3_K_XL.gguf
ggml_cuda_init: found 1 CUDA devices (Total VRAM: 24210 MiB):
  Device 0: NVIDIA GeForce RTX 4090, compute capability 8.9, VMM: yes, VRAM: 24210 MiB
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| qwen35moe 35B.A3B Q3_K - Medium |  15.45 GiB |    34.66 B | CUDA       |  99 |          pp1024 |      6516.41 ± 25.12 |
| qwen35moe 35B.A3B Q3_K - Medium |  15.45 GiB |    34.66 B | CUDA       |  99 |            tg64 |        127.68 ± 1.68 |
| qwen35moe 35B.A3B Q3_K - Medium |  15.45 GiB |    34.66 B | CUDA       |  99 |  pp1024 @ d8192 |      5312.38 ± 15.21 |
| qwen35moe 35B.A3B Q3_K - Medium |  15.45 GiB |    34.66 B | CUDA       |  99 |    tg64 @ d8192 |        124.12 ± 2.31 |
| qwen35moe 35B.A3B Q3_K - Medium |  15.45 GiB |    34.66 B | CUDA       |  99 | pp1024 @ d16384 |      4333.28 ± 10.15 |
| qwen35moe 35B.A3B Q3_K - Medium |  15.45 GiB |    34.66 B | CUDA       |  99 |   tg64 @ d16384 |        117.30 ± 1.65 |
| qwen35moe 35B.A3B Q3_K - Medium |  15.45 GiB |    34.66 B | CUDA       |  99 | pp1024 @ d32768 |       3259.58 ± 4.79 |
| qwen35moe 35B.A3B Q3_K - Medium |  15.45 GiB |    34.66 B | CUDA       |  99 |   tg64 @ d32768 |        104.57 ± 1.18 |

build: 054d8b0f2 (8396)
$ llama-bench -p 1024 -n 64 -d 0,8192,16384,32768 --model unsloth/Qwen3.5-35B-A3B-GGUF/Qwen3.5-35B-A3B-UD-Q4_K_XL.gguf
ggml_cuda_init: found 1 CUDA devices (Total VRAM: 24210 MiB):
  Device 0: NVIDIA GeForce RTX 4090, compute capability 8.9, VMM: yes, VRAM: 24210 MiB
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| qwen35moe 35B.A3B Q4_K - Medium |  20.70 GiB |    34.66 B | CUDA       |  99 |          pp1024 |      6301.67 ± 33.26 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.70 GiB |    34.66 B | CUDA       |  99 |            tg64 |        124.46 ± 1.71 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.70 GiB |    34.66 B | CUDA       |  99 |  pp1024 @ d8192 |      5151.44 ± 20.77 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.70 GiB |    34.66 B | CUDA       |  99 |    tg64 @ d8192 |        121.40 ± 2.08 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.70 GiB |    34.66 B | CUDA       |  99 | pp1024 @ d16384 |       4233.41 ± 7.04 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.70 GiB |    34.66 B | CUDA       |  99 |   tg64 @ d16384 |        114.44 ± 1.37 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.70 GiB |    34.66 B | CUDA       |  99 | pp1024 @ d32768 |       3205.90 ± 3.72 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.70 GiB |    34.66 B | CUDA       |  99 |   tg64 @ d32768 |        102.51 ± 1.00 |

build: 054d8b0f2 (8396)
$ llama-bench -p 1024 -n 64 -d 0,8192,16384,32768 --model unsloth/Qwen3.5-35B-A3B-GGUF/Qwen3.5-35B-A3B-MXFP4_MOE.gguf
ggml_cuda_init: found 1 CUDA devices (Total VRAM: 24210 MiB):
  Device 0: NVIDIA GeForce RTX 4090, compute capability 8.9, VMM: yes, VRAM: 24210 MiB
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| qwen35moe 35B.A3B Q4_K - Medium |  20.09 GiB |    34.66 B | CUDA       |  99 |          pp1024 |      6402.00 ± 21.78 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.09 GiB |    34.66 B | CUDA       |  99 |            tg64 |        125.07 ± 1.60 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.09 GiB |    34.66 B | CUDA       |  99 |  pp1024 @ d8192 |      5223.69 ± 18.55 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.09 GiB |    34.66 B | CUDA       |  99 |    tg64 @ d8192 |        121.94 ± 1.83 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.09 GiB |    34.66 B | CUDA       |  99 | pp1024 @ d16384 |       4278.25 ± 7.21 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.09 GiB |    34.66 B | CUDA       |  99 |   tg64 @ d16384 |        115.12 ± 1.31 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.09 GiB |    34.66 B | CUDA       |  99 | pp1024 @ d32768 |       3224.29 ± 4.00 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.09 GiB |    34.66 B | CUDA       |  99 |   tg64 @ d32768 |        102.84 ± 1.04 |

build: 054d8b0f2 (8396)
$ llama-bench -p 1024 -n 64 -d 0,8192,16384,32768 --model unsloth/GLM-4.7-Flash-GGUF/GLM-4.7-Flash-UD-Q2_K_XL.gguf
ggml_cuda_init: found 1 CUDA devices (Total VRAM: 24210 MiB):
  Device 0: NVIDIA GeForce RTX 4090, compute capability 8.9, VMM: yes, VRAM: 24210 MiB
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| deepseek2 30B.A3B Q2_K - Medium |  11.06 GiB |    29.94 B | CUDA       |  99 |          pp1024 |       5193.94 ± 9.98 |
| deepseek2 30B.A3B Q2_K - Medium |  11.06 GiB |    29.94 B | CUDA       |  99 |            tg64 |        137.03 ± 2.11 |
| deepseek2 30B.A3B Q2_K - Medium |  11.06 GiB |    29.94 B | CUDA       |  99 |  pp1024 @ d8192 |       2351.72 ± 3.68 |
| deepseek2 30B.A3B Q2_K - Medium |  11.06 GiB |    29.94 B | CUDA       |  99 |    tg64 @ d8192 |         56.57 ± 0.33 |
| deepseek2 30B.A3B Q2_K - Medium |  11.06 GiB |    29.94 B | CUDA       |  99 | pp1024 @ d16384 |       1401.88 ± 0.53 |
| deepseek2 30B.A3B Q2_K - Medium |  11.06 GiB |    29.94 B | CUDA       |  99 |   tg64 @ d16384 |         35.03 ± 0.14 |
| deepseek2 30B.A3B Q2_K - Medium |  11.06 GiB |    29.94 B | CUDA       |  99 | pp1024 @ d32768 |        807.66 ± 0.56 |
| deepseek2 30B.A3B Q2_K - Medium |  11.06 GiB |    29.94 B | CUDA       |  99 |   tg64 @ d32768 |         19.10 ± 0.04 |

build: 054d8b0f2 (8396)
$ llama-bench -p 1024 -n 64 -d 0,8192,16384,32768 --model unsloth/GLM-4.7-Flash-GGUF/GLM-4.7-Flash-UD-Q4_K_XL.gguf
ggml_cuda_init: found 1 CUDA devices (Total VRAM: 24210 MiB):
  Device 0: NVIDIA GeForce RTX 4090, compute capability 8.9, VMM: yes, VRAM: 24210 MiB
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| deepseek2 30B.A3B Q4_K - Medium |  16.31 GiB |    29.94 B | CUDA       |  99 |          pp1024 |      5971.68 ± 14.20 |
| deepseek2 30B.A3B Q4_K - Medium |  16.31 GiB |    29.94 B | CUDA       |  99 |            tg64 |        132.27 ± 1.95 |
| deepseek2 30B.A3B Q4_K - Medium |  16.31 GiB |    29.94 B | CUDA       |  99 |  pp1024 @ d8192 |       2472.30 ± 4.78 |
| deepseek2 30B.A3B Q4_K - Medium |  16.31 GiB |    29.94 B | CUDA       |  99 |    tg64 @ d8192 |         55.62 ± 0.34 |
| deepseek2 30B.A3B Q4_K - Medium |  16.31 GiB |    29.94 B | CUDA       |  99 | pp1024 @ d16384 |       1453.71 ± 0.95 |
| deepseek2 30B.A3B Q4_K - Medium |  16.31 GiB |    29.94 B | CUDA       |  99 |   tg64 @ d16384 |         34.47 ± 0.10 |
| deepseek2 30B.A3B Q4_K - Medium |  16.31 GiB |    29.94 B | CUDA       |  99 | pp1024 @ d32768 |        828.11 ± 0.30 |
| deepseek2 30B.A3B Q4_K - Medium |  16.31 GiB |    29.94 B | CUDA       |  99 |   tg64 @ d32768 |         19.02 ± 0.03 |

build: 054d8b0f2 (8396)

# llama-server + llama-benchy
# llama-server version: 8396 (054d8b0f2)
$ llama-server \
  --model unsloth/Qwen3.5-35B-A3B-GGUF/Qwen3.5-35B-A3B-UD-Q3_K_XL.gguf \
  --jinja --ctx-size 262144 \
  --temp 1.0 --top-p 0.95 --top-k 20 --min-p 0.00
$ uvx llama-benchy@v0.3.4 --base-url http://127.0.0.1:8080 --no-cache --model Qwen/Qwen3.5-35B-A3B --depth 0 8192 16384 32768 --runs 5
| model                |            test |               t/s |       peak t/s |         ttfr (ms) |      est_ppt (ms) |     e2e_ttft (ms) |
|:---------------------|----------------:|------------------:|---------------:|------------------:|------------------:|------------------:|
| Qwen/Qwen3.5-35B-A3B |          pp2048 | 3171.60 ± 1283.20 |                |   805.91 ± 400.47 |   804.21 ± 400.47 |   806.03 ± 400.48 |
| Qwen/Qwen3.5-35B-A3B |            tg32 |    109.62 ± 12.48 | 113.47 ± 12.96 |                   |                   |                   |
| Qwen/Qwen3.5-35B-A3B |  pp2048 @ d8192 |  4900.92 ± 366.64 |                |  2103.10 ± 158.42 |  2101.40 ± 158.42 |  2103.22 ± 158.43 |
| Qwen/Qwen3.5-35B-A3B |    tg32 @ d8192 |     107.39 ± 3.03 |  111.32 ± 3.05 |                   |                   |                   |
| Qwen/Qwen3.5-35B-A3B | pp2048 @ d16384 |  4218.22 ± 254.81 |                |  4387.78 ± 269.90 |  4386.08 ± 269.90 |  4387.91 ± 269.94 |
| Qwen/Qwen3.5-35B-A3B |   tg32 @ d16384 |      99.04 ± 1.98 |  102.58 ± 2.09 |                   |                   |                   |
| Qwen/Qwen3.5-35B-A3B | pp2048 @ d32768 |  3486.46 ± 331.35 |                | 10078.22 ± 952.37 | 10076.53 ± 952.37 | 10078.33 ± 952.37 |
| Qwen/Qwen3.5-35B-A3B |   tg32 @ d32768 |      87.25 ± 3.41 |   90.46 ± 3.56 |                   |                   |                   |
$ llama-server \
  --model unsloth/Qwen3.5-4B-GGUF/Qwen3.5-4B-Q8_0.gguf \
  --jinja --ctx-size 262144 \
  --temp 1.0 --top-p 0.95 --top-k 20 --min-p 0.00
$ uvx llama-benchy@v0.3.5 --base-url http://127.0.0.1:8080 --no-cache --model Qwen/Qwen3.5-4B --depth 0 8192 16384 32768 --runs 5
| model           |            test |               t/s |      peak t/s |        ttfr (ms) |     est_ppt (ms) |    e2e_ttft (ms) |
|:----------------|----------------:|------------------:|--------------:|-----------------:|-----------------:|-----------------:|
| Qwen/Qwen3.5-4B |          pp2048 | 7862.30 ± 1114.94 |               |   267.98 ± 42.54 |   266.63 ± 42.54 |   268.10 ± 42.54 |
| Qwen/Qwen3.5-4B |            tg32 |     118.85 ± 0.74 | 123.27 ± 0.90 |                  |                  |                  |
| Qwen/Qwen3.5-4B |  pp2048 @ d8192 | 8268.40 ± 1028.33 |               | 1260.64 ± 167.98 | 1259.29 ± 167.98 | 1260.76 ± 167.99 |
| Qwen/Qwen3.5-4B |    tg32 @ d8192 |     106.45 ± 4.00 | 110.36 ± 4.25 |                  |                  |                  |
| Qwen/Qwen3.5-4B | pp2048 @ d16384 |  6616.98 ± 557.83 |               | 2807.17 ± 239.17 | 2805.81 ± 239.17 | 2807.28 ± 239.17 |
| Qwen/Qwen3.5-4B |   tg32 @ d16384 |      93.11 ± 3.12 |  96.60 ± 3.29 |                  |                  |                  |
| Qwen/Qwen3.5-4B | pp2048 @ d32768 |  5179.34 ± 663.92 |               | 6835.63 ± 879.64 | 6834.27 ± 879.64 | 6835.73 ± 879.64 |
| Qwen/Qwen3.5-4B |   tg32 @ d32768 |      78.65 ± 4.70 |  81.64 ± 4.81 |                  |                  |                  |

# sglang commit 7f99319c
# Add --mamba-scheduler-strategy extra_buffer to fix error: 
# ValueError: Speculative decoding for Qwen3_5ForConditionalGeneration is not compatible with radix cache when using --mamba-scheduler-strategy no_buffer. To use radix cache with speculative decoding, please use --mamba-scheduler-strategy extra_buffer and set SGLANG_ENABLE_SPEC_V2=1.
$ SGLANG_ENABLE_SPEC_V2=1 uv run python -m sglang.launch_server \
  --model Qwen/Qwen3.5-4B \
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
| Qwen/Qwen3.5-4B |          pp2048 |  8768.36 ± 886.82 |              |  239.95 ± 21.02 |  235.78 ± 21.02 |  240.08 ± 21.03 |
| Qwen/Qwen3.5-4B |            tg32 |      49.87 ± 0.22 | 55.22 ± 0.68 |                 |                 |                 |
| Qwen/Qwen3.5-4B |  pp2048 @ d8192 | 11567.46 ± 226.15 |              |  889.81 ± 16.91 |  885.64 ± 16.91 |  889.93 ± 16.91 |
| Qwen/Qwen3.5-4B |    tg32 @ d8192 |      49.00 ± 0.06 | 53.82 ± 0.75 |                 |                 |                 |
| Qwen/Qwen3.5-4B | pp2048 @ d16384 | 11502.00 ± 381.09 |              | 1608.61 ± 55.36 | 1604.44 ± 55.36 | 1608.72 ± 55.35 |
| Qwen/Qwen3.5-4B |   tg32 @ d16384 |      47.91 ± 0.14 | 53.12 ± 0.42 |                 |                 |                 |
| Qwen/Qwen3.5-4B | pp2048 @ d32768 |  11019.27 ± 76.24 |              | 3163.95 ± 21.94 | 3159.78 ± 21.94 | 3164.07 ± 21.93 |
| Qwen/Qwen3.5-4B |   tg32 @ d32768 |      45.98 ± 0.20 | 51.13 ± 0.45 |                 |                 |                 |

# vllm 0.17.1
$ uv run vllm serve Qwen/Qwen3.5-4B \
  --speculative-config '{"method": "mtp", "num_speculative_tokens": 1}' \
  --reasoning-parser qwen3
$ uvx llama-benchy@v0.3.5 --base-url http://127.0.0.1:8000/v1 --no-cache --model Qwen/Qwen3.5-4B --depth 0 8192 16384 32768 --runs 5
| model           |            test |                t/s |     peak t/s |       ttfr (ms) |    est_ppt (ms) |   e2e_ttft (ms) |
|:----------------|----------------:|-------------------:|-------------:|----------------:|----------------:|----------------:|
| Qwen/Qwen3.5-4B |          pp2048 | 10110.05 ± 4405.47 |              | 451.52 ± 562.67 | 447.82 ± 562.67 | 454.00 ± 561.53 |
| Qwen/Qwen3.5-4B |            tg32 |       66.71 ± 0.07 | 70.56 ± 0.14 |                 |                 |                 |
| Qwen/Qwen3.5-4B |  pp2048 @ d8192 |  14004.87 ± 241.15 |              |  735.14 ± 12.90 |  731.44 ± 12.90 |  735.26 ± 12.89 |
| Qwen/Qwen3.5-4B |    tg32 @ d8192 |       54.32 ± 0.38 | 57.67 ± 0.45 |                 |                 |                 |
| Qwen/Qwen3.5-4B | pp2048 @ d16384 |  13537.13 ± 161.68 |              | 1365.56 ± 16.32 | 1361.86 ± 16.32 | 1365.72 ± 16.39 |
| Qwen/Qwen3.5-4B |   tg32 @ d16384 |       45.23 ± 1.29 | 47.95 ± 1.38 |                 |                 |                 |
| Qwen/Qwen3.5-4B | pp2048 @ d32768 |   12372.68 ± 93.63 |              | 2817.89 ± 21.29 | 2814.18 ± 21.29 | 2818.00 ± 21.29 |
| Qwen/Qwen3.5-4B |   tg32 @ d32768 |       33.89 ± 0.68 | 35.93 ± 0.74 |                 |                 |                 |
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

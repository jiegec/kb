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
# llama-server version: 8286 (5f91b1d5d)
$ llama-server \
  --model unsloth/Qwen3.5-35B-A3B-GGUF/Qwen3.5-35B-A3B-UD-Q3_K_XL.gguf \
  --jinja --ctx-size 262144 \
  --temp 1.0 --top-p 0.95 --top-k 20 --min-p 0.00
$ uvx llama-benchy@v0.3.4 --base-url http://127.0.0.1:8080 --no-cache --model Qwen/Qwen3.5-35B-A3B --depth 0 8192 16384 32768 --runs 5
| model                |            test |               t/s |       peak t/s |         ttfr (ms) |      est_ppt (ms) |     e2e_ttft (ms) |
|:---------------------|----------------:|------------------:|---------------:|------------------:|------------------:|------------------:|
| Qwen/Qwen3.5-35B-A3B |          pp2048 | 2558.51 ± 1069.81 |                |  1017.02 ± 521.76 |  1015.83 ± 521.76 |  1017.14 ± 521.78 |
| Qwen/Qwen3.5-35B-A3B |            tg32 |    106.32 ± 11.14 | 110.05 ± 11.53 |                   |                   |                   |
| Qwen/Qwen3.5-35B-A3B |  pp2048 @ d8192 |  4067.16 ± 243.41 |                |  2528.09 ± 148.53 |  2526.90 ± 148.53 |  2528.23 ± 148.53 |
| Qwen/Qwen3.5-35B-A3B |    tg32 @ d8192 |     103.21 ± 2.77 |  107.02 ± 2.85 |                   |                   |                   |
| Qwen/Qwen3.5-35B-A3B | pp2048 @ d16384 |  3606.17 ± 165.08 |                |  5123.32 ± 232.18 |  5122.13 ± 232.18 |  5123.43 ± 232.18 |
| Qwen/Qwen3.5-35B-A3B |   tg32 @ d16384 |      95.02 ± 1.95 |   98.98 ± 1.95 |                   |                   |                   |
| Qwen/Qwen3.5-35B-A3B | pp2048 @ d32768 |  3077.20 ± 225.70 |                | 11375.13 ± 811.46 | 11373.95 ± 811.46 | 11375.25 ± 811.48 |
| Qwen/Qwen3.5-35B-A3B |   tg32 @ d32768 |      84.94 ± 2.32 |   88.18 ± 2.60 |                   |                   |                   |
$ llama-server \
  --model unsloth/Qwen3.5-4B-GGUF/Qwen3.5-4B-Q8_0.gguf \
  --jinja --ctx-size 262144 \
  --temp 1.0 --top-p 0.95 --top-k 20 --min-p 0.00
$ uvx llama-benchy@v0.3.4 --base-url http://127.0.0.1:8080 --no-cache --model Qwen/Qwen3.5-4B --depth 0 8192 16384 32768 --runs 5
| model           |            test |              t/s |      peak t/s |        ttfr (ms) |     est_ppt (ms) |    e2e_ttft (ms) |
|:----------------|----------------:|-----------------:|--------------:|-----------------:|-----------------:|-----------------:|
| Qwen/Qwen3.5-4B |          pp2048 | 5884.44 ± 597.23 |               |   353.71 ± 38.52 |   352.09 ± 38.52 |   353.82 ± 38.52 |
| Qwen/Qwen3.5-4B |            tg32 |    111.07 ± 6.90 | 114.92 ± 7.16 |                  |                  |                  |
| Qwen/Qwen3.5-4B |  pp2048 @ d8192 | 6434.15 ± 509.45 |               | 1603.20 ± 124.67 | 1601.58 ± 124.67 | 1603.30 ± 124.68 |
| Qwen/Qwen3.5-4B |    tg32 @ d8192 |    100.81 ± 4.02 | 104.42 ± 4.11 |                  |                  |                  |
| Qwen/Qwen3.5-4B | pp2048 @ d16384 | 5523.88 ± 346.92 |               | 3351.58 ± 207.61 | 3349.95 ± 207.61 | 3351.72 ± 207.56 |
| Qwen/Qwen3.5-4B |   tg32 @ d16384 |     87.84 ± 2.97 |  91.12 ± 3.10 |                  |                  |                  |
| Qwen/Qwen3.5-4B | pp2048 @ d32768 | 4293.27 ± 444.08 |               | 8194.35 ± 805.30 | 8192.73 ± 805.30 | 8194.46 ± 805.30 |
| Qwen/Qwen3.5-4B |   tg32 @ d32768 |     74.82 ± 3.33 |  77.60 ± 3.57 |                  |                  |                  |

# sglang commit 57b093d
# Add --tp 2 (use two cards) due to OOM
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
  --mem-fraction-static 0.8 \
  --tp 2 \
  --mamba-scheduler-strategy extra_buffer
$ uvx llama-benchy@v0.3.4 --base-url http://127.0.0.1:30000/v1 --no-cache --model Qwen/Qwen3.5-4B --depth 0 8192 16384 32768 --runs 5
| model           |            test |              t/s |     peak t/s |       ttfr (ms) |    est_ppt (ms) |   e2e_ttft (ms) |
|:----------------|----------------:|-----------------:|-------------:|----------------:|----------------:|----------------:|
| Qwen/Qwen3.5-4B |          pp2048 | 6999.30 ± 337.02 |              |  298.17 ± 14.26 |  293.43 ± 14.26 |  298.31 ± 14.27 |
| Qwen/Qwen3.5-4B |            tg32 |     63.38 ± 0.26 | 69.68 ± 0.68 |                 |                 |                 |
| Qwen/Qwen3.5-4B |  pp2048 @ d8192 | 9171.37 ± 455.86 |              | 1124.28 ± 58.29 | 1119.54 ± 58.29 | 1124.41 ± 58.29 |
| Qwen/Qwen3.5-4B |    tg32 @ d8192 |     62.56 ± 0.30 | 68.99 ± 0.59 |                 |                 |                 |
| Qwen/Qwen3.5-4B | pp2048 @ d16384 | 9508.49 ± 100.97 |              | 1943.56 ± 20.39 | 1938.82 ± 20.39 | 1943.71 ± 20.35 |
| Qwen/Qwen3.5-4B |   tg32 @ d16384 |     61.17 ± 0.53 | 67.91 ± 1.01 |                 |                 |                 |
| Qwen/Qwen3.5-4B | pp2048 @ d32768 |  9396.72 ± 30.12 |              | 3710.01 ± 11.91 | 3705.27 ± 11.91 | 3710.14 ± 11.91 |
| Qwen/Qwen3.5-4B |   tg32 @ d32768 |     58.76 ± 1.87 | 64.87 ± 2.16 |                 |                 |                 |

# vllm 0.17.0
$ uv run vllm serve Qwen/Qwen3.5-4B \
  --speculative-config '{"method": "mtp", "num_speculative_tokens": 1}' \
  --reasoning-parser qwen3
$ uvx llama-benchy@v0.3.4 --base-url http://127.0.0.1:8000/v1 --no-cache --model Qwen/Qwen3.5-4B --depth 0 8192 16384 32768 --runs 5
| model           |            test |                t/s |     peak t/s |       ttfr (ms) |    est_ppt (ms) |   e2e_ttft (ms) |
|:----------------|----------------:|-------------------:|-------------:|----------------:|----------------:|----------------:|
| Qwen/Qwen3.5-4B |          pp2048 | 10139.24 ± 4522.21 |              | 499.86 ± 661.47 | 496.25 ± 661.47 | 499.99 ± 661.51 |
| Qwen/Qwen3.5-4B |            tg32 |       67.30 ± 0.22 | 71.37 ± 0.18 |                 |                 |                 |
| Qwen/Qwen3.5-4B |  pp2048 @ d8192 |  13895.18 ± 229.91 |              |  740.83 ± 12.27 |  737.22 ± 12.27 |  741.50 ± 11.55 |
| Qwen/Qwen3.5-4B |    tg32 @ d8192 |       53.90 ± 1.38 | 57.13 ± 1.64 |                 |                 |                 |
| Qwen/Qwen3.5-4B | pp2048 @ d16384 |  13655.20 ± 130.86 |              | 1353.61 ± 12.96 | 1350.00 ± 12.96 | 1353.86 ± 13.02 |
| Qwen/Qwen3.5-4B |   tg32 @ d16384 |       45.42 ± 1.39 | 48.22 ± 1.54 |                 |                 |                 |
| Qwen/Qwen3.5-4B | pp2048 @ d32768 |   12354.36 ± 91.77 |              | 2821.91 ± 21.04 | 2818.30 ± 21.04 | 2822.02 ± 21.05 |
| Qwen/Qwen3.5-4B |   tg32 @ d32768 |       33.76 ± 0.99 | 35.81 ± 1.11 |                 |                 |                 |
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
$ uv run python3 -m mlx_lm.benchmark --model ./mlx-community/Qwen3.5-4B-MLX-4bit -p 1024 -g 64
Running warmup..
Timing with prompt_tokens=1024, generation_tokens=64, batch_size=1.
Trial 1:  prompt_tps=351.905, generation_tps=38.757, peak_memory=3.502
Trial 2:  prompt_tps=363.097, generation_tps=38.150, peak_memory=3.503
Trial 3:  prompt_tps=359.749, generation_tps=39.020, peak_memory=3.503
Trial 4:  prompt_tps=359.048, generation_tps=39.020, peak_memory=3.504
Trial 5:  prompt_tps=358.087, generation_tps=39.119, peak_memory=3.504
Averages: prompt_tps=358.377, generation_tps=38.813, peak_memory=3.503
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

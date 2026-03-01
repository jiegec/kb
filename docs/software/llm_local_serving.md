# LLM 本地部署

## 安装 uv

```shell
pipx install uv
set -x PATH ~/.local/bin $PATH
```

## GLM-4.7-Flash

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
$ curl -fsSL https://lmstudio.ai/install.sh | bash
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
# build latest llama.cpp
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-cli llama-mtmd-cli llama-server llama-gguf-split llama-bench
cp llama.cpp/build/bin/llama-* llama.cpp

# download gguf from hf
uv run hf download unsloth/GLM-4.7-Flash-GGUF \
    --local-dir unsloth/GLM-4.7-Flash-GGUF \
    --include "*UD-Q2_K_XL*"
# serve
./llama.cpp/llama-server \
    --model unsloth/GLM-4.7-Flash-GGUF/GLM-4.7-Flash-UD-Q2_K_XL.gguf \
    --jinja --ctx-size 202752 \
    --temp 0.7 --top-p 1.0 --min-p 0.01 --fit on
./llama.cpp/llama-bench \
    --model unsloth/GLM-4.7-Flash-GGUF/GLM-4.7-Flash-UD-Q2_K_XL.gguf
```

## Qwen3.5 series

llama.cpp:

```shell
# follow https://unsloth.ai/docs/models/qwen3.5
# build latest llama.cpp
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-cli llama-mtmd-cli llama-server llama-gguf-split llama-bench
cp llama.cpp/build/bin/llama-* llama.cpp

# download gguf from hf
# Qwen3.5-27B
uv run hf download unsloth/Qwen3.5-27B-GGUF \
    --local-dir unsloth/Qwen3.5-27B-GGUF \
    Qwen3.5-27B-UD-Q4_K_XL.gguf
./llama.cpp/llama-server \
    --model unsloth/Qwen3.5-27B-GGUF/Qwen3.5-27B-UD-Q4_K_XL.gguf \
    --jinja --ctx-size 262144 \
    --temp 1.0 --top-p 0.95 --top-k 20 --min-p 0.00

# Qwen3.5-35B-A3B
uv run hf download unsloth/Qwen3.5-35B-A3B-GGUF \
    --local-dir unsloth/Qwen3.5-35B-A3B-GGUF \
    Qwen3.5-35B-A3B-UD-Q3_K_XL.gguf
./llama.cpp/llama-server \
    --model unsloth/Qwen3.5-35B-A3B-GGUF/Qwen3.5-35B-A3B-UD-Q3_K_XL.gguf \
    --jinja --ctx-size 262144 \
    --temp 1.0 --top-p 0.95 --top-k 20 --min-p 0.00
```

## 常见环境变量

- `HF_HUB_OFFLINE=1`
- `CUDA_VISIBLE_DEVICES`

## 推理性能测试

```shell
$ llama-bench -p 1024 -n 64 -d 0,16384,32768,49152 --model unsloth/Qwen3.5-27B-GGUF/Qwen3.5-27B-UD-Q4_K_XL.gguf
ggml_cuda_init: found 1 CUDA devices:
  Device 0: NVIDIA GeForce RTX 4090, compute capability 8.9, VMM: yes
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| qwen35 ?B Q4_K - Medium        |  15.57 GiB |    26.90 B | CUDA       |  99 |          pp1024 |       2458.27 ± 0.90 |
| qwen35 ?B Q4_K - Medium        |  15.57 GiB |    26.90 B | CUDA       |  99 |            tg64 |         38.99 ± 0.34 |
| qwen35 ?B Q4_K - Medium        |  15.57 GiB |    26.90 B | CUDA       |  99 | pp1024 @ d16384 |       1709.17 ± 1.14 |
| qwen35 ?B Q4_K - Medium        |  15.57 GiB |    26.90 B | CUDA       |  99 |   tg64 @ d16384 |         36.41 ± 0.21 |
| qwen35 ?B Q4_K - Medium        |  15.57 GiB |    26.90 B | CUDA       |  99 | pp1024 @ d32768 |       1305.55 ± 1.61 |
| qwen35 ?B Q4_K - Medium        |  15.57 GiB |    26.90 B | CUDA       |  99 |   tg64 @ d32768 |         33.23 ± 0.17 |
| qwen35 ?B Q4_K - Medium        |  15.57 GiB |    26.90 B | CUDA       |  99 | pp1024 @ d49152 |       1044.94 ± 0.57 |
| qwen35 ?B Q4_K - Medium        |  15.57 GiB |    26.90 B | CUDA       |  99 |   tg64 @ d49152 |         30.73 ± 0.18 |

build: 244641955 (8148)
$ llama-bench -p 1024 -n 64 -d 0,16384,32768,49152 --model unsloth/Qwen3.5-35B-A3B-GGUF/Qwen3.5-35B-A3B-UD-Q3_K_XL.gguf
ggml_cuda_init: found 1 CUDA devices:
  Device 0: NVIDIA GeForce RTX 4090, compute capability 8.9, VMM: yes
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| qwen35moe ?B Q3_K - Medium     |  14.66 GiB |    34.66 B | CUDA       |  99 |          pp1024 |      5179.66 ± 11.30 |
| qwen35moe ?B Q3_K - Medium     |  14.66 GiB |    34.66 B | CUDA       |  99 |            tg64 |        116.50 ± 1.84 |
| qwen35moe ?B Q3_K - Medium     |  14.66 GiB |    34.66 B | CUDA       |  99 | pp1024 @ d16384 |       3727.19 ± 5.49 |
| qwen35moe ?B Q3_K - Medium     |  14.66 GiB |    34.66 B | CUDA       |  99 |   tg64 @ d16384 |        109.45 ± 2.16 |
| qwen35moe ?B Q3_K - Medium     |  14.66 GiB |    34.66 B | CUDA       |  99 | pp1024 @ d32768 |       2900.42 ± 5.31 |
| qwen35moe ?B Q3_K - Medium     |  14.66 GiB |    34.66 B | CUDA       |  99 |   tg64 @ d32768 |         98.17 ± 1.51 |
| qwen35moe ?B Q3_K - Medium     |  14.66 GiB |    34.66 B | CUDA       |  99 | pp1024 @ d49152 |       2355.58 ± 3.22 |
| qwen35moe ?B Q3_K - Medium     |  14.66 GiB |    34.66 B | CUDA       |  99 |   tg64 @ d49152 |         89.04 ± 0.99 |

build: 244641955 (8148)
$ llama-bench -p 1024 -n 64 -d 0,16384,32768,49152 --model unsloth/Qwen3.5-35B-A3B-GGUF/Qwen3.5-35B-A3B-UD-Q4_K_XL.gguf
ggml_cuda_init: found 1 CUDA devices:
  Device 0: NVIDIA GeForce RTX 4090, compute capability 8.9, VMM: yes
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| qwen35moe ?B Q4_K - Medium     |  18.32 GiB |    34.66 B | CUDA       |  99 |          pp1024 |      5588.52 ± 46.39 |
| qwen35moe ?B Q4_K - Medium     |  18.32 GiB |    34.66 B | CUDA       |  99 |            tg64 |        118.33 ± 1.71 |
| qwen35moe ?B Q4_K - Medium     |  18.32 GiB |    34.66 B | CUDA       |  99 | pp1024 @ d16384 |       3923.77 ± 5.52 |
| qwen35moe ?B Q4_K - Medium     |  18.32 GiB |    34.66 B | CUDA       |  99 |   tg64 @ d16384 |        110.72 ± 2.12 |
| qwen35moe ?B Q4_K - Medium     |  18.32 GiB |    34.66 B | CUDA       |  99 | pp1024 @ d32768 |       3011.25 ± 7.92 |
| qwen35moe ?B Q4_K - Medium     |  18.32 GiB |    34.66 B | CUDA       |  99 |   tg64 @ d32768 |         98.76 ± 1.57 |
| qwen35moe ?B Q4_K - Medium     |  18.32 GiB |    34.66 B | CUDA       |  99 | pp1024 @ d49152 |       2418.66 ± 4.49 |
| qwen35moe ?B Q4_K - Medium     |  18.32 GiB |    34.66 B | CUDA       |  99 |   tg64 @ d49152 |         89.46 ± 1.22 |

build: 4e76d24f2 (8169)
$ llama-bench -p 1024 -n 64 -d 0,16384,32768,49152 --model unsloth/Qwen3.5-35B-A3B-GGUF/Qwen3.5-35B-A3B-MXFP4_MOE.gguf
ggml_cuda_init: found 1 CUDA devices:
  Device 0: NVIDIA GeForce RTX 4090, compute capability 8.9, VMM: yes
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| qwen35moe ?B MXFP4 MoE         |  18.42 GiB |    34.66 B | CUDA       |  99 |          pp1024 |      5727.19 ± 20.73 |
| qwen35moe ?B MXFP4 MoE         |  18.42 GiB |    34.66 B | CUDA       |  99 |            tg64 |        107.93 ± 1.49 |
| qwen35moe ?B MXFP4 MoE         |  18.42 GiB |    34.66 B | CUDA       |  99 | pp1024 @ d16384 |       3965.90 ± 7.16 |
| qwen35moe ?B MXFP4 MoE         |  18.42 GiB |    34.66 B | CUDA       |  99 |   tg64 @ d16384 |        101.73 ± 1.79 |
| qwen35moe ?B MXFP4 MoE         |  18.42 GiB |    34.66 B | CUDA       |  99 | pp1024 @ d32768 |       3037.72 ± 1.54 |
| qwen35moe ?B MXFP4 MoE         |  18.42 GiB |    34.66 B | CUDA       |  99 |   tg64 @ d32768 |         92.25 ± 1.14 |
| qwen35moe ?B MXFP4 MoE         |  18.42 GiB |    34.66 B | CUDA       |  99 | pp1024 @ d49152 |       2442.20 ± 2.96 |
| qwen35moe ?B MXFP4 MoE         |  18.42 GiB |    34.66 B | CUDA       |  99 |   tg64 @ d49152 |         83.67 ± 0.96 |

build: 4e76d24f2 (8169)
$ llama-bench -p 1024 -n 64 -d 0,16384,32768,49152 --model unsloth/GLM-4.7-Flash-GGUF/GLM-4.7-Flash-UD-Q2_K_XL.gguf
ggml_cuda_init: found 1 CUDA devices:
  Device 0: NVIDIA GeForce RTX 4090, compute capability 8.9, VMM: yes
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| deepseek2 30B.A3B Q2_K - Medium |  11.06 GiB |    29.94 B | CUDA       |  99 |          pp1024 |      5211.90 ± 11.66 |
| deepseek2 30B.A3B Q2_K - Medium |  11.06 GiB |    29.94 B | CUDA       |  99 |            tg64 |        138.18 ± 1.94 |
| deepseek2 30B.A3B Q2_K - Medium |  11.06 GiB |    29.94 B | CUDA       |  99 | pp1024 @ d16384 |       1406.24 ± 1.47 |
| deepseek2 30B.A3B Q2_K - Medium |  11.06 GiB |    29.94 B | CUDA       |  99 |   tg64 @ d16384 |         35.17 ± 0.12 |
| deepseek2 30B.A3B Q2_K - Medium |  11.06 GiB |    29.94 B | CUDA       |  99 | pp1024 @ d32768 |        807.41 ± 0.34 |
| deepseek2 30B.A3B Q2_K - Medium |  11.06 GiB |    29.94 B | CUDA       |  99 |   tg64 @ d32768 |         19.07 ± 0.04 |
| deepseek2 30B.A3B Q2_K - Medium |  11.06 GiB |    29.94 B | CUDA       |  99 | pp1024 @ d49152 |        492.38 ± 0.08 |
| deepseek2 30B.A3B Q2_K - Medium |  11.06 GiB |    29.94 B | CUDA       |  99 |   tg64 @ d49152 |         12.72 ± 0.02 |

build: 244641955 (8148)
$ llama-bench -p 1024 -n 64 -d 0,16384,32768,49152 --model unsloth/GLM-4.7-Flash-GGUF/GLM-4.7-Flash-UD-Q4_K_XL.gguf
ggml_cuda_init: found 1 CUDA devices:
  Device 0: NVIDIA GeForce RTX 4090, compute capability 8.9, VMM: yes
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| deepseek2 30B.A3B Q4_K - Medium |  16.31 GiB |    29.94 B | CUDA       |  99 |          pp1024 |      5956.03 ± 19.83 |
| deepseek2 30B.A3B Q4_K - Medium |  16.31 GiB |    29.94 B | CUDA       |  99 |            tg64 |        132.07 ± 1.71 |
| deepseek2 30B.A3B Q4_K - Medium |  16.31 GiB |    29.94 B | CUDA       |  99 | pp1024 @ d16384 |       1458.44 ± 1.41 |
| deepseek2 30B.A3B Q4_K - Medium |  16.31 GiB |    29.94 B | CUDA       |  99 |   tg64 @ d16384 |         34.52 ± 0.11 |
| deepseek2 30B.A3B Q4_K - Medium |  16.31 GiB |    29.94 B | CUDA       |  99 | pp1024 @ d32768 |        827.43 ± 0.44 |
| deepseek2 30B.A3B Q4_K - Medium |  16.31 GiB |    29.94 B | CUDA       |  99 |   tg64 @ d32768 |         18.98 ± 0.04 |
| deepseek2 30B.A3B Q4_K - Medium |  16.31 GiB |    29.94 B | CUDA       |  99 | pp1024 @ d49152 |        498.64 ± 0.19 |
| deepseek2 30B.A3B Q4_K - Medium |  16.31 GiB |    29.94 B | CUDA       |  99 |   tg64 @ d49152 |         12.71 ± 0.02 |

build: 244641955 (8148)
```

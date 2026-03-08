# LLM 本地部署

## 安装 uv

```shell
pipx install uv
set -x PATH ~/.local/bin $PATH
```

## 安装 llama.cpp

```shell
# build latest llama.cpp
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-cli llama-mtmd-cli llama-server llama-gguf-split llama-bench
cp llama.cpp/build/bin/llama-* llama.cpp
```

## 安装 lmstudio

```shell
curl -fsSL https://lmstudio.ai/install.sh | bash
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

# Qwen3.5-9B
uv run hf download unsloth/Qwen3.5-9B-GGUF \
    --local-dir unsloth/Qwen3.5-9B-GGUF \
    Qwen3.5-9B-Q8_0.gguf
```

## 常见环境变量

- `HF_HUB_OFFLINE=1`
- `CUDA_VISIBLE_DEVICES`

## 推理性能测试

```shell
$ llama-bench -p 1024 -n 64 -d 0,16384,32768,65536 --model unsloth/Qwen3.5-9B-GGUF/Qwen3.5-9B-Q8_0.gguf
ggml_cuda_init: found 1 CUDA devices:
  Device 0: NVIDIA GeForce RTX 4090, compute capability 8.9, VMM: yes
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| qwen35 ?B Q8_0                 |   8.86 GiB |     8.95 B | CUDA       |  99 |          pp1024 |      7777.04 ± 42.53 |
| qwen35 ?B Q8_0                 |   8.86 GiB |     8.95 B | CUDA       |  99 |            tg64 |         77.08 ± 0.66 |
| qwen35 ?B Q8_0                 |   8.86 GiB |     8.95 B | CUDA       |  99 | pp1024 @ d16384 |       5251.42 ± 3.52 |
| qwen35 ?B Q8_0                 |   8.86 GiB |     8.95 B | CUDA       |  99 |   tg64 @ d16384 |         73.35 ± 0.53 |
| qwen35 ?B Q8_0                 |   8.86 GiB |     8.95 B | CUDA       |  99 | pp1024 @ d32768 |       3931.33 ± 9.34 |
| qwen35 ?B Q8_0                 |   8.86 GiB |     8.95 B | CUDA       |  99 |   tg64 @ d32768 |         68.40 ± 0.36 |
| qwen35 ?B Q8_0                 |   8.86 GiB |     8.95 B | CUDA       |  99 | pp1024 @ d65536 |       2433.61 ± 0.84 |
| qwen35 ?B Q8_0                 |   8.86 GiB |     8.95 B | CUDA       |  99 |   tg64 @ d65536 |         60.40 ± 0.30 |

build: cf232515c (8207)
$ llama-bench -p 1024 -n 64 -d 0,8192,16384,32768 --model unsloth/Qwen3.5-27B-GGUF/Qwen3.5-27B-UD-Q4_K_XL.gguf
ggml_cuda_init: found 1 CUDA devices:
  Device 0: NVIDIA GeForce RTX 4090, compute capability 8.9, VMM: yes
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| qwen35 ?B Q4_K - Medium        |  16.40 GiB |    26.90 B | CUDA       |  99 |          pp1024 |       2498.24 ± 4.44 |
| qwen35 ?B Q4_K - Medium        |  16.40 GiB |    26.90 B | CUDA       |  99 |            tg64 |         37.67 ± 0.27 |
| qwen35 ?B Q4_K - Medium        |  16.40 GiB |    26.90 B | CUDA       |  99 |  pp1024 @ d8192 |       2103.78 ± 0.98 |
| qwen35 ?B Q4_K - Medium        |  16.40 GiB |    26.90 B | CUDA       |  99 |    tg64 @ d8192 |         36.73 ± 0.22 |
| qwen35 ?B Q4_K - Medium        |  16.40 GiB |    26.90 B | CUDA       |  99 | pp1024 @ d16384 |       1733.38 ± 0.73 |
| qwen35 ?B Q4_K - Medium        |  16.40 GiB |    26.90 B | CUDA       |  99 |   tg64 @ d16384 |         35.27 ± 0.18 |
| qwen35 ?B Q4_K - Medium        |  16.40 GiB |    26.90 B | CUDA       |  99 | pp1024 @ d32768 |       1323.81 ± 3.53 |
| qwen35 ?B Q4_K - Medium        |  16.40 GiB |    26.90 B | CUDA       |  99 |   tg64 @ d32768 |         32.35 ± 0.15 |

build: cf232515c (8207)
$ llama-bench -p 1024 -n 64 -d 0,8192,16384,32768 --model unsloth/Qwen3.5-35B-A3B-GGUF/Qwen3.5-35B-A3B-UD-Q3_K_XL.gguf
ggml_cuda_init: found 1 CUDA devices:
  Device 0: NVIDIA GeForce RTX 4090, compute capability 8.9, VMM: yes
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| qwen35moe ?B Q3_K - Medium     |  15.45 GiB |    34.66 B | CUDA       |  99 |          pp1024 |      5686.97 ± 25.48 |
| qwen35moe ?B Q3_K - Medium     |  15.45 GiB |    34.66 B | CUDA       |  99 |            tg64 |        108.82 ± 1.73 |
| qwen35moe ?B Q3_K - Medium     |  15.45 GiB |    34.66 B | CUDA       |  99 |  pp1024 @ d8192 |      4736.07 ± 11.93 |
| qwen35moe ?B Q3_K - Medium     |  15.45 GiB |    34.66 B | CUDA       |  99 |    tg64 @ d8192 |        107.86 ± 2.21 |
| qwen35moe ?B Q3_K - Medium     |  15.45 GiB |    34.66 B | CUDA       |  99 | pp1024 @ d16384 |      3958.30 ± 11.95 |
| qwen35moe ?B Q3_K - Medium     |  15.45 GiB |    34.66 B | CUDA       |  99 |   tg64 @ d16384 |        102.46 ± 1.63 |
| qwen35moe ?B Q3_K - Medium     |  15.45 GiB |    34.66 B | CUDA       |  99 | pp1024 @ d32768 |       3036.95 ± 9.78 |
| qwen35moe ?B Q3_K - Medium     |  15.45 GiB |    34.66 B | CUDA       |  99 |   tg64 @ d32768 |         92.48 ± 1.12 |

build: cf232515c (8207)
$ llama-bench -p 1024 -n 64 -d 0,8192,16384,32768 --model unsloth/Qwen3.5-35B-A3B-GGUF/Qwen3.5-35B-A3B-UD-Q4_K_XL.gguf
ggml_cuda_init: found 1 CUDA devices:
  Device 0: NVIDIA GeForce RTX 4090, compute capability 8.9, VMM: yes
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| qwen35moe ?B Q4_K - Medium     |  20.70 GiB |    34.66 B | CUDA       |  99 |          pp1024 |      5511.50 ± 22.65 |
| qwen35moe ?B Q4_K - Medium     |  20.70 GiB |    34.66 B | CUDA       |  99 |            tg64 |        107.37 ± 1.57 |
| qwen35moe ?B Q4_K - Medium     |  20.70 GiB |    34.66 B | CUDA       |  99 |  pp1024 @ d8192 |      4639.90 ± 13.14 |
| qwen35moe ?B Q4_K - Medium     |  20.70 GiB |    34.66 B | CUDA       |  99 |    tg64 @ d8192 |        106.09 ± 1.89 |
| qwen35moe ?B Q4_K - Medium     |  20.70 GiB |    34.66 B | CUDA       |  99 | pp1024 @ d16384 |       3848.08 ± 3.59 |
| qwen35moe ?B Q4_K - Medium     |  20.70 GiB |    34.66 B | CUDA       |  99 |   tg64 @ d16384 |        100.90 ± 1.72 |
| qwen35moe ?B Q4_K - Medium     |  20.70 GiB |    34.66 B | CUDA       |  99 | pp1024 @ d32768 |       2974.77 ± 3.39 |
| qwen35moe ?B Q4_K - Medium     |  20.70 GiB |    34.66 B | CUDA       |  99 |   tg64 @ d32768 |         91.18 ± 1.23 |

build: cf232515c (8207)
$ llama-bench -p 1024 -n 64 -d 0,8192,16384,32768 --model unsloth/Qwen3.5-35B-A3B-GGUF/Qwen3.5-35B-A3B-MXFP4_MOE.gguf
ggml_cuda_init: found 1 CUDA devices:
  Device 0: NVIDIA GeForce RTX 4090, compute capability 8.9, VMM: yes
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| qwen35moe ?B Q4_K - Medium     |  20.09 GiB |    34.66 B | CUDA       |  99 |          pp1024 |      5615.43 ± 16.85 |
| qwen35moe ?B Q4_K - Medium     |  20.09 GiB |    34.66 B | CUDA       |  99 |            tg64 |        107.20 ± 1.80 |
| qwen35moe ?B Q4_K - Medium     |  20.09 GiB |    34.66 B | CUDA       |  99 |  pp1024 @ d8192 |      4706.81 ± 13.93 |
| qwen35moe ?B Q4_K - Medium     |  20.09 GiB |    34.66 B | CUDA       |  99 |    tg64 @ d8192 |        106.77 ± 1.75 |
| qwen35moe ?B Q4_K - Medium     |  20.09 GiB |    34.66 B | CUDA       |  99 | pp1024 @ d16384 |      3895.65 ± 10.38 |
| qwen35moe ?B Q4_K - Medium     |  20.09 GiB |    34.66 B | CUDA       |  99 |   tg64 @ d16384 |        101.27 ± 1.33 |
| qwen35moe ?B Q4_K - Medium     |  20.09 GiB |    34.66 B | CUDA       |  99 | pp1024 @ d32768 |       3021.19 ± 4.83 |
| qwen35moe ?B Q4_K - Medium     |  20.09 GiB |    34.66 B | CUDA       |  99 |   tg64 @ d32768 |         91.49 ± 1.22 |

build: cf232515c (8207)
$ llama-bench -p 1024 -n 64 -d 0,8192,16384,32768 --model unsloth/GLM-4.7-Flash-GGUF/GLM-4.7-Flash-UD-Q2_K_XL.gguf
ggml_cuda_init: found 1 CUDA devices:
  Device 0: NVIDIA GeForce RTX 4090, compute capability 8.9, VMM: yes
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| deepseek2 30B.A3B Q2_K - Medium |  11.06 GiB |    29.94 B | CUDA       |  99 |          pp1024 |      5193.96 ± 29.07 |
| deepseek2 30B.A3B Q2_K - Medium |  11.06 GiB |    29.94 B | CUDA       |  99 |            tg64 |        136.02 ± 3.63 |
| deepseek2 30B.A3B Q2_K - Medium |  11.06 GiB |    29.94 B | CUDA       |  99 |  pp1024 @ d8192 |       2344.45 ± 3.63 |
| deepseek2 30B.A3B Q2_K - Medium |  11.06 GiB |    29.94 B | CUDA       |  99 |    tg64 @ d8192 |         56.39 ± 0.48 |
| deepseek2 30B.A3B Q2_K - Medium |  11.06 GiB |    29.94 B | CUDA       |  99 | pp1024 @ d16384 |       1403.63 ± 0.40 |
| deepseek2 30B.A3B Q2_K - Medium |  11.06 GiB |    29.94 B | CUDA       |  99 |   tg64 @ d16384 |         35.04 ± 0.17 |
| deepseek2 30B.A3B Q2_K - Medium |  11.06 GiB |    29.94 B | CUDA       |  99 | pp1024 @ d32768 |        809.62 ± 0.37 |
| deepseek2 30B.A3B Q2_K - Medium |  11.06 GiB |    29.94 B | CUDA       |  99 |   tg64 @ d32768 |         19.06 ± 0.03 |

build: cf232515c (8207)
$ llama-bench -p 1024 -n 64 -d 0,8192,16384,32768 --model unsloth/GLM-4.7-Flash-GGUF/GLM-4.7-Flash-UD-Q4_K_XL.gguf
ggml_cuda_init: found 1 CUDA devices:
  Device 0: NVIDIA GeForce RTX 4090, compute capability 8.9, VMM: yes
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| deepseek2 30B.A3B Q4_K - Medium |  16.31 GiB |    29.94 B | CUDA       |  99 |          pp1024 |      5995.20 ± 12.27 |
| deepseek2 30B.A3B Q4_K - Medium |  16.31 GiB |    29.94 B | CUDA       |  99 |            tg64 |        132.24 ± 2.37 |
| deepseek2 30B.A3B Q4_K - Medium |  16.31 GiB |    29.94 B | CUDA       |  99 |  pp1024 @ d8192 |       2474.67 ± 5.83 |
| deepseek2 30B.A3B Q4_K - Medium |  16.31 GiB |    29.94 B | CUDA       |  99 |    tg64 @ d8192 |         55.50 ± 0.60 |
| deepseek2 30B.A3B Q4_K - Medium |  16.31 GiB |    29.94 B | CUDA       |  99 | pp1024 @ d16384 |       1456.86 ± 1.14 |
| deepseek2 30B.A3B Q4_K - Medium |  16.31 GiB |    29.94 B | CUDA       |  99 |   tg64 @ d16384 |         34.49 ± 0.11 |
| deepseek2 30B.A3B Q4_K - Medium |  16.31 GiB |    29.94 B | CUDA       |  99 | pp1024 @ d32768 |        827.42 ± 0.35 |
| deepseek2 30B.A3B Q4_K - Medium |  16.31 GiB |    29.94 B | CUDA       |  99 |   tg64 @ d32768 |         18.96 ± 0.06 |

build: cf232515c (8207)
```

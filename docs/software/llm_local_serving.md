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

## 常见环境变量

- `HF_HUB_OFFLINE=1`
- `CUDA_VISIBLE_DEVICES`

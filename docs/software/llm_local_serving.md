# LLM 本地部署

## 安装 uv

```shell
pipx install uv
set -x PATH ~/.local/bin $PATH
```

## GLM-4.7-Flash

[zai-org/GLM-4.7-Flash](https://huggingface.co/zai-org/GLM-4.7-Flash)

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
```

## 常见环境变量

- `HF_HUB_ONLINE=1`
- `CUDA_VISIBLE_DEVICES`

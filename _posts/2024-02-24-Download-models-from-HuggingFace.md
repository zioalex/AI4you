---
layout: post
title: "Downloading AI Models from HuggingFace and Loading them into Ollama"
date: 2024-02-24
categories: [ai, llm, ollama]
tags: [huggingface, ollama, gguf, llama.cpp, local-ai]
---

This post covers how to download AI models from [HuggingFace](https://huggingface.co)
and load them into [Ollama](https://ollama.com) for local inference. It includes:
downloading pre-quantized GGUF models directly, handling gated models that require
accepting terms of service, and converting raw HuggingFace models to GGUF yourself
using `llama.cpp`.

> **References:** [HuggingFace CLI guide](https://huggingface.co/docs/huggingface_hub/en/guides/cli)

---

## 1. Install and authenticate

```bash
pip install -U "huggingface_hub[cli]"
```

Log in using a token from <https://huggingface.co/settings/tokens>:

```bash
hf auth login
```

---

## 2. Download a pre-quantized GGUF model

[TheBloke](https://huggingface.co/TheBloke) and other community contributors publish
ready-to-use GGUF files. Download a single file directly into a local folder:

```bash
# Download one specific GGUF file
hf download TheBloke/Mistral-7B-Instruct-v0.2-GGUF \
    mistral-7b-instruct-v0.2.Q8_0.gguf \
    --local-dir huggingface_models/

# Download all files from a repository
hf download TheBloke/SOLAR-10.7B-Instruct-v1.0-uncensored-GGUF \
    --local-dir huggingface_models/
```

> **Note:** `--local-dir-use-symlinks` and `--resume` are no longer needed — files
> are placed directly in the target folder and interrupted downloads resume automatically.

Alternatively, download directly with `curl`:

```bash
curl -L -O https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q8_0.gguf
```

---

## 3. Fix download timeouts (slow proxy / corporate network)

If you hit a `ReadTimeout` error, increase the default 10-second timeout:

```bash
export HF_HUB_DOWNLOAD_TIMEOUT=30
```

---

## 4. Gated models (accept terms of service first)

Some models (e.g., Meta Llama) require you to accept their terms on the HuggingFace
website before downloading. Once accepted, download as normal:

```bash
hf download meta-llama/Llama-3.1-8B-Instruct \
    --include "*.safetensors" \
    --local-dir ./llama-3.1-8b-instruct
```

---

## 5. Convert a HuggingFace model to GGUF with llama.cpp

If a model is not available as GGUF, you can convert it yourself.

### Clone llama.cpp and install dependencies

```bash
git clone https://github.com/ggml-org/llama.cpp.git
cd llama.cpp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the conversion

```bash
python3 convert_hf_to_gguf.py \
    /mnt/data/huggingface_models/models--deepcogito--cogito-v1-preview-llama-8B/snapshots/64c42369b3f322fbffb277bfff146551dd2823cc/ \
    --outfile /mnt/data/ollama/cogito-v1-preview-llama-8B_f16.gguf \
    --outtype f16
```

> Tip: always convert from a full-precision source (`f16` or `f32`) rather than from
> an already-quantized model for best quality.

---

## 6. Load the GGUF model into Ollama

Create a `Modelfile` pointing at the GGUF file:

```
# cogito-v1-preview-llama-8B_f16.modelfile
FROM /mnt/data/ollama/cogito-v1-preview-llama-8B_f16.gguf

TEMPLATE """ {{- if or .System .Tools }}<|start_header_id|>system<|end_header_id|>
{{- if .System }}

{{ .System }}
{{- end }}
{{- if .Tools }}

Available Tools:
{{ range $.Tools }}{{- . }}
{{ end }}
{{ end }}<|eot_id|>
{{- end }}
{{- range $i, $_ := .Messages }}
{{- $last := eq (len (slice $.Messages $i)) 1 }}
{{- if eq .Role "user" }}<|start_header_id|>user<|end_header_id|>

{{ .Content }}<|eot_id|>{{ if $last }}<|start_header_id|>assistant<|end_header_id|>

{{ end }}
{{- else if eq .Role "assistant" }}<|start_header_id|>assistant<|end_header_id|>
{{- if .ToolCalls }}
{{ range .ToolCalls }}
<tool_call>
{"name": "{{ .Function.Name }}", "arguments": {{ .Function.Arguments }}}
</tool_call>{{ end }}
{{- else }}

{{ .Content }}
{{- end }}{{ if not $last }}<|eot_id|>{{ end }}
{{- else if eq .Role "tool" }}<|start_header_id|>ipython<|end_header_id|>

{"content": "{{ .Content }}"}<|eot_id|>{{ if $last }}<|start_header_id|>assistant<|end_header_id|>

{{ end }}
{{- end }}
{{- end }}"""

PARAMETER stop "<|start_header_id|>"
PARAMETER stop "<|end_header_id|>"
PARAMETER stop "<|eot_id|>"
PARAMETER temperature 0.7
```

Register and run the model:

```bash
ollama create cogito8b -f cogito-v1-preview-llama-8B_f16.modelfile
ollama run cogito8b
```

Enable deep reasoning at the Ollama prompt:

```
/set system """Enable deep thinking subroutine."""
```

---

## 7. Use tool calling with the Ollama Python SDK

See [`ollama_tool_workflow.py`](ollama_tool_workflow.py) in this folder for a working
example of a chat loop that lets the model execute Python code via tool calls.


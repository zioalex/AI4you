# https://huggingface.co/docs/huggingface_hub/en/guides/cli
# https://www.youtube.com/watch?v=7BH4C6-HP14

pip install -U "huggingface_hub[cli]"
huggingface-cli login
https://huggingface.co/settings/tokens
  _Your token has been saved to /home/zioalex/.cache/huggingface/token
                                                                                                                                                                                                                                                                                      ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.2-GGUF mistral-7b-instruct-v0.2.Q8_0.gguf --local-dir  huggingface_models/ --local-dir-use-symlinks False

huggingface-cli download --cache-dir /mnt/data/huggingface_models cogito:8b

# This fails because of the 10 secs timeout. The proxy can be a bit slow
urllib3.exceptions.ReadTimeoutError: HTTPSConnectionPool(host='cdn-lfs-us-1.huggingface.co', port=443): Read timed out. (read timeout=10)

During handling of the above exception, another exception occurred:

````bash
Traceback (most recent call last):
  File "/home/zioalex/.local/bin/huggingface-cli", line 8, in <module>
    sys.exit(main())
  File "/home/zioalex/.local/lib/python3.8/site-packages/huggingface_hub/commands/huggingface_cli.py", line 49, in main
    service.run()
  File "/home/zioalex/.local/lib/python3.8/site-packages/huggingface_hub/commands/download.py", line 161, in run
    print(self._download())  # Print path to downloaded files
  File "/home/zioalex/.local/lib/python3.8/site-packages/huggingface_hub/commands/download.py", line 180, in _download
    return hf_hub_download(
  File "/home/zioalex/.local/lib/python3.8/site-packages/huggingface_hub/utils/_validators.py", line 119, in _inner_fn
    return fn(*args, **kwargs)
  File "/home/zioalex/.local/lib/python3.8/site-packages/huggingface_hub/file_download.py", line 1492, in hf_hub_download
    http_get(
  File "/home/zioalex/.local/lib/python3.8/site-packages/huggingface_hub/file_download.py", line 456, in http_get
    r = _request_wrapper(
  File "/home/zioalex/.local/lib/python3.8/site-packages/huggingface_hub/file_download.py", line 392, in _request_wrapper
    response = get_session().request(method=method, url=url, **params)
  File "/home/zioalex/.local/lib/python3.8/site-packages/requests/sessions.py", line 589, in request
    resp = self.send(prep, **send_kwargs)
  File "/home/zioalex/.local/lib/python3.8/site-packages/requests/sessions.py", line 703, in send
    r = adapter.send(request, **kwargs)
  File "/home/zioalex/.local/lib/python3.8/site-packages/huggingface_hub/utils/_http.py", line 68, in send
    return super().send(request, *args, **kwargs)
  File "/home/zioalex/.local/lib/python3.8/site-packages/requests/adapters.py", line 532, in send
    raise ReadTimeout(e, request=request)
requests.exceptions.ReadTimeout: (ReadTimeoutError("HTTPSConnectionPool(host='cdn-lfs-us-1.huggingface.co', port=443): Read timed out. (read timeout=10)"), '(Request ID: a33d910c-84c6-4514-8362-c705e2039d38)')
````
export HF_HUB_DOWNLOAD_TIMEOUT=30
# TO download all the files in the namespes/repo_id 
huggingface-cli download  TheBloke/SOLAR-10.7B-Instruct-v1.0-uncensored-GGUF --local-dir  huggingface_models/ --local-dir-use-symlinks False  --resume

# TO download only a specific file in the namespes/repo_id 
huggingface-cli download  TheBloke/SOLAR-10.7B-Instruct-v1.0-uncensored-GGUF solar-10.7b-instruct-v1.0-uncensored.Q8_0.gguf --local-dir  huggingface_models/ --local-dir-use-symlinks False  --resume

or download it directly with curl
curl -O  https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q8_0.gguf -L


# Or you can download the model that you want and then convert it to GGUF format with
## Clone the llama.cpp repo and install the requirements


```bash
    git clone https://github.com/ggml-org/llama.cpp.git
    cd llama.cpp
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
```

## Create the GGUF file from the HuggingFace model
```bash
    (.venv) opensource/llama.cpp (master) $ python3 convert_hf_to_gguf.py   /mnt/data/huggingface_models/models--deepcogito--cogito-v1-preview-llama-8B/snapshots/64c42369b3f322fbffb277bfff146551dd2823cc/   --outfile /mnt/data/ollama/cogito-v1-preview-llama-8B_f16.gguf   --outtype f16
```

ollama create  cogito8b -f cogito-v1-preview-llama-8B_f16.modelfile

Create the modelfile for ollama
```bash
cogito-v1-preview-llama-8B_f16.modelfile 
FROM  /mnt/data/ollama/cogito-v1-preview-llama-8B_f16.gguf

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

# tell Ollama where each conversation block ends
PARAMETER stop "<|start_header_id|>"
PARAMETER stop "<|end_header_id|>"
PARAMETER stop "<|eot_id|>"

# (optional) tweak runtime behaviour
PARAMETER temperature 0.7
```

## Run the reasoning model
```bash
ollama run cogito8b
```

## Enable reasoning
```bash
# in Ollama
/set system """Enable deep thinking subroutine."""
```

## Old gemma code
# And then you have to create the model in ollama manually

vi gemma-7b.modelfile 
#FROM /home/s0vp8h/.ollama/models/blobs/sha256:b1f4aabd3db466eb1c8ff792efa7647cf02e56202574b9cdd555c2df32d5af43
FROM /mnt/data/s0vp8h/huggingface_models/gemma-7b.gguf
#TEMPLATE """[INST] {{ .Prompt }} [/INST]"""

TEMPLATE """[INST] {{ if .System }}<<SYS>>{{ .System }}<</SYS>>

{{ end }}{{ .Prompt }} [/INST] """
PARAMETER stop "[INST]"
PARAMETER stop "[/INST]"
PARAMETER stop "<<SYS>>"
PARAMETER stop "<</SYS>>"

And then you need to create the model in ollama with
ollama create gemma7b -f gemma-7b.modelfile


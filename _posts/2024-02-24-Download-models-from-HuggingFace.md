# https://huggingface.co/docs/huggingface_hub/en/guides/cli
# https://www.youtube.com/watch?v=7BH4C6-HP14

pip install -U "huggingface_hub[cli]"
huggingface-cli login
https://huggingface.co/settings/tokens
  _Your token has been saved to /home/zioalex/.cache/huggingface/token
                                                                                                                                                                                                                                                                                      ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.2-GGUF mistral-7b-instruct-v0.2.Q8_0.gguf --local-dir  huggingface_models/ --local-dir-use-symlinks False
# This fails because of the 10 secs timeout. The proxy can be a bit slow
urllib3.exceptions.ReadTimeoutError: HTTPSConnectionPool(host='cdn-lfs-us-1.huggingface.co', port=443): Read timed out. (read timeout=10)

During handling of the above exception, another exception occurred:

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

export HF_HUB_DOWNLOAD_TIMEOUT=30
huggingface-cli download  w4r10ck/SOLAR-10.7B-Instruct-v1.0-uncensored --local-dir  huggingface_models/ --local-dir-use-symlinks False

or download it directly with curl
curl -O  https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q8_0.gguf -L
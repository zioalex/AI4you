import json, subprocess, ollama

# 1️⃣  Tell the model what "ipython" is and what arguments it takes
tools = [
    {
        "type": "function",
        "function": {
            "name": "ipython",
            "description": "Run Python 3.11 code and return stdout / stderr.",
            "parameters": {
                "type": "object",
                "required": ["content"],
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "Pure Python source code"
                    }
                }
            }
        }
    }
]

MODEL   = "cogito8b"   # whatever name you used with `ollama create`
history = []           # chat history we'll keep appending to

while True:
    # ── user turn ───────────────────────────────────────────────────
    user = input(">>> ")
    history.append({"role": "user", "content": user})

    # ── assistant turn (may propose tool calls) ────────────────────
    resp = ollama.chat(
        model    = MODEL,
        messages = history,
        tools    = tools,        # <--  pass the list here
        stream   = False
    )
    msg = resp["message"]
    history.append(msg)
    print(f"Message content {msg}")  # print the assistant's message
    # ── did the model ask to run ipython? ───────────────────────────
    if msg.get("tool_calls"):
        for call in msg["tool_calls"]:
            if call["function"]["name"] == "ipython":
                # grab the code string
                args = json.loads(call["function"]["arguments"])
                code = args["content"]

                # execute it safely (here, simple subprocess demo)
                try:
                    out = subprocess.check_output(
                        ["python", "-c", code],
                        stderr=subprocess.STDOUT,
                        text=True,
                        timeout=10
                    )
                except Exception as e:
                    out = f"ERROR: {e}"

                # feed result back to the model
                history.append({
                    "role":    "tool",
                    "name":    "ipython",
                    "content": out,
                })

        # assistant follows up, now knowing the tool result
        follow = ollama.chat(
            model    = MODEL,
            messages = history,
            tools    = tools,    # still include tools!
            stream   = False
        )
        print(follow["message"]["content"])
        history.append(follow["message"])
    else:
        # no tool call – just print the answer
        print(msg["content"])

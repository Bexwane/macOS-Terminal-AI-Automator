#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import platform
from datetime import datetime
from groq import Groq

# === CONFIG ===
API_KEY = os.environ.get("GROQ_API_KEY")
if not API_KEY:
    print("❌ GROQ_API_KEY missing. Add it to your ~/.zshrc")
    sys.exit(1)

MODEL = "deepseek-r1-distill-llama-70b"
client = Groq(api_key=API_KEY)

user_prompt = " ".join(sys.argv[1:]).strip()
if not user_prompt:
    print("⚠️ Usage: codeboss \"describe what you want done\"")
    sys.exit(1)
    
# === TERMINAL HISTORY ===
try:
    shell_history = subprocess.check_output("history | tail -n 10", shell=True, text=True)
except:
    shell_history = ""

# === SESSION MEMORY ===
memory_log_path = os.path.expanduser("~/.ai_session.jsonl")
recent_sessions = []

if os.path.exists(memory_log_path):
    with open(memory_log_path, "r") as f:
        recent_sessions = [json.loads(line) for line in f.readlines()[-3:]]
        
# === SYSTEM INSTRUCTION ===
system_behavior = (
    "You are SYNGH-AI-CODEBOSS, a cracked dev assistant. "
    "You respond ONLY in raw JSON. If the task is something trivial like making a folder or running a shell command, just give the shell code and set filename to \"\" and action to \"run\". If no file is needed, don't create one."
    "You respond ONLY in raw JSON. If a task like checking the IP can be done in one shell command, set filename to empty string and language to shell. Do not create Python files for basic shell tasks. Use action: \"run\" for safe commands."
    "For complex tasks like opening browser tabs, create AppleScript (.scpt) files on macOS."
    "{\n"
    "  \"filename\": \"name.py\",\n"
    "  \"language\": \"python\",\n"
    "  \"purpose\": \"what it does\",\n"
    "  \"action\": \"run\" | \"edit\" | \"save\",\n"
    "  \"code\": \"ACTUAL CODE\"\n"
    "}\n\n"
    "NO markdown, NO commentary, NO headings."
)

messages = [
    {"role": "system", "content": system_behavior},
    {"role": "user", "content": f"[context] Last terminal commands:\n{shell_history.strip()}"}
]

for s in recent_sessions:
    messages.append({
        "role": "user",
        "content": f"[memory] Prompt: {s['prompt']} → {s['filename']} ({s['action']})"
    })

messages.append({"role": "user", "content": user_prompt})
print("🧠 Thinking...\n")

response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    temperature=0.5,
    max_completion_tokens=2048,
    top_p=0.9,
    stream=False
)

import re

raw_reply = response.choices[0].message.content

# Strip all <think> ... </think> blocks — even with newlines
raw_reply = re.sub(r"<think>.*?</think>", "", raw_reply, flags=re.DOTALL).strip()

# Optional: double-check for JSON bracket only
start = raw_reply.find("{")
end = raw_reply.rfind("}") + 1
raw_reply = raw_reply[start:end]
try:
    data = json.loads(raw_reply)
    filename = data["filename"]
    action = data["action"].lower()
    code = data["code"]
    purpose = data.get("purpose", "No purpose given.")
except Exception as e:
    print("💀 AI sent bad JSON:\n")
    print(raw_reply)
    sys.exit(1)

# Save file only if filename is provided
if filename:
    with open(filename, "w") as f:
        f.write(code)
    
    # Make shell scripts executable
    if filename.endswith(".sh"):
        os.chmod(filename, 0o755)

# Handle shell commands (filename empty) differently
if not filename:
    # Pure shell command case
    print(f"💡 Purpose: {purpose}")
    print(f"🤖 Command: {code}")
    print("\n🧠 So... what now, ? Run it? Skip it?")
    user_input = input("👉 ").strip().lower()
    
    def decide_shell(user_input):
        if any(word in user_input for word in ["run", "execute", "go", "send"]):
            return "run"
        return "skip"
    
    choice = decide_shell(user_input)
    
    if choice == "run":
        print("🚀 Running command...\n")
        # Execute directly without extra output
        result = subprocess.run(
            code, 
            shell=True, 
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # Print clean output only if command produces output
        if result.stdout:
            print("Command Output:")
            print(result.stdout)
        if result.stderr:
            print("Command Errors:")
            print(result.stderr)
    else:
        print("🛑 Skipped running command.")
else:
    # File-based command case
    print(f"📁 File created: {filename}")
    print(f"💡 Purpose: {purpose}")
    print(f"🤖 Suggested Action: {action.upper()}")
    print("\n🧠 So... what now, mf? Run it? Edit it? Skip it?")
    user_input = input("👉 ").strip().lower()
    
    def decide(user_input):
        if any(word in user_input for word in ["run", "execute", "go", "send"]):
            return "run"
        elif any(word in user_input for word in ["edit", "open", "fix", "micro"]):
            return "edit"
        elif any(word in user_input for word in ["skip", "nah", "no", "leave"]):
            return "skip"
        else:
            return action
    
    choice = decide(user_input)
    
    if choice == "run":
        print("🚀 Running...\n")
        # Extended file type support
        if filename.endswith(".py"):
            subprocess.run(["python3", filename])
        elif filename.endswith(".sh"):
            subprocess.run(["bash", filename])
        elif filename.endswith(".js"):
            subprocess.run(["node", filename])
        elif filename.endswith(".scpt") and platform.system() == "Darwin":
            subprocess.run(["osascript", filename])
        elif filename.endswith(".rb"):
            subprocess.run(["ruby", filename])
        elif filename.endswith(".php"):
            subprocess.run(["php", filename])
        elif filename.endswith(".pl"):
            subprocess.run(["perl", filename])
        elif filename.endswith(".html"):
            if platform.system() == "Darwin":
                subprocess.run(["open", filename])
            elif platform.system() == "Linux":
                subprocess.run(["xdg-open", filename])
            else:
                print("⚠️ Unsupported platform for HTML opening")
        elif filename.endswith(".java"):
            class_name = os.path.splitext(filename)[0]
            subprocess.run(["javac", filename])
            subprocess.run(["java", class_name])
        else:
            print(f"⚠️ Unknown file type: {filename}")
            print("Trying to execute with default handler...")
            try:
                if platform.system() == "Darwin":
                    subprocess.run(["open", filename])
                elif platform.system() == "Linux":
                    subprocess.run(["xdg-open", filename])
                elif platform.system() == "Windows":
                    os.startfile(filename)
                else:
                    print("⚠️ No handler found for this file type")
            except Exception as e:
                print(f"❌ Failed to open file: {str(e)}")
    elif choice == "edit":
        print("✏️ Opening in micro...\n")
        subprocess.run(["micro", filename])
    else:
        print("🛑 Skipped. File is saved.")

# Log session
with open(memory_log_path, "a") as f:
    f.write(json.dumps({
        "timestamp": datetime.utcnow().isoformat(),
        "prompt": user_prompt,
        "filename": filename,
        "action": choice,
        "code": code
    }) + "\n")

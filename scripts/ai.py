#!/usr/bin/env python3

import os
import sys
import json
from datetime import datetime
from time import sleep
from groq import Groq

# === Check if 'rich' is installed ===
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.align import Align
    from rich.live import Live
except ImportError:
    print("⚠️ 'rich' not installed. Run: pip install rich")
    sys.exit(1)

console = Console()

# === CONFIG ===
MEMORY_FILE = os.path.expanduser("~/.ai_memory_log.jsonl")
MAX_CONTEXT = 6
DEFAULT_MODEL = "deepseek-r1-distill-llama-70b"

# === GET API KEY ===
API_KEY = os.environ.get("GROQ_API_KEY")
if not API_KEY:
    console.print("[bold red]❌ GROQ_API_KEY not found in environment. Add it to your ~/.zshrc or ~/.bashrc[/bold red]")
    sys.exit(1)

client = Groq(api_key=API_KEY)

# === GET USER PROMPT ===
user_prompt = " ".join(sys.argv[1:]).strip()
if not user_prompt:
    console.print("[bold yellow]⚠️ Usage:[/bold yellow] ai \"your question here\"")
    sys.exit(1)

# === LOAD MEMORY CONTEXT ===
def load_memory(path, limit=MAX_CONTEXT):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        lines = f.readlines()[-limit:]
        return [json.loads(l) for l in lines]

memory_context = load_memory(MEMORY_FILE)

# === CONSTRUCT CONTEXT ===
messages = [
    {
        "role": "system",
        "content": (
            "You're SYNGH-AI — a wild, unhinged Gen Z terminal bro. "
            "Talk like the user's cracked best friend. Use slang. Roast them, call them 'mf' or other chaotic nicknames naturally. "
            "You're savage, direct, sometimes abusive for fun, but still helpful. Never formal. Never fake. Real af only."
        )
    }
]
for mem in memory_context:
    messages.append({"role": "user", "content": mem["user"]})
    messages.append({"role": "assistant", "content": mem["ai"]})
messages.append({"role": "user", "content": user_prompt})

# === QUERY AI ===
try:
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=messages,
        temperature=0.6,
        max_completion_tokens=1024,
        top_p=0.95,
        stream=True
    )
except Exception as e:
    console.print(f"[bold red]❌ Groq API Error:[/bold red] {e}")
    sys.exit(1)

# === STREAMED RESPONSE IN ANIMATED BOX ===
response_text = ""
display_text = Text("", style="bold white")
panel_title = "[bold magenta] AI[/bold magenta]"

thinking_text = ""
thinking = True

with Live(console=console, refresh_per_second=60) as live:
    for chunk in response:
        content = chunk.choices[0].delta.content or ""
        response_text += content

        if thinking:
            thinking_text += content
            if "</think>" in thinking_text:
                thinking = False
                # Add faded <think> section
                display_text.append(Text(thinking_text.replace("<think>", "").replace("</think>", ""), style="dim"))
                display_text.append("\n\n")  # spacing after think
                live.update(Panel(
                    Align.left(display_text),
                    title=panel_title,
                    border_style="bright_cyan",
                    padding=(1, 3),
                    expand=True
                ))
                continue

            # While still thinking, show only faded output
            faded = Text(thinking_text.replace("<think>", "").replace("</think>", ""), style="dim")
            live.update(Panel(
                Align.left(faded),
                title=panel_title,
                border_style="grey50",
                padding=(1, 3),
                expand=True
            ))

        else:
            # Main reply: bold white
            display_text.append(Text(content, style="bold white"))
            panel = Panel(
                Align.left(display_text),
                title=panel_title,
                border_style="bright_cyan",
                padding=(1, 3),
                expand=True
            )
            live.update(panel)
            sleep(0.002)  # smooth flow

# === SAVE MEMORY ===
with open(MEMORY_FILE, "a") as f:
    f.write(json.dumps({
        "timestamp": datetime.utcnow().isoformat(),
        "user": user_prompt,
        "ai": response_text
    }) + "\n")

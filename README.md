**macOS Terminal AI Automator**

Bring AI and automation to your macOS Terminal.
	•	ai → Ask anything. Get quick answers without leaving your CLI.
	•	ag → Automate boring stuff like creating folders, batch renaming, compressing files, and more.

No more memorizing commands – just tell the AI what you need.

⸻

**Features**
	•	AI in your Terminal – Ask for commands, snippets, or explanations instantly.
	•	Automation on demand – One-liners to handle repetitive tasks.
	•	Lightweight & Fast – No extra setup beyond Python.

⸻

**Install**


chmod +x scripts/*.py    # Make scripts executable

or if you're confused, just simply put the scripts (ag.py and ai.py) in your home folder ( for example Users/davidpearson/ )

 and run these commands:
 
chmod +x ~/ai.py
chmod +x ~/ag.py

Here’s the full text for the updated part of your README (Requirements + API Key Setup + Install Instructions):

⸻

🛠 Requirements
	•	macOS
	•	Python 3.x
	•	Groq API Key (Free) → Get yours here
	•	Internet connection

⸻

🔑 Setting Up Groq API Key

To use the AI features, you need a Groq API key:
	Sign up and get your API key → [Groq Console](https://console.groq.com/keys)
	Open your shell config file:

nano ~/.zshrc


	Add this line (replace YOUR_KEY with your actual key):

export GROQ_API_KEY="YOUR_KEY"


	Save and reload your shell:

source ~/.zshrc



✅ Now the scripts can access your API key automatically.

⸻

**📦 Install Requirements**

Ensure Python is installed:

brew install python

**Usage**

Run AI assistant:

python scripts/ai.py "how do I kill a process by name?"

Run automation tool:

python scripts/ag.py "create 10 folders in Documents with a .txt file inside each"


⸻

 **Make It Easier (Add Shortcuts)**

If you use zsh (macOS default), add these lines to your ~/.zshrc:

alias ai="python /absolute/path/to/macos-terminal-ai-automator/scripts/ai.py"
alias ag="python /absolute/path/to/macos-terminal-ai-automator/scripts/ag.py"

Reload your shell:

source ~/.zshrc

 Now just type:

ai "what's the command to check disk space?"
ag "compress all PDFs in Documents"


⸻

**Example Use Cases**

ai "Give me a Python script to batch rename files"
ai "Show me how to list files sorted by size"

ag "Create 5 folders in Desktop and put a text file in each"
ag "Zip all images in Pictures"


⸻

When Prompted

Sometimes the tool will ask:

So... what now? Run it? Edit it? Skip it?
👉

Here’s what to type:
	•	run → Executes immediately (also works with: execute, go, send)
	•	edit → Opens file in editor (works with: open, fix)
	•	skip → Does nothing, just saves file (works with: nah, no)

⸻

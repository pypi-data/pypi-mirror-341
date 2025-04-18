<p align="center">
  <img src="https://raw.githubusercontent.com/ARJ2211/ask-git/refs/heads/main/assets/logo.png">
</p>

# 🧠 Ask-Git: Git History Explorer with Local LLMs

Ask-Git is a powerful CLI tool that lets developers **understand Git history** using natural language. It wraps around Git commands and feeds relevant context to **local LLMs (via Ollama)** to generate human-readable explanations and summaries — all without uploading your code or commits to the cloud.

## 🚀 Features

Ask-Git is currently focused on the following capabilities:

### ✅ Implemented

- **`explain <file>`**  
  Summarize recent changes made to a specific file.  
  This combines recent commits, diffs, and blame information to explain how a file evolved.

- **`summary --since <date> --until <date> [--author <name>]`**  
  Summarize commit activity in a date range (optionally filtered by author).  
  Ideal for understanding what happened during a sprint or review period.

### 🚧 In Progress

- **`why "<question>"`**  
  Ask why a feature, line, or change was made (coming soon).

- **`pr-summary`**  
  Generate a pull-request-style summary from recent commits (coming soon).

---

## 🛠️ Installation

Ask-Git is a Python CLI tool. Make sure you have Python 3.8+ installed.

You can install it directly from PyPI:

```bash
pip install ask-git
```

Or clone and install from source:

```bash
git clone https://github.com/ARJ2211/ask-git.git
cd ask-git
pip install -e .
```

---

## 🧠 Ollama Setup

You need [Ollama](https://ollama.com/) running locally to use the LLM features.

Install and start Ollama:

```bash
ollama serve
```

Pull a supported model (e.g., CodeLlama):

```bash
ollama pull codellama
```

Make sure it's accessible at `http://localhost:11434`.

---

## 🧾 Usage

Once installed, you can run the tool via the `ask-git` command:

### 🔍 Summarize Git Activity

```bash
ask-git summary --since 2024-04-01 --until 2024-04-15
```

Optional filter by author:

```bash
ask-git summary --since 2024-04-01 --until 2024-04-15 --author "Alice"
```

### 📄 Explain a File's History

```bash
ask-git explain path/to/your/file.py
```

This will pull recent changes to the file and ask the LLM to describe what happened.

---

## ⚙️ How It Works

- Uses GitPython and subprocess to gather `git log`, `diff`, and `blame` context.
- Builds custom prompts for the LLM to explain or summarize changes.
- Talks to Ollama via HTTP API for local LLM queries (e.g., Mistral, CodeLlama).
- Outputs explanations and summaries directly to your terminal using `rich`.

---

## 🧪 Development Status

This project is still evolving. Contributions are welcome!

- `explain` and `summary` are stable
- `why` and `pr-summary` are under active development

---

## 📩 Contact

Questions or suggestions?  
Check out [askaayush.com](https://www.askaayush.com) or raise an issue on [GitHub](https://github.com/ARJ2211/ask-git).

# GitReco

> 🧠 A CLI tool that suggests Git commit messages based on your changes.

`gitreco` is a developer-friendly CLI that analyzes your Git diff and suggests commit messages following commit standards like `feat:`, `fix:`, `refactor:`, etc.

---

## ✨ Features

- 📝 Suggests commit messages from current Git diff
- 🔍 Understands file changes to generate contextual messages
- 📦 Lightweight and easy to integrate into any Git workflow
- ✅ Supports conventional commit format

---

## 📦 Installation

```bash
pip install gitreco
```

# 🚀 Usage
```shell
gitreco
```
Example output:
```shell
Suggested commit message:
feat: Add support for language in greeting function
```

# 🔧 Requirements

This tool uses Ollama to run LLaMA 3.2 locally. Make sure you have the following installed:

1. Ollama
2. LLaMA 3.2 model (run the command below):

```shell
ollama pull llama3.2
```
💡 Note: Depending on your machine, downloading the model may take a few minutes.

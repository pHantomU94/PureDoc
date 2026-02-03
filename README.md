# PureDoc

**PureDoc** A lightweight utility to transform Markdown into clean, perfectly formatted Microsoft Word (.docx) files.

## 🛠️ Requirements

Before running the application, ensure your Mac has the following installed:

1. **Python 3.10+**: (3.12 is highly recommended for stability).
2. **Pandoc**: The universal document converter.
* Install via Homebrew: `brew install pandoc`


3. **Microsoft Word**: Required for generating the initial style template and final document viewing.

---

## 🚀 Installation & Deployment

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/PureDoc.git
cd PureDoc

```

### 2. Create and Activate a Virtual Environment (Recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Verify Essential Files

Ensure the following files are in the same directory as `app.py`:

* `bullet_process.lua`: The core Lua filter for processing lists and breaks.
* `template.docx`: The Word style reference (will be auto-generated on first run if missing).

---

## 📖 How to Use

1. **Launch the App**:
```bash
python3 app.py

```


2. **Paste Content**: Copy your Markdown text from ChatGPT/Claude and paste it into the left editor.
3. **Configure Options**:
* **"Ignore Bullet (•)"**: Enable this to remove bullet points and align list items as standard paragraphs.
* **"Numbered Lists"**: Choose whether to keep them as auto-numbered lists or convert them to plain text.


4. **Instant Preview**:
* **Right Panel**: View the processed Markdown structure.
* **👁️ (QuickLook Icon)**: Click to trigger the native macOS preview window for a 100% accurate Word layout check.


5. **Export**: Click **"Export Word"** to save your file. The document will open automatically once the conversion is complete.

---

## 📂 Project Structure

```text
.
├── app.py                # Main Flet GUI application
├── bullet_process.lua    # Pandoc Lua filter (Logic for lists and breaks)
├── template.docx         # Reference style template for Word export
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation

```

---

## 📜 License

This project is licensed under the [MIT License](https://www.google.com/search?q=LICENSE).

---

## 🤝 Contributing

Contributions are welcome!

* If you encounter API compatibility issues with newer Python versions (e.g., Python 3.14), please open an Issue.
* Feel free to submit a Pull Request if you have improvements for the Lua filter or the UI.

---

### 💡 Pro Tip for GitHub:

Don't forget to add a **https://www.google.com/search?q=LICENSE** file (MIT) to your repository. Would you like me to generate the standard text for that as well?
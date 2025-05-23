# 🎓 SIU Admission Chatbot

An intelligent AI-driven chatbot built to support prospective students of Saigon International University (SIU). Utilizing the Google Gemini Flash 2.0 API, it employs function calling, a hierarchically structured Markdown knowledge base, and a Gradio-powered interface to deliver fast, accurate, and scalable admissions support.

---

## 🚀 Features

- ✅ Understands natural language queries in Vietnamese.
- 🔍 Decomposes complex questions and finds the most relevant answer using a hierarchical search algorithm.
- 📂 Reads information from modular Markdown files stored in nested folders.
- 💬 Returns rewritten, human-readable answers via Gemini Flash 2.0.
- 🎛️ Easy to expand and maintain without technical expertise.

---

## UI Preview

![Chatbot Demo](video.gif)

Built using [Gradio](https://www.gradio.app/), allowing users to interact with the chatbot in a clean and intuitive interface.

---

## 🛠 Requirements

- Python `3.10.6`
- [Gradio](https://gradio.app/)
- [google-generativeai](https://pypi.org/project/google-generativeai/)
- tqdm (optional, for loading bars)

Install with:

```bash
pip install -r requirements.txt
````

---

## Knowledge Base Structure

The knowledge base is pre-structured as a tree-structured folder hierarchy using Markdown files (.md). The chatbot performs a top-down search, beginning from broad categories and descending into increasingly specific subfolders until it finds a file containing relevant content to answer the user's query.

This predefined structure allows the system to locate information accurately and systematically. Below is an example of the folder hierarchy for admissions-related content:

### Example: `content/` Directory

```bash
📁 content/
├── 📁 general/
│   ├── 📁 about-siu/
│   │   ├── 📄 history.md
│   │   ├── 📄 mission-vision.md
│   │   └── 📄 core-values.md
│   ├── 📁 campus-life/
│   │   ├── 📄 student-clubs.md
│   │   ├── 📄 events.md
│   │   └── 📄 internships.md
│   ├── 📁 facilities/
│   │   ├── 📄 labs.md
│   │   ├── 📄 dormitories.md
│   │   └── 📄 library.md
│   └── 📁 international-programs/
│       ├── 📄 exchange-programs.md
│       └── 📄 dual-degree.md
├── 📁 scholarships/
│   ├── 📄 scholarship-criteria.md
│   ├── 📄 application-process.md
│   └── 📄 important-dates.md
├── 📁 admissions/
│   ├── 📁 admission-methods/
│   │   ├── 📄 highschool-record.md
│   │   ├── 📄 national-exam.md
│   │   └── 📄 combined-method.md
│   ├── 📄 direct-admission-policy.md
│   ├── 📄 available-majors.md
│   ├── 📄 eligible-candidates.md
│   ├── 📄 admission-scope.md
│   └── 📁 application-process/
│       ├── 📄 how-to-apply.md
│       ├── 📄 admission-fee.md
│       └── 📄 application-form-guide.md
├── 📄 chatbot-faq.md
```

> Tip: Just add more folders or `.md` files and the chatbot will pick them up automatically. No code changes needed.

---

## How It Works

1. User submits a query in Vietnamese.
2. Gemini Flash 2.0 interprets the intent using natural language understanding.
3. The system decomposes the query (if needed).
4. A file traversal module searches through `content/` from top to bottom.
5. If a relevant `.md` file is found, the chatbot reads and rewrites the content into a conversational response.
6. The user receives a polished, informative answer.

---

## 🎯 Project Purpose

This project was built to:

* Reduce the workload of human admission officers.
* Offer instant, consistent answers to prospective students 24/7.
* Create a scalable and maintainable system for university-wide Q\&A services.
* Demonstrate how modern LLMs and structured data can work together effectively in education.

---

## 🧩 File Structure

```
📁 siu-admission-chatbot/
├── 📁 data/                  # Markdown-based knowledge base (structured by topics)
├── 📄 main.py               # Entry point for chatbot inference and coordination
├── 📄 UI.py                 # Gradio-based user interface for web interaction
├── 📄 file_searcher.py      # Handles traversal and lookup across folder hierarchy
├── 📄 search.py             # Uses Gemini LLM to match user intent with content
├── 📄 decomposer1.py        # Decomposes complex questions into sub-queries
├── 📄 requirements.txt      # List of Python dependencies
├── 📄 README.md             # Project documentation and setup instructions
└── 📄 test.ipynb            # Notebook to test and debug sample queries
```

---

## 💡 Example Use Cases

* “Các phương thức xét tuyển của SIU là gì?”
* “Điều kiện để được học bổng là gì?”
* “Hồ sơ cần những gì để đăng ký vào SIU?”
* “Trường SIU có chương trình trao đổi quốc tế không?”

The system will automatically determine the intent, locate the relevant Markdown file, and return a friendly, accurate response.

---

## 📌 Future Improvements

* 🔗 Integration with official SIU database/API.
* 🌐 Multilingual support (Vietnamese ⇄ English).
* 🧾 Logging and analytics to track popular queries.
* 🤖 Offline mode with cached content.

---





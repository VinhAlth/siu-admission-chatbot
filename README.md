Dưới đây là một **README chuyên nghiệp hoàn chỉnh** cho dự án Chatbot Tuyển sinh SIU. Bạn chỉ cần **copy toàn bộ một lần**, không cần chỉnh sửa thêm nếu không muốn. Văn phong phù hợp cho các dự án AI nghiên cứu hoặc triển khai thực tế tại trường.

---

````markdown
# 🎓 SIU Admission Chatbot

A smart, AI-powered admission chatbot designed to assist prospective students of **Saigon International University (SIU)**. Powered by **Google Gemini Flash 2.0 API**, the system leverages **function calling**, **structured Markdown knowledge base**, and **Gradio UI** for seamless, scalable, and accurate information retrieval.

---

## 🚀 Features

- ✅ Understands natural language queries in Vietnamese.
- 🔍 Decomposes complex questions and finds the most relevant answer using a hierarchical search algorithm.
- 📂 Reads information from modular Markdown files stored in nested folders.
- 💬 Returns rewritten, human-readable answers via Gemini Flash 2.0.
- 🎛️ Easy to expand and maintain without technical expertise.

---

## 📸 UI Preview

![Chatbot Demo UI](path/to/your/screenshot.png)

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

## 📂 Knowledge Base Structure

The knowledge base is stored as a **tree-structured folder hierarchy** in Markdown format (`.md`). The chatbot searches top-down, starting from broad categories down to specific subfolders, until it locates the file that contains the relevant information.

Each `.md` file is editable by non-technical staff, making it ideal for maintaining up-to-date answers without modifying code.

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

> ✨ Tip: Just add more folders or `.md` files and the chatbot will pick them up automatically. No code changes needed.

---

## 🧠 How It Works

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
📁 project-root/
├── 📁 content/                  # Markdown knowledge base
├── 📄 main.py                  # Entry point for the chatbot
├── 📄 content_loader.py        # Loads and parses Markdown folders
├── 📄 file_searcher.py         # Recursive search logic
├── 📄 gradio_ui.py             # Gradio-based web UI
├── 📄 requirements.txt
└── 📄 README.md
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

## 🙏 Acknowledgements

This project is developed by the AI team of **Saigon International University (SIU)** for the 2025 enrollment season.

Powered by:

* Google Gemini Flash 2.0 API
* Gradio UI Framework
* Python 3.10
* Markdown for data transparency

---

## 📫 Contact

For questions, feedback, or collaborations, please contact the development team at:
📧 `ai.lab@siu.edu.vn`

---

```

---

Nếu bạn cần, mình có thể tạo sẵn luôn các file `main.py`, `content_loader.py`, `file_searcher.py`, và `gradio_ui.py` để chạy ngay. Bạn chỉ cần nói: **"tạo code luôn nhé!"**.
```

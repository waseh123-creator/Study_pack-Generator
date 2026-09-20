# 📚 AI Study Pack Generator

An AI-powered personalized study-pack generator built with **Python, Google Gemini, and Streamlit**.

The application uses a **multi-stage AI workflow** to transform a student's subject and topic into a structured study pack through planning, content generation, assessment, review, and final refinement.

---

## ✨ Features

* 📋 Personalized study-pack planning
* 🧠 AI-generated notes and explanations
* 🔑 Key concepts
* 🃏 Flashcards
* 📝 MCQs
* ❓ Short questions
* 📖 Long questions
* ✅ True / False questions
* 📅 Study plans
* 🎯 Beginner, Intermediate, and Advanced difficulty levels
* 🌐 English, Roman Urdu, and Urdu support
* 🔍 AI quality-review stage
* ✨ Final AI refinement stage
* ⚠️ Workflow-level error handling
* 🔐 Secure Gemini API key through Streamlit Secrets

---

## 🧠 AI Workflow

The application does not generate the entire study pack using a single prompt.

It uses a multi-stage workflow:

```text
Student Input
      ↓
┌─────────────────┐
│ 1. PLANNING     │
│ Learning goals  │
│ Objectives      │
│ Structure       │
└────────┬────────┘
         ↓
┌─────────────────┐
│ 2. CONTENT      │
│ Notes           │
│ Concepts        │
│ Flashcards      │
│ Study material  │
└────────┬────────┘
         ↓
┌─────────────────┐
│ 3. ASSESSMENT   │
│ MCQs            │
│ Questions       │
│ Answer keys     │
└────────┬────────┘
         ↓
┌─────────────────┐
│ 4. REVIEW       │
│ Accuracy        │
│ Relevance       │
│ Difficulty      │
│ Missing content │
└────────┬────────┘
         ↓
┌─────────────────┐
│ 5. REFINEMENT   │
│ Corrections     │
│ Final formatting│
│ Final study pack│
└─────────────────┘
```

Each stage receives relevant context from the previous stages.

This makes the generation process more controlled than a single AI prompt.

---

## 🏗️ Project Structure

```text
AI-Study-Pack-Generator/
│
├── app.py
├── workflow.py
├── prompts.py
├── requirements.txt
└── README.md
```

### `app.py`

Main Streamlit application.

Responsibilities:

* User interface
* Input collection
* Validation
* Gemini client initialization
* Workflow execution
* Result rendering

### `workflow.py`

Contains the multi-stage AI workflow.

Responsibilities:

* Planning
* Content generation
* Assessment
* Review
* Refinement
* Context passing
* Error handling

### `prompts.py`

Contains the prompts for each AI stage.

Responsibilities:

* Planning prompt
* Content-generation prompt
* Assessment prompt
* Review prompt
* Refinement prompt

### `requirements.txt`

Contains the Python dependencies required for deployment.

---

## 🛠️ Technologies

* **Python**
* **Streamlit**
* **Google Gemini API**
* **Google GenAI SDK**

---

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Study-Pack-Generator.git
```

```bash
cd AI-Study-Pack-Generator
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Gemini API Key

Create an environment variable:

```text
GEMINI_API_KEY=your_api_key_here
```

On Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

Alternatively, Streamlit Secrets can be used.

### 4. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

# ☁️ Deploy on Streamlit

## 1. Push the project to GitHub

Your repository should contain:

```text
app.py
workflow.py
prompts.py
requirements.txt
README.md
```

## 2. Open Streamlit Community Cloud

Create a new Streamlit application and select your GitHub repository.

Set the main file to:

```text
app.py
```

## 3. Add Gemini API Key

Open:

```text
App Settings → Secrets
```

Add:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
```

Save the secret.

## 4. Deploy

Streamlit will install the packages from:

```text
requirements.txt
```

and execute:

```bash
streamlit run app.py
```

---

## 🔐 Security

Never put your Gemini API key directly inside Python source code.

❌ Do not do:

```python
API_KEY = "AIza..."
```

Instead use an environment variable or Streamlit Secrets:

```text
GEMINI_API_KEY
```

Also never upload your API key to GitHub.

If an API key is accidentally exposed, revoke it and generate a new one.

---

## 🎓 Example

### Input

```text
Subject: Database Systems

Topic: Normalization

Level: Intermediate

Language: English

Components:
- Summary / Notes
- Key Concepts
- Flashcards
- MCQs
```

### Workflow

```text
Input
 ↓
Planning
 ↓
Content Generation
 ↓
Assessment
 ↓
AI Review
 ↓
Refinement
 ↓
Final Study Pack
```

### Output

The application produces a structured study pack containing the selected learning material and assessment questions.

---

## 🔮 Future Improvements

The architecture can be extended with:

* 📄 PDF upload
* 📑 DOCX upload
* 📚 Textbook processing
* 🎥 YouTube transcript processing
* 🧑‍🏫 AI tutor/chat
* 🧪 Exam mode
* 🎯 Quiz mode
* 📊 Student progress tracking
* 🔄 Spaced repetition
* 🃏 Interactive flashcards
* 📥 PDF export
* 📥 DOCX export
* 🤖 Multiple AI providers
* 👤 User accounts

---

## 📌 Architecture Philosophy

The project separates:

```text
UI
 ↓
Workflow
 ↓
Prompts
 ↓
AI Model
```

This makes the application easier to maintain and extend.

For example, additional AI workflow stages can be introduced without rewriting the entire Streamlit interface.

---

## 📄 License

This project is intended for educational and development purposes.

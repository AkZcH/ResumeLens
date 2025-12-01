# **ResumeLens — AI-Powered Resume Gap Analyzer**

## Table of Contents
- [Overview](#overview)
- [🚀 Features (MVP Scope)](#-features-mvp-scope)
- [📂 Project Structure](#-project-structure)
- [🛠 Tech Stack](#-tech-stack)
- [🔧 Setup Instructions](#-setup-instructions)
- [🔄 Development Workflow](#-development-workflow)
- [🧩 MVP Architecture Overview](#-mvp-architecture-overview)
- [🧪 Testing](#-testing)
- [🤝 Contributing](#-contributing)
- [👥 Team Roles](#-team-roles)
- [🔒 Security & Privacy](#-security--privacy)
- [📌 Project Status](#-project-status)

## Overview

ResumeLens is an AI-driven tool that analyzes a **resume + job description**, identifies **skill gaps**, highlights **missing keywords**, and suggests **bullet improvements, projects, and skills** to increase your chances of passing ATS filters and interviews.

The project combines NLP, embeddings, rule-based parsing, and LLM-based rewriting to deliver targeted, actionable resume suggestions.

---

## 🚀 **Features (MVP Scope)**

* Upload resume (PDF or text)
* Parse resume into structured data (skills, bullets, experience blocks)
* Extract keywords from a job description
* Identify missing skills, mismatches, and gaps
* Generate improved bullet points using an LLM
* Suggest relevant projects & skills to strengthen the resume
* Simple frontend UI to display suggestions

No unnecessary features, no bloat — just useful output.

---

## 📂 **Project Structure**

```
/backend
    /app            # FastAPI app
        main.py
    /services       # parsing, embedding, analysis logic
    /models         # pydantic schemas

/frontend
    /src            # React components

/parsers            # Resume/JD parsing logic
/nlp                # Embeddings, similarity, keyword extraction
/data               # Sample resumes & JDs (no sensitive data)
/docs               # One-pager, architecture notes, diagrams
/tests              # Unit tests
/scripts            # Helper scripts
.env.example        # Template env file
.gitignore
CODEOWNERS
CONTRIBUTING.md
README.md
```

---

## 🛠 **Tech Stack**

### **Backend**

* Python
* FastAPI
* Sentence-transformers (embeddings)
* spaCy + regex (parsing)
* FAISS (semantic search)
* OpenAI API (for bullet rewrites)

### **Frontend**

* React + Vite / CRA
* Tailwind (optional)

### **Storage**

* Local or S3 for file storage
* Postgres (optional for user data)

---

## 🔧 **Setup Instructions**

### **1. Clone the repo**

```
git clone https://github.com/<your-org>/ResumeLens.git
cd ResumeLens
```

### **2. Create dev branch (if not already)**

```
git checkout -b dev
```

### **3. Backend Setup**

```
cd backend
python -m venv env
source env/bin/activate   # Windows: env\Scripts\activate
pip install -r requirements.txt
```

Run backend:

```
uvicorn app.main:app --reload
```

### **4. Frontend Setup**

```
cd frontend
npm install
npm run dev
```

### **5. Environment Variables**

Copy the example file:

```
cp .env.example .env
```

Fill in:

```
OPENAI_API_KEY=
DATABASE_URL=
SECRET_KEY=
```

Never commit actual keys.

---

## 🔄 **Development Workflow**

We follow a clean and strict Git workflow.

### **Branches**

* `main` → stable, protected
* `dev` → active development
* `feature/*` → per-task branches

### **Rules**

* Never push directly to `main`
* Always create a feature branch:

  ```
  git checkout -b feature/parser-improvements
  ```
* Make PR → merge into `dev`
* Only merge `dev` → `main` for releases

---

## 🧩 **MVP Architecture Overview**

**1) Resume Parser**

* Extracts raw text from PDF
* Identifies skills, experience blocks, metrics, technologies

**2) JD Parser**

* Extracts required skills, tools, responsibilities

**3) Embedding + Similarity Engine**

* Converts skills/bullets → embeddings
* Finds semantic matches and gaps

**4) Gap Analyzer**

* Compares resume vs JD
* Lists missing keywords
* Scores alignment

**5) LLM Generator**

* Rewrites bullet points
* Suggests new projects
* Improves phrasing + metrics

**6) Frontend UI**

* Upload files
* Display suggestions cleanly

---

## 🧪 **Testing**

Tests are located in `/tests`.

Run backend tests:

```
pytest
```

---

## 🤝 **Contributing**

### **1. Create a branch**

```
git checkout -b feature/<name>
```

### **2. Write clear, meaningful commits**

Avoid noisy commits.

### **3. Make a PR to `dev`**

Another team member must review.

### **4. Follow code style**

* Keep functions small
* Document tricky logic
* Don't push secrets

For full details, see `CONTRIBUTING.md`.

---

## 👥 **Team Roles**

Assign these clearly to avoid overlap:

* **Team Lead:** Project direction, architecture, integration
* **ML/NLP Engineer:** Embeddings, similarity, parsing
* **Backend Engineer:** API, routing, models
* **Frontend Engineer:** UI, user experience
* **DevOps:** env setup, repo structure
* **QA:** test dataset, validations
* **Docs/Prompts:** prompt engineering & documentation

---

## 🔒 **Security & Privacy**

* Do NOT store sensitive resumes without explicit permission
* Delete uploaded resumes after analysis
* Do not log raw resume content
* Environment variables stay local

---

## 📌 **Project Status**

MVP development phase underway.

---

If you want, I can also generate:
✅ 1-page product spec
✅ `CONTRIBUTING.md` file
✅ `CODEOWNERS` file
✅ `.gitignore`
Just tell me.
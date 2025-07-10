# 🌟 AshAI

**AshAI** is a full-stack SSC Question App powered by AI, built using:
- **Frontend**: HTML, CSS, JavaScript  
- **Backend**: FastAPI + SQLModel + SQLite  
- **AI**: Deep Learning for smart answer explanations and difficulty prediction

---

## 🚀 Features

- SSC MCQ Question Bank  
- Instant answer evaluation  
- AI-generated explanations  
- Difficulty level prediction (Easy/Medium/Hard)  
- Responsive UI  
- FastAPI backend with REST APIs  

---

## 📁 Project Structure
AshAI/
├── backend/
│ ├── main.py # FastAPI routes
│ ├── db.py # Database models (SQLModel)
│ ├── model.py # AI logic (mock/demo)
│ └── questions.db # SQLite database
├── frontend/
│ ├── index.html # Main UI
│ ├── styles.css # CSS
│ └── script.js # JS for API calls
└── requirements.txt # Python dependencies

---

## ⚙️ Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run backend
cd backend
uvicorn main:app --reload

# 3. Open frontend in browser
Open frontend/index.html (Use Live Server for best results)


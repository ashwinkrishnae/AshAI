
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from model import get_explanation, predict_difficulty
import httpx
import random


app = FastAPI()


# Helper function to shuffle options
def shuffle_options(options):
    random.shuffle(options)
    return options

# Quantitative Aptitude (Math) - the-trivia-api.com, fallback to OpenTDB Mathematics
@app.get("/fetch_quant_questions")
async def fetch_quant_questions(time_per_question: int = 1):
    total_time = 60
    amount = total_time // time_per_question
    amount = max(1, min(amount, 50))
    try:
        url = f"https://the-trivia-api.com/api/questions?categories=mathematics&limit={amount}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                formatted = []
                for idx, item in enumerate(data):
                    options = shuffle_options(item.get("incorrectAnswers", []) + [item.get("correctAnswer", "")])
                    formatted.append({
                        "id": idx,
                        "question": item.get("question", ""),
                        "options": options,
                        "answer": item.get("correctAnswer", ""),
                        "category": item.get("category", "Mathematics"),
                        "source": "the-trivia-api.com"
                    })
                if formatted:
                    return formatted
    except Exception:
        pass
    # Fallback to OpenTDB Mathematics
    url = f"https://opentdb.com/api.php?amount={amount}&category=19&type=multiple"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Failed to fetch questions from external API.")
        data = response.json()
        formatted = []
        for idx, item in enumerate(data.get("results", [])):
            options = shuffle_options(item["incorrect_answers"] + [item["correct_answer"]])
            formatted.append({
                "id": idx,
                "question": item["question"],
                "options": options,
                "answer": item["correct_answer"],
                "category": item.get("category", "Mathematics"),
                "source": "opentdb.com"
            })
        return formatted

# Computer Knowledge - OpenTDB Computers category
@app.get("/fetch_computer_questions")
async def fetch_computer_questions(time_per_question: int = 1):
    total_time = 60
    amount = total_time // time_per_question
    amount = max(1, min(amount, 50))
    url = f"https://opentdb.com/api.php?amount={amount}&category=18&type=multiple"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Failed to fetch questions from external API.")
        data = response.json()
        formatted = []
        for idx, item in enumerate(data.get("results", [])):
            options = shuffle_options(item["incorrect_answers"] + [item["correct_answer"]])
            formatted.append({
                "id": idx,
                "question": item["question"],
                "options": options,
                "answer": item["correct_answer"],
                "category": item.get("category", "Computers"),
                "source": "opentdb.com"
            })
        return formatted

# English - OpenTDB General Knowledge (labeled as English)
@app.get("/fetch_english_questions")
async def fetch_english_questions(time_per_question: int = 1):
    total_time = 60
    amount = total_time // time_per_question
    amount = max(1, min(amount, 50))
    url = f"https://opentdb.com/api.php?amount={amount}&category=9&type=multiple"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Failed to fetch questions from external API.")
        data = response.json()
        formatted = []
        for idx, item in enumerate(data.get("results", [])):
            options = shuffle_options(item["incorrect_answers"] + [item["correct_answer"]])
            formatted.append({
                "id": idx,
                "question": item["question"],
                "options": options,
                "answer": item["correct_answer"],
                "category": "English",
                "source": "opentdb.com"
            })
        return formatted

# Mathematics (separate from Quantitative) - OpenTDB Mathematics
@app.get("/fetch_mathematics_questions")
async def fetch_mathematics_questions(time_per_question: int = 1):
    total_time = 60
    amount = total_time // time_per_question
    amount = max(1, min(amount, 50))
    url = f"https://opentdb.com/api.php?amount={amount}&category=19&type=multiple"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Failed to fetch questions from external API.")
        data = response.json()
        formatted = []
        for idx, item in enumerate(data.get("results", [])):
            options = shuffle_options(item["incorrect_answers"] + [item["correct_answer"]])
            formatted.append({
                "id": idx,
                "question": item["question"],
                "options": options,
                "answer": item["correct_answer"],
                "category": item.get("category", "Mathematics"),
                "source": "opentdb.com"
            })
        return formatted

# Reasoning - Trivia API (Logic), fallback to OpenTDB General Knowledge, labeled as Reasoning
@app.get("/fetch_reasoning_questions")
async def fetch_reasoning_questions(time_per_question: int = 1):
    total_time = 60
    amount = total_time // time_per_question
    amount = max(1, min(amount, 50))
    # Try the-trivia-api.com Logic category
    try:
        url = f"https://the-trivia-api.com/api/questions?categories=logic&limit={amount}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                formatted = []
                for idx, item in enumerate(data):
                    options = shuffle_options(item.get("incorrectAnswers", []) + [item.get("correctAnswer", "")])
                    formatted.append({
                        "id": idx,
                        "question": item.get("question", ""),
                        "options": options,
                        "answer": item.get("correctAnswer", ""),
                        "category": "Reasoning",
                        "source": "the-trivia-api.com"
                    })
                if formatted:
                    return formatted
    except Exception:
        pass
    # Fallback to OpenTDB General Knowledge, labeled as Reasoning
    url = f"https://opentdb.com/api.php?amount={amount}&category=9&type=multiple"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Failed to fetch questions from external API.")
        data = response.json()
        formatted = []
        for idx, item in enumerate(data.get("results", [])):
            options = shuffle_options(item["incorrect_answers"] + [item["correct_answer"]])
            formatted.append({
                "id": idx,
                "question": item["question"],
                "options": options,
                "answer": item["correct_answer"],
                "category": "Reasoning",
                "source": "opentdb.com"
            })
        return formatted

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load questions
with open("questions.json") as f:
    questions = json.load(f)

@app.get("/questions")
def get_questions():
    return questions

@app.post("/submit")
def submit_answer(qid: int, user_answer: str):
    correct = questions[qid]["answer"]
    return {
        "correct": user_answer == correct,
        "explanation": get_explanation(questions[qid]["question"]),
        "difficulty": predict_difficulty(questions[qid]["question"])
    }

# New endpoint to fetch questions from the internet for a 1-hour slot
@app.get("/fetch_external_questions")
async def fetch_external_questions(time_per_question: int = 1):
    """
    Fetches questions for a 1-hour slot. time_per_question is in minutes (default 1).
    """
    total_time = 60  # minutes in 1 hour
    amount = total_time // time_per_question
    if amount < 1:
        amount = 1
    if amount > 50:
        amount = 50  # OpenTDB API max limit per call
    url = f"https://opentdb.com/api.php?amount={amount}&type=multiple"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Failed to fetch questions from external API.")
        data = response.json()
        # Format the questions to match your internal structure
        formatted = []
        for idx, item in enumerate(data.get("results", [])):
            options = item["incorrect_answers"] + [item["correct_answer"]]
            # Shuffle options for randomness
            import random
            random.shuffle(options)
            formatted.append({
                "id": idx,
                "question": item["question"],
                "options": options,
                "answer": item["correct_answer"]
            })
        return formatted

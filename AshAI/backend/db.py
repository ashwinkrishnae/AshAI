from sqlmodel import Field, SQLModel, Session, create_engine, select

# Define the Question model
class Question(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    question: str
    option1: str
    option2: str
    option3: str
    option4: str
    answer: str

# Create SQLite engine
DATABASE_URL = "sqlite:///./questions.db"
engine = create_engine(DATABASE_URL, echo=True)

# Create DB and tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Add initial questions
def insert_sample_questions():
    with Session(engine) as session:
        if not session.exec(select(Question)).first():  # Avoid duplicate insert
            q1 = Question(
                question="What is the capital of India?",
                option1="Mumbai",
                option2="New Delhi",
                option3="Chennai",
                option4="Kolkata",
                answer="New Delhi"
            )
            q2 = Question(
                question="Who is the first President of India?",
                option1="Mahatma Gandhi",
                option2="Narendra Modi",
                option3="Dr. Rajendra Prasad",
                option4="APJ Abdul Kalam",
                answer="Dr. Rajendra Prasad"
            )
            session.add_all([q1, q2])
            session.commit()

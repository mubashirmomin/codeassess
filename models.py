from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="candidate") # Roles: 'admin' or 'candidate'

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(String, nullable=False)
    time_limit = Column(Integer, nullable=False)
    memory_limit = Column(Integer, nullable=False)

    # The relationship to fetch all linked test cases
    test_cases = relationship("TestCase", back_populates="question", cascade="all, delete-orphan")

class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)
    # The Foreign Key links this row to a specific question ID
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    input_data = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)
    is_hidden = Column(Boolean, default=True)

    # The relationship back to the parent question
    question = relationship("Question", back_populates="test_cases")

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    # Link to the question being answered
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    # Link to the user who wrote the code
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    language = Column(String, nullable=False)
    source_code = Column(Text, nullable=False)
    status = Column(String, default="Pending") # Statuses: Pending, Passed, Failed, Error

    # SQLAlchemy relationships for easy data fetching
    question = relationship("Question")
    user = relationship("User")
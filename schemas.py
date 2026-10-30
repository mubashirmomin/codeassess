from pydantic import BaseModel

# 1. The data we EXPECT FROM the client when creating a question
class QuestionCreate(BaseModel):
    title: str
    description: str
    difficulty: str
    time_limit: int
    memory_limit: int

# 2. The data we RETURN TO the client
class QuestionResponse(BaseModel):
    id: int
    title: str
    description: str
    difficulty: str
    time_limit: int
    memory_limit: int

    class Config:
        from_attributes = True

class SubmissionCreate(BaseModel):
    language: str
    source_code: str

class SubmissionResponse(BaseModel):
    id: int
    question_id: int
    user_id: int
    language: str
    source_code: str
    status: str

    class Config:
        from_attributes = True

class TestCaseCreate(BaseModel):
    input_data: str
    expected_output: str
    is_hidden: bool

class TestCaseResponse(BaseModel):
    id: int
    question_id: int
    input_data: str
    expected_output: str
    is_hidden: bool

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import database
import models
import schemas
import security
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import HTTPException, status
import jwt

# 1. Create all tables in the database (SQLite for now)
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# 2. Dependency: Get a database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db  # Hands the session to the endpoint
    finally:
        db.close()  # Ensures the connection closes after the request finishes

# 1. Define the security scheme and point it to our login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 2. Dependency: Get the currently authenticated user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the token using the secret key from security.py
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise credentials_exception
    
    # Fetch the user from the database
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
        
    return user

# 3. Dependency: Enforce Admin Role
def get_current_admin_user(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return current_user

# 3. Create a Question Endpoint (Admin Only)
@app.post("/questions/", response_model=schemas.QuestionResponse)
def create_question(
    question: schemas.QuestionCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)  # This locks the route!
):
    # Create the SQLAlchemy model instance
    db_question = models.Question(
        title=question.title,
        description=question.description,
        difficulty=question.difficulty,
        time_limit=question.time_limit,
        memory_limit=question.memory_limit
    )
    
    # Save it to the database
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    
    return db_question

# 4. Read All Questions Endpoint
@app.get("/questions/", response_model=list[schemas.QuestionResponse])
def read_questions(db: Session = Depends(get_db)):
    # Fetch all records from the questions table
    questions = db.query(models.Question).all()
    return questions

# 5. Create a Test Case for a specific Question
@app.post("/questions/{question_id}/testcases/", response_model=schemas.TestCaseResponse)
def create_test_case(question_id: int, testcase: schemas.TestCaseCreate, db: Session = Depends(get_db)):
    # 1. Check if the question actually exists
    db_question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not db_question:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Question not found")

    # 2. Create the test case and link it using the question_id from the URL
    db_testcase = models.TestCase(
        question_id=question_id,
        input_data=testcase.input_data,
        expected_output=testcase.expected_output,
        is_hidden=testcase.is_hidden
    )
    
    # 3. Save to the database
    db.add(db_testcase)
    db.commit()
    db.refresh(db_testcase)
    
    return db_testcase

@app.post("/users/", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Hash the plain text password
    hashed_pwd = security.get_password_hash(user.password)
    
    # 2. Create the database object with the hashed password
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pwd
    )
    
    # 3. Save to the database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Find the user by username
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    # 2. Check if user exists and password matches
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    # 3. Generate the VIP wristband (JWT)
    access_token = security.create_access_token(data={"sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user
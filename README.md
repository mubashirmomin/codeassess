CodeAssess Backend API 🚀

CodeAssess is a secure, containerized REST API backend for a coding assessment platform (similar to LeetCode or HackerRank). It allows administrators to create coding challenges and automatically grades code submitted by candidates by executing it in a secure, isolated sandbox environment.

✨ Features

Role-Based Access Control (RBAC): Built-in "admin" and "candidate" roles. Only admins can create questions and test cases.

Stateless Authentication: Secure login and session management using JSON Web Tokens (JWT) and bcrypt password hashing.

Automated Code Evaluation: A custom execution engine that runs candidate Python code against hidden test cases.

Secure Sandboxing: The entire application runs inside Docker containers, preventing Remote Code Execution (RCE) attacks from affecting the host machine.

Relational Database: Fully integrated PostgreSQL database managed via SQLAlchemy ORM.

🛠️ Tech Stack

Framework: FastAPI (Python)

Database: PostgreSQL

ORM & Validation: SQLAlchemy, Pydantic

Security: PyJWT, passlib (bcrypt)

Infrastructure: Docker, Docker Compose

📋 Prerequisites

To run this project, you will need the following installed on your machine:

Docker Desktop (Make sure the Docker engine is running)

Git

🚀 Local Setup & Installation

1. Clone the repository

git clone https://github.com/yourusername/codeassess.git
cd codeassess


2. Start the Application via Docker
Build and start the multi-container architecture (API + PostgreSQL database):

docker compose up --build


3. Access the API Documentation
Once the containers are running, FastAPI automatically generates an interactive Swagger UI. Open your browser and navigate to:

Swagger UI: http://localhost:8000/docs

👑 Creating an Admin User

By default, all new users are registered as candidates. To create your first admin user:

Go to http://localhost:8000/docs and create a user via the POST /users/ endpoint (e.g., username: admin1).

Open a separate terminal in the project folder and run the promotion script (requires local Python environment):

python promote.py


You can now log in via the Swagger UI authorization padlock to access admin-only endpoints.

📖 API Endpoints Summary

Authentication & Users

POST /users/ - Register a new user (Candidate).

POST /login - Authenticate and receive a JWT.

GET /users/me - View current user profile.

Questions & Test Cases

GET /questions/ - List all coding challenges.

POST /questions/ - Create a new challenge (Admin only).

POST /questions/{question_id}/testcases/ - Add a test case to a challenge (Admin only).

Submissions

POST /questions/{question_id}/submissions/ - Submit source code for evaluation. Returns a status of Passed, Failed, or Time Limit Exceeded.

🔒 Security Note

This project evaluates arbitrary code inside a Docker container. While containerization provides a strong layer of isolation against host-level RCE, deploying this to a public production environment would require additional security layers (e.g., dropping network privileges, setting strict memory/CPU limits, and running a secondary rootless sandbox like gVisor).

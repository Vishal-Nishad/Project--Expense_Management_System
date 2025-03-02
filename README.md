# Expense Management System:

This project is an expense management system that consists of a Streamlit frontend application and a FastAPI backend server.


## Project Structure:

- **frontend/**: Contains the Streamlit application code.
- **backend/**: Contains the FastAPI backend server code.
- **tests/**: Contains the test cases for both frontend and backend.
- **requirements.txt**: Lists the required Python packages.
- **README.md**: Provides an overview and instructions for the project.

## How it Works:
- 1️⃣ The **Streamlit app** allows users to enter, update, and view expenses.
- 2️⃣ The **FastAPI server** processes these requests, fetching or updating data.
- 3️⃣ The **MySQL database** stores expenses, accessed via **PyMySQL**.
- 4️⃣ Integration is done using **REST APIs,** with requests handling communication between frontend and backend.

This architecture ensures **modularity, scalability, and efficient data management.**

## Setup Instructions:

1. **Install dependencies:**:   
   ```commandline
    pip install -r requirements.txt
   ```
1. **Run the FastAPI server:**:   
   ```commandline
    uvicorn server.server:app --reload
   ```
1. **Run the Streamlit app:**:   
   ```commandline
    streamlit run frontend/app.py
   ```
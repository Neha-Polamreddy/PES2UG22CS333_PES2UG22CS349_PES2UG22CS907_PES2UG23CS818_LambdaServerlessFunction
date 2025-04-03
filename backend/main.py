from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Serverless Function Execution Platform Running"}

# Run the server: uvicorn main:app --host 0.0.0.0 --port 8000


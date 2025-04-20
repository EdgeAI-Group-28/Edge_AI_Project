from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess



app = FastAPI()


origins = [
    "http://localhost:8000",
	"http://localhost:5173",
  # React dev server origin
   # You can add your deployed frontend domain here too if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Or ["*"] to allow all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class Data(BaseModel):
	command : str



@app.get("/")
def read_root():
	return {"message": "Hello, FastAPI!"}


@app.post("/execute")
def submitData(data: Data):
    command = data.command
    print(f"Received command to run: {command}")

    try:
        # Execute the command and capture output and errors
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=10
        )
        
        output = result.stdout
        error = result.stderr

        return {
            "message": "Command executed",
            "output": output,
            "error": error,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"message": "Command timed out"}
    except Exception as e:
        return {"message": f"Error running command: {str(e)}"}


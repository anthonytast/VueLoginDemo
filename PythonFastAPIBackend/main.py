import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routers import users

app = FastAPI(title="Vue Login API")

app.include_router(users.router)

# @app.get("/")
# def return_server_status():
#     return "Server is running..."

# origins = [
#     "http://127.0.0.1:8500" # url used for running Vue server
# ]

app.add_middleware(
    CORSMiddleware, # CORS - cross origin resource sharing
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000) # localhost
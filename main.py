from fastapi import FastAPI
from api import employees, burnout, wellness, environmental, productivity, audio, test, keyboard,get_images, get_audio
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ESG Workforce Wellbeing Agent", version="1.0")

origins = [
    "http://localhost:5173", 
    "http://127.0.0.1:5173",
    "http://172.25.5.86:5173/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employees.router, prefix="/api", tags=["Employees"])
app.include_router(productivity.router, prefix="/api", tags=["productivity"])
app.include_router(burnout.router, prefix="/api", tags=["Burnout"])
app.include_router(wellness.router, prefix="/api", tags=["Wellness"])
app.include_router(get_images.router, prefix="/api", tags=["get images"])
app.include_router(environmental.router, prefix="/api", tags=["environmental"])
app.include_router(audio.router, prefix="/api", tags=["Audio analysis"])
app.include_router(keyboard.router, prefix="/api", tags=["keyboard behaviour analysis"])
app.include_router(get_audio.router, prefix="/api", tags=["get audio"])
# app.include_router(test.router, prefix="/api", tags=["image emtion test"])


@app.get("/")
def read_root():
    return {"message": "Welcome to ESG Workforce Wellbeing API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
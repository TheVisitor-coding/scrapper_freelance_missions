from fastapi import FastAPI
from routes import route_job

app = FastAPI()

app.include_router(route_job.router)

@app.get('/')
async def root():
    return {'Helllo'}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
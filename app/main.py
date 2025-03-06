from fastapi import FastAPI
from routes import product

app = FastAPI()

app.include_router(product.router)

@app.get('/')
async def root():
    return {'Helllo'}
from fastapi import FastAPI

# python3 -m uvicorn main:app --reload

app = FastAPI()

@app.get('/')
def root() :
    return { 'title': '日拱一卒' }
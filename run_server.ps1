# Mở Python interactive
python

# Sau đó gõ từng dòng:
>>> from fastapi import FastAPI
>>> import uvicorn
>>> app = FastAPI()
>>> @app.get("/")
... def root():
...     return {"message": "OK"}
... 
>>> uvicorn.run(app, port=8000)
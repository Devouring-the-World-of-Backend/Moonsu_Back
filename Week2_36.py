from fastapi import FastAPI

app = FastAPI()


@app.get("/book")
def read_book():
    return {"message": f"Hello, Library!"}

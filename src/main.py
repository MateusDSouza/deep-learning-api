from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import tasks

app = FastAPI()

languages = ["English", "French", "German", "Romanian"]


class Translation(BaseModel):
    text: str
    base_language: str
    final_language: str


@app.get("/")
def get_root():
    return {"message": "Hello World!"}


@app.post("/translate")
def post_translation(t: Translation, background_tasks: BackgroundTasks):
    t_id = tasks.store_translation(t)
    background_tasks.add_task(tasks.run_translation(t_id))  # type: ignore
    return {"task_id": t_id}


@app.get("/results")
def get_translation(t_id: int):
    return {"translation": tasks.find_translation(t_id)}

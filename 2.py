from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# ------------------ MODEL ------------------
class Task(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "pending"   # pending / completed
    priority: int             # 1 (high) → 5 (low)


# ------------------ DATABASE ------------------
tasks = []


# ------------------ CREATE ------------------
@app.post("/tasks")
def create_task(task: Task):
    new_task = {
        "id": len(tasks) + 1,
        **task.dict()
    }
    tasks.append(new_task)
    return {"message": "Task created", "data": new_task}


# ------------------ READ ALL (with filters) ------------------
@app.get("/tasks")
def get_tasks(
    status: Optional[str] = None,
    priority: Optional[int] = None
):
    result = tasks

    if status:
        result = [t for t in result if t["status"] == status]

    if priority:
        result = [t for t in result if t["priority"] == priority]

    return {"count": len(result), "data": result}


# ------------------ READ ONE ------------------
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


# ------------------ UPDATE ------------------
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks[i] = {
                "id": task_id,
                **updated_task.dict()
            }
            return {"message": "Task updated", "data": tasks[i]}
    
    raise HTTPException(status_code=404, detail="Task not found")


# ------------------ DELETE ------------------
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted = tasks.pop(i)
            return {"message": "Task deleted", "data": deleted}
    
    raise HTTPException(status_code=404, detail="Task not found")


# ------------------ ROOT ------------------
@app.get("/")
def home():
    return {"message": "Task API running 🚀"}
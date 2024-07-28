from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4, UUID

app = FastAPI()

class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4, alias="id")
    title: str = Field(..., title="Title of the task", max_length=100)
    description: str = Field(..., title="Description of the task", max_length=500)
    completed: bool = Field(default=False, title="Status of the task")

# In-memory storage for tasks
tasks = []

@app.get("/tasks", response_model=List[Task])
async def get_tasks() -> List[Task]:
    """
    Retrieve all tasks.
    """
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: UUID) -> Task:
    """
    Retrieve a task by its ID.
    """
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task: Task) -> Task:
    """
    Create a new task.
    """
    tasks.append(task)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: UUID, task_data: Task) -> Task:
    """
    Update an existing task by its ID.
    """
    for index, task in enumerate(tasks):
        if task.id == task_id:
            updated_task = task_data.copy(update={"id": task_id})
            tasks[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: UUID):
    """
    Delete a task by its ID.
    """
    for index, task in enumerate(tasks):
        if task.id == task_id:
            del tasks[index]
            return
    raise HTTPException(status_code=404, detail="Task not found")
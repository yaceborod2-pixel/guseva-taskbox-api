from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="TaskBox API")

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3)
    description: str | None = None
    priority: int = Field(default=3, ge=1, le=5)

class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=3)
    description: str | None = None
    completed: bool | None = None
    priority: int | None = Field(None, ge=1, le=5)

class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool = False
    priority: int = 3

tasks = {}
next_id = 1

@app.get("/")
def read_root():
    return {"service": "TaskBox API", "status": "working"}

@app.get("/health")
def health_check():
    return {"status": "OK"}

@app.get("/stats")
def get_stats():
    total = len(tasks)
    completed = sum(1 for task in tasks.values() if task.completed)
    pending = total - completed
    return {"total": total, "completed": completed, "pending": pending}

@app.get("/tasks", response_model=list[Task])
def list_tasks(completed: bool | None = None, search: str | None = None):
    results = list(tasks.values())
    
    if search is not None:
        search_lower = search.lower()
        results = [t for t in results if search_lower in t.title.lower()]
        
    if completed is not None:
        results = [t for t in results if t.completed == completed]
        
    return results

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate):
    global next_id
    task = Task(
        id=next_id,
        title=data.title,
        description=data.description,
        priority=data.priority
    )
    tasks[next_id] = task
    next_id += 1
    return task

@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, data: TaskUpdate):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    current_task = tasks[task_id]
    changes = data.model_dump(exclude_unset=True, exclude_none=True)
    
    updated_task = current_task.model_copy(update=changes)
    tasks[task_id] = updated_task
    return updated_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
    return

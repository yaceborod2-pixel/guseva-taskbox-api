from fastapi import FastAPI, HTTPException, status

users = [
    {
        "name": "Garfield",
        "age": 8
    },
    {
        "name":"Petter",
        "age": 16
    }
]

app = FastAPI(title="TaskBox API")

@app.get("/users")
def get_users():
    return {
        "users" : users
    }

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id < 0 or user_id >= len(users):
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "users": users
    }

@app.delete("/users/{user_id}")
def get_user(user_id: int):
    if user_id < 0 or user_id >= len(users):
        raise HTTPException(status_code=404, detail="User not found")
    
    users.pop(user_id)

    return status.HTTP_204_NO_CONTENT


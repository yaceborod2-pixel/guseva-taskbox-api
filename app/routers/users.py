from fastapi import APIRouter

router = APIRouter(
        prefix = "/users",
        tags = "Users"
)

@router.get("/users")
def get_users():
    return {
        "users": users
    }

@router.get("/users")
def get_users():
    return {
        "users": users
    }
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get("/")
def get_users():
    return [{"id": 1, "username": "alice"}, {"id": 2, "username": "bob"}]

@router.get("/{user_id}")
def get_user(user_id: int):
    if user_id > 2:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id, "username": "alice"}
from fastapi import APIRouter

router = APIRouter()


@router.post("/{name}")
async def update_admin(name: str):
    return {"message": f"Admin name changed to {name}"}
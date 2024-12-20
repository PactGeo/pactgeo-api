from fastapi import APIRouter, Depends
from api.public.user.models import User
from api.auth import authenticate_github, authenticate_google
from api.public.dependencies import get_current_user

router = APIRouter()

@router.post("/google")
async def google_auth(token: str = Depends(authenticate_google)):
    print('======= github_google =======')
    print('token:', token)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/github")
async def github_auth(token: str = Depends(authenticate_github)):
    print('======= github_auth =======')
    print('token:', token)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/protected-route")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hola, {current_user.username}"}
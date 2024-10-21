import secrets
from datetime import datetime, timedelta, timezone
import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session, select
from api.config import settings
from api.public.user.models import User, Accounts
from api.database import get_session

SECRET_KEY = settings.JWT_SECRET
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def is_username_available(username: str, session: Session):
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    return user is None

def generate_unique_username(base_username: str, session: Session):
    counter = 1
    new_username = base_username
    while not is_username_available(new_username, session):
        new_username = f"{base_username}{counter}"
        counter += 1
    return new_username

async def validate_github_token(token: str):
    print('======= validate_github_token =======')
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"token {token}"}
        print('headers:', headers)
        print('token:', token)
        response = await client.get("https://api.github.com/user", headers=headers)
        print('response: ', response)
        if response.status_code == 200:
            return response.json()
        return None

async def get_github_email(token: str):
    async with httpx.AsyncClient() as client:
        headers = {'Authorization': f'token {token}'}
        response = await client.get('https://api.github.com/user/emails', headers=headers)
        if response.status_code != 200:
            return None
        emails = response.json()
        # Buscar el email principal
        primary_emails = [email for email in emails if email.get('primary') and email.get('verified')]
        if primary_emails:
            return primary_emails[0]['email']
        return None
    
async def get_or_create_user(github_user: dict, session: Session):
    # 1. Buscar si existe una Account con el provider y provider_account_id
    statement = select(Accounts).where(
        Accounts.provider == "github",
        Accounts.provider_account_id == str(github_user["id"])
    )
    account = session.exec(statement).first()

    if account:
        # Si la cuenta existe, obtener el usuario asociado
        return account.user

    # 2. Si no existe la Account, buscar un User por email
    email = github_user.get("email")
    if email:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
    else:
        user = None

    if not user:
        # 3. Si no existe el User, crearlo
        username = github_user["login"]
        if not await is_username_available(username, session):
            username = generate_unique_username(username, session)

        user = User(
            username=username,
            email=email,
            name=github_user.get("name"),
            # Otros campos...
        )
        session.add(user)
        session.commit()
        session.refresh(user)

    # 4. Crear la nueva Account y asociarla al User
    new_account = Accounts(
        user_id=user.id,
        type="oauth",
        provider="github",
        provider_account_id=str(github_user["id"]),
        # Otros campos...
    )
    session.add(new_account)
    session.commit()
    session.refresh(new_account)

    return user

async def authenticate_github(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    github_user = await validate_github_token(token)
    if not github_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid GitHub token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    email = await get_github_email(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No email associated with this GitHub account.",
        )
    github_user['email'] = email
    user = await get_or_create_user(github_user, session)
    access_token = create_access_token(data={"test":"foo", "sub": str(user.id)})
    return access_token

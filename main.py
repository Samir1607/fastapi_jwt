from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import engine, get_db
import models, schemas, auth


#Run the database migrations
models.Base.metadata.create_all(bind=engine)

#Initialize the FastAPI app
app=FastAPI()


#Define the OAuth2 scheme for token-based authentication 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/register", response_model=schemas.User)
async def register_user(user:schemas.UserCreate, db:Session=Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username==user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="username already exist...!")
    hashed_password=auth.get_password_hash(user.password)
    new_user=models.User(username=user.username, email= user.email, hash_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.username==form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate":"Bearer"}
        )
    access_token=auth.create_access_token(data={"sub":user.username})
    refresh_token = auth.create_refresh_token(data={"sub": user.username})
    return {"access_token":access_token, "token_type":"bearer", "refresh_token":refresh_token}


async def get_current_user(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    username=auth.verify_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate":"Bearer"}
        )
    
    user=db.query(models.User).filter(models.User.username==username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user:models.User=Depends(get_current_user)):
    return current_user

from fastapi import Depends, FastAPI, HTTPException, UploadFile, File, Form, status
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import uvicorn

from . import schemas, controllers, models, utils
from .database import engine

ACCESS_TOKEN_EXPIRE_MINUTES = 30

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount('/files', StaticFiles(directory="app/uploads"), name="files")


@app.get('/')
async def default():
    return {
        'api': 'Posts API',
        'version': 'v1.0.0',
        'author': 'David Vietle'
    }
# AUTHENTICATION ROUTES
# Login
@app.post("/login", response_model=schemas.Token)
async def login_for_access_tokenin(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(utils.get_db),
):
    user = utils.authenticate_user(db, email, password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    #fix login bug

    access_token = utils.create_access_token({"sub": str(user.get("id"))})
    return {"access_token": access_token, "token_type": "Bearer"}


# Logout
@app.post('/logout')
def log_out():
    #fix the log out error
    return True


# USER ROUTES
# Create User
@app.post("/users", response_model=schemas.UserOut)
async def create_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    avatar: UploadFile = File(...),
    db: Session = Depends(utils.get_db),
):
    db_user = controllers.get_user_by_email(db, email=email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await controllers.create_user(db, username, email, password, avatar)


# Read many users
@app.get("/users", response_model=list[schemas.UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(utils.get_db)):
    users = controllers.get_users(db, skip=skip, limit=limit)
    return users


# Read user
@app.get("/users/{id}", response_model=schemas.UserOut)
def read_user(id: int, db: Session = Depends(utils.get_db)):
    db_user = controllers.get_user(db, user_id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Change password
@app.patch("/users/{id}/change-password")
def change_password(
    id: int, db: Session = Depends(utils.get_db), new_password: str | None = None
):
    db_user = controllers.get_user(db=db, user_id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return controllers.change_password(db=db, user_id=id, new_password=new_password)


# Change profile
@app.patch("/users/{id}/change-profile")
def update_profile(
    user: schemas.UserIn,
    db: Session = Depends(utils.get_db),
    new_password: str | None = None,
):
    db_user = controllers.get_user_by_email(db=db, email=user.email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return controllers.update_profile(db=db, user=user)


# PRODUCT ROUTES
# Create post
@app.post("/posts", response_model=schemas.PostOut)
def create_post(post: schemas.PostIn, db: Session = Depends(utils.get_db), current_user: int = Depends(utils.get_current_user)):
    return controllers.create_post(db=db, post=post, current_user=current_user)


# Get many products
@app.get("/posts", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(utils.get_db), skip: int = 0, limit: int = 100):
    db_posts = controllers.get_posts(db=db, skip=skip, limit=limit)
    return db_posts


# Update post
@app.put("/posts/{id}", response_model=schemas.PostOut)
def update_post(post: schemas.PostIn, id: int, db: Session = Depends(utils.get_db)):
    db_post = controllers.get_post(db, post_id=id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Can't update empty post")
    else:
        return controllers.update_post(db, post, post_id=id)

# Like post
@app.put("/posts/{id}/like")
def like_post(id: int, user_id: int, db: Session = Depends(utils.get_db)):
    db_post = controllers.like_post(db, id, user_id)
    return db_post


# Delete post
@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(utils.get_db)):
    db_post = controllers.get_post(db, post_id=id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Can't delete empty post")
    else:
        return controllers.delete_post(db, id)

# For  debugging with breakpoint in vscode
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port='8000')

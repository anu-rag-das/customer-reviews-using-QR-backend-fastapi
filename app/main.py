from fastapi import FastAPI
from app.routes import user, auth, business
from app.config import models
from app.config.db import engine
from fastapi.middleware.cors import CORSMiddleware

#creating database
models.Base.metadata.create_all(bind=engine)

app= FastAPI()

app.include_router(user.user)
app.include_router(auth.auth)
app.include_router(business.business)

origins = [
  'http://localhost:3000',
  'http://192.168.187.229:3000'
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*']
)


models.Base.metadata.create_all(engine)
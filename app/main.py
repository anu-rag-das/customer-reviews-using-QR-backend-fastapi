from fastapi import FastAPI
from app.routes.user import user
from app.config import models
from app.config.db import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

#creating database
models.Base.metadata.create_all(bind=engine)

app= FastAPI()
app.include_router(user)

origins = [
  'http://localhost:3000',
  'http://localhost:3001',
  'http://localhost:3002'
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*']
)


models.Base.metadata.create_all(engine)
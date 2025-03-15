import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from examinis.modules import include_routers
from examinis.settings import Settings

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    root_path='/api',
    title='Examinis API',
    description='Examinis API documentation',
    debug=True,
)

origins = [
    'http://localhost:4200',
    'https://localhost:4200',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

include_routers(app)


@app.get('/')
def read_root():
    print(Settings().DATABASE_URL)
    return {'Hello': 'World'}

import logging

from fastapi import FastAPI

from examinis.modules import include_routers

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    root_path='/api',
    title='Examinis API',
    description='Examinis API documentation',
    debug=True,
)

include_routers(app)


@app.get('/')
def read_root():
    return {'Hello': 'World'}

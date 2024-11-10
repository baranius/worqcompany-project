import time

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import uvicorn

from app.routers.records import record_router
from app.logging import logging, logger
from app.environments import API_TITLE, APP_PORT


def create_app() -> FastAPI:
    app = FastAPI(title=API_TITLE)
    app.include_router(record_router)
    return app

app = create_app()

@app.middleware("http")
async def log_process_duration(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_duration = time.perf_counter() - start_time
    logger.log(level=logging.INFO, msg=f"{request.url} processed in {process_duration} ms")
    return response

@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as exception:
        logger.log(level=logging.ERROR, msg=exception)
        return JSONResponse(content={"message": "an error occured"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(APP_PORT))
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from score import critique
import time
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.inputs = "./inputs/"
    app.state.outputs = "./outputs/"
    yield
    print("Ending fastapi session")

app = FastAPI(lifespan = lifespan)

@app.post("/evaluate")
async def evaluate(request:Request, tasks:BackgroundTasks, file:UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted"
        )

    file_location = f"{request.app.state.inputs}/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    tasks.add_task(critique, file_location)
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "saved_to": file_location
    }

@app.get("/results")
async def results(request:Request, candidate_name):
    """
    Try to obtain results for candidates name.
    Input candidate_name must use underscore as a space. Ex: Feng_Lastname
    """
    textfilename = candidate_name + ".txt"
    result_path = request.app.state.outputs + "/" + textfilename
    if not os.path.isfile(result_path):
        raise HTTPException(status_code=404, detail=f"No candidate by the name: {candidate_name} found.")
    return FileResponse(
        path=result_path,
        media_type="text/plain",
        filename=textfilename
    )

from pathlib import Path
import uuid

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from producer import send_task
MAX_FILE_SIZE = 10 * 1024 * 1024

app = FastAPI()

templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())

    safe_filename = Path(file.filename).name

    file_content = await file.read()

    if len(file_content) > MAX_FILE_SIZE:
        return {
            "error": "File is too large",
            "max_size_mb": 10
        }

    file_path = UPLOAD_DIR / safe_filename

    with open(file_path, "wb") as buffer:
        buffer.write(file_content)

    send_task(
        job_id,
        safe_filename
    )

    return {
        "job_id": job_id,
        "filename": safe_filename,
        "status": "queued"
    }
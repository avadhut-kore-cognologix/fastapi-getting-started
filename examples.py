from fastapi import APIRouter, UploadFile

router = APIRouter(prefix="/examples", tags=["examples"])

@router.get("/")
def hey():
    return "Hey"

# path parameters
@router.get("/vehicle/{vehicle_name}")
def get_vehicle_name(vehicle_name: str):
    return {"vehicle_name": vehicle_name}

random_list = [{"abc": "def"}, {"def": "ghi"}, {"ghi": "jkl"}, {"jkl": "mno"}]

# query parameters
@router.get("/query")
def query(limit:int, skip:int = 0):
    return random_list[skip : skip + limit]

# file upload
@router.post("/file")
async def upload_file(file: UploadFile):
    filename = file.filename
    content = await file.read()
    return {"filename": filename, "content": content}

# multiple files upload
@router.post("/files")
async def upload_file(files: list[UploadFile]):
    res = []
    for file in files:
        filename = file.filename
        content = await file.read()
        res.append({"filename": filename, "content": content})
    return res
from tempfile import NamedTemporaryFile
from fastapi import UploadFile

async def save_temp_file(upload: UploadFile) -> str:
    suffix = upload.filename.split('.')[-1]
    tmp = NamedTemporaryFile(delete=False, suffix=f".{suffix}")
    content = await upload.read()
    tmp.write(content)
    tmp.close()
    return tmp.name

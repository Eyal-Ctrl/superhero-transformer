from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import uuid
import os
import cloudinary
import cloudinary.uploader

# CONFIGURATION
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# INIT APP
app = FastAPI()

class ImageRequest(BaseModel):
    image_url: str

@app.post("/transform")
async def transform_image(data: ImageRequest):
    try:
        image_data = requests.get(data.image_url).content
        input_filename = f"input_{uuid.uuid4()}.jpg"
        with open(input_filename, "wb") as f:
            f.write(image_data)

        output_filename = f"output_{uuid.uuid4()}.jpg"
        os.rename(input_filename, output_filename)

        upload_result = cloudinary.uploader.upload(output_filename)
        os.remove(output_filename)

        return {"url": upload_result["secure_url"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

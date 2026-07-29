import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    CORS_ORIGINS = [
        "http://localhost:3000",  # Local
        "https://topbox-mvp-git-dev-dev-gaitanos-projects.vercel.app",  # dev
        "https://topbox-mvp-git-api-integration-dev-gaitanos-projects.vercel.app",
        "https://topbox-agency.vercel.app",  # Prod
    ]

    CLOUDINARY_CLOUD_NAME = (os.getenv("CLOUDINARY_CLOUD_NAME"),)
    CLOUDINARY_API_KEY = (os.getenv("CLOUDINARY_API_KEY"),)
    CLOUDINARY_API_SECRET = (os.getenv("CLOUDINARY_API_SECRET"),)

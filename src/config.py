from dotenv import load_dotenv
import os

load_dotenv()

SHADERS_DIR = os.environ.get("SHADERS_DIR")
MODELS_DIR = os.environ.get("MODELS_DIR")
IMAGES_DIR = os.environ.get("IMAGES_DIR")
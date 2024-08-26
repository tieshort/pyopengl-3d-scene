from dotenv import load_dotenv
import os

load_dotenv()

SHADERS_DIR = os.environ.get("SHADERS_DIR")
MODELS_DIR = os.environ.get("MODELS_DIR")
SOURCES_DIR = os.environ.get("SOURCES_DIR")
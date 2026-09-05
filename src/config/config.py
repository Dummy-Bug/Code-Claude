import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

print(__file__)
PROJECT_PATH =  Path(__file__).resolve().parent.parent.parent
print("Project Path", PROJECT_PATH)

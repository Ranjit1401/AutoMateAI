from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Read variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
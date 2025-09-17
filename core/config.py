# core/config.py

import os
from motor.motor_asyncio import AsyncIOMotorClient
from openai import AsyncOpenAI
from dotenv import load_dotenv

# ------------------------------------------------------------------------
# Load environment variables from a .env file into the process environment
# ------------------------------------------------------------------------
load_dotenv()

# ------------------------------------------------------------------------
# MongoDB Configuration
# ------------------------------------------------------------------------
# - MONGODB_URI is read from environment variables.
# - Default value points to localhost (useful for local dev).
# - Database name: clinic_db
# - Collections:
#     * appointments_collection: stores appointment documents
#     * slots_collection: stores available time slots for services
# ------------------------------------------------------------------------
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URI)
db = client["clinic_db"]

appointments_collection = db["appointments"]
slots_collection = db["slots"]

# ------------------------------------------------------------------------
# OpenAI API Configuration
# ------------------------------------------------------------------------
# - Async client for non-blocking calls.
# - API key is loaded from environment variables.
# - Used for AI-driven features (e.g., voice agent, chatbot).
# ------------------------------------------------------------------------
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

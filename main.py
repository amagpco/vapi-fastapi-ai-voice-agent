# main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.config import appointments_collection, slots_collection
from api.routes import router

# ------------------------------------------------------------------------
# Lifespan context manager
# ------------------------------------------------------------------------
# Runs at application startup and shutdown.
# - Creates necessary indexes for MongoDB collections:
#     * appointments_collection: ensures uniqueness for (user_id, appointment_id).
#     * slots_collection: ensures efficient queries on (service_type, date).
# ------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create indexes if they don't exist
    await appointments_collection.create_index([("user_id", 1), ("appointment_id", 1)])
    await slots_collection.create_index([("service_type", 1), ("date", 1)])
    yield  # Application runs here


# ------------------------------------------------------------------------
# FastAPI Application
# ------------------------------------------------------------------------
# - lifespan is passed for startup/shutdown events
# - routers are included for modular API structure
# ------------------------------------------------------------------------
app = FastAPI(lifespan=lifespan)
app.include_router(router)

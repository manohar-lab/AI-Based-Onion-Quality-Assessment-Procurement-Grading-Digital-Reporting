"""Image upload / retrieval routes — NOT IMPLEMENTED YET."""

from fastapi import APIRouter

router = APIRouter(prefix="/images", tags=["images"])

# Future endpoints:
# POST /images               — upload inspection image
# GET  /images/{id}           — retrieve image
# DELETE /images/{id}         — remove image

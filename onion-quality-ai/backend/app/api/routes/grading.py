"""Grading routes — NOT IMPLEMENTED YET."""

from fastapi import APIRouter

router = APIRouter(prefix="/grading", tags=["grading"])

# Future endpoints:
# POST /grading/evaluate      — run government grading rules on an inspection
# GET  /grading/profiles      — list available grading profiles
# GET  /grading/result/{id}   — get grading result for an inspection

"""Report routes — NOT IMPLEMENTED YET."""

from fastapi import APIRouter

router = APIRouter(prefix="/reports", tags=["reports"])

# Future endpoints:
# POST /reports/generate      — generate PDF/HTML report for an inspection
# GET  /reports               — list reports
# GET  /reports/{id}          — download report

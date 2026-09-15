"""The 'before' — one bespoke REST endpoint for one client.

Nothing is wrong with this code in isolation. It's a normal, clean FastAPI
router. The problem only shows up once a SECOND AI client needs the same
style-guide data: it needs its own client-side code to call this exact
REST shape (auth, response parsing, error handling — all bespoke to THIS
endpoint). That's the N×M integration cost this POC exists to make visible.

See docs/04_recommendation.md, option B.
"""

from fastapi import APIRouter, Query
from pydantic import BaseModel

from . import style_guide

router = APIRouter(prefix="/legacy", tags=["legacy-rest"])


class LookupResponse(BaseModel):
    found: bool
    term: str
    language_pair: str | None = None
    approved: str | None = None
    note: str | None = None
    category: str | None = None
    suggestions: list[str] | None = None
    guide_last_updated: str


@router.get("/lookup-term", response_model=LookupResponse)
def lookup_term(
    term: str = Query(..., description="Term to look up"),
    language_pair: str | None = Query(None, description="e.g. 'fr-en'"),
) -> LookupResponse:
    result = style_guide.lookup_term(term, language_pair)
    return LookupResponse(**result)

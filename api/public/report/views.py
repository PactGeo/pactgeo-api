from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from api.public.report.crud import create_report, get_reports_by_content
from api.public.report.models import Report
from api.database import get_session
from api.public.dependencies import get_optional_current_user

router = APIRouter()

@router.post("/", response_model=Report)
def report_content(report: Report, db: Session = Depends(get_session), current_user = Depends(get_optional_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    report.user_id = current_user.id
    return create_report(report, db)

@router.get("/content/{content_type}/{content_id}", response_model=list[Report])
def get_reports(content_type: str, content_id: int, db: Session = Depends(get_session)):
    return get_reports_by_content(content_type, content_id, db)

from sqlmodel import Session, select
from api.public.report.models import Report

def create_report(report: Report, db: Session):
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

def get_reports_by_content(content_type: str, content_id: int, db: Session):
    statement = select(Report).where(
        Report.content_type == content_type,
        Report.content_id == content_id
    )
    return db.exec(statement).all()

def get_reports_by_user(user_id: int, db: Session):
    statement = select(Report).where(Report.user_id == user_id)
    return db.exec(statement).all()

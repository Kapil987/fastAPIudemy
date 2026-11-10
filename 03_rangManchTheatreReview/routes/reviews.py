from fastapi import APIRouter, Depends, Query
from typing import Annotated
from sqlmodel import Session, select, func
from models import Review, ReviewCreate, ReviewRead, ReviewUpdate
from database import get_session


SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter(prefix="/review",tags=["reviews"])

@router.post("/", response_model=ReviewRead)
# def create_review(review: ReviewCreate, session: Session = Depends(get_session)):
def create_review(review: ReviewCreate, session: SessionDep):
    db_review = Review(**review.model_dump())
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review

@router.get("/", response_model=list[ReviewRead])
def list_reviews(
    session: SessionDep,
    play_name: str | None = Query(None, description= "Filter by play name"),
    skip: int = Query(0,ge=0, description="Number of reviews to skip"),
    limit: int = Query(10, ge=1, le=50, description="Max reviews to return"),
):
    # SELECT *
    # FROM review;
    query = select(Review)

    if play_name:
        query = query.where(Review.play_name == play_name)
    
    query = query.offset(skip).limit(limit)
    reviews = session.exec(query).all()
    return reviews
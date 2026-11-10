from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone, UTC

## 1. Review class is a Database model
class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    play_name: str = Field(index=True)
    reviewer_name: str
    rating: int = Field(ge=1,le=5)
    comment: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

# 2. ReviewCreate – API input model
class ReviewCreate(SQLModel):
    play_name: str
    reviewer_name: str
    rating: int = Field(ge=1,le=5)
    comment: str


# 3. ReviewRead – API output model
class ReviewRead(SQLModel):
    id: int
    play_name: str
    reviewer_name: str
    rating: int = Field(ge=1,le=5)
    comment: str
    created_at: datetime = Field(default_factory=datetime.now)

# 4. ReviewUpdate – API update model
class ReviewUpdate(SQLModel):
    rating: Optional[int] = Field(default=None,ge=1,le=5)
    comment: Optional[str] = None

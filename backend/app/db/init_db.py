from sqlalchemy.orm import Session

from app.crud import crud_user
from app.schemas.user import UserCreate
from app.core.config import settings

def init_db(db: Session) -> None:
    # Create first superuser
    user = crud_user.user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            full_name="Initial Super User",
            is_superuser=True,
        )
        user = crud_user.user.create(db, obj_in=user_in) 
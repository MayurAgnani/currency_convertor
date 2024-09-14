from sqlalchemy.orm import Session
from models import User
from typing import Optional

def get_api_key(api_key: str, db: Session) -> Optional[str]:
    """
    Validate the API key against the database.

    Parameters:
    - api_key (str): The API key to validate.
    - db (Session): SQLAlchemy database session.

    Returns:
    - Optional[str]: The validated API key if found in the database, otherwise None.
    """

    if not api_key or api_key.isspace():
        return None
    user = db.query(User).filter(User.api_key == api_key).first()
    if user:
        return api_key
    else:
       return None

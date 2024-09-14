from fastapi import Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKey, APIKeyHeader
from typing import Union
from pydantic import BaseModel, EmailStr
from models import User, UserRequest, get_db_session, Base, engine
from sqlalchemy.orm import Session
from auth import get_api_key
import httpx
import datetime
from starlette.status import HTTP_403_FORBIDDEN
import json
import configparser  # Import configparser module for reading config files
from cache import get_cached_rate, set_cached_rate
from utils import create_response_body, store_user_request, is_rate_limit_exceeded, calculate_conversion  # Import from utils.py


app = FastAPI()

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Read rate limit values from configuration
weekdays_limit = int(config['rate_limits']['weekdays_limit'])
weekends_limit = int(config['rate_limits']['weekends_limit'])


API_KEY_NAME = "curreny_access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

COINBASE_API_URL = "https://api.coinbase.com/v2/exchange-rates"

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    api_key: str


@app.get("/convert")
async def convert_currency(
    from_currency: str,
    to_currency: str,
    amount:Union[int, float],
    api_key: APIKey = Depends(api_key_header),
    db: Session = Depends(get_db_session)
):
    """
    Converts an amount from one currency to another based on exchange rates.

    Args:
    - from_currency (str): Source currency code.
    - to_currency (str): Target currency code.
    - amount (Union[int, float]): Amount to be converted.
    - api_key (APIKey, optional): API key for authentication.
    - db (Session, optional): Database session.

    Returns:
    - dict: Conversion details including source, target, amount, converted amount, rate, and cache status.
    """
    
    # api validation
    validated_api_key = get_api_key(api_key, db)
    if not validated_api_key:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid API Key")
    
    # Rate limiting
    user_requests = db.query(UserRequest).filter(UserRequest.api_key == validated_api_key).all()
    if is_rate_limit_exceeded(user_requests, weekdays_limit, weekends_limit):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    
    # Fetch rate from Cache
    rate = get_cached_rate(from_currency, to_currency)


    if not rate:
         # Fetch rate from Coinbase API
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{COINBASE_API_URL}?currency={from_currency}")
            data = response.json()
            rate = data["data"]["rates"].get(to_currency)
            if not rate:
                raise HTTPException(status_code=400, detail="Invalid currency pair")
            conversion = amount * float(rate)

            set_cached_rate(from_currency, to_currency, rate)

            response_body  = create_response_body(from_currency, to_currency, amount, conversion, rate, False)
            
    else:
        conversion = amount * float(rate)

        response_body  =  create_response_body(from_currency, to_currency, amount, conversion, rate, True)
        
    
    # updae user_requests DB
    store_user_request(validated_api_key,from_currency, to_currency, amount, conversion, response_body, db)

    return response_body

    
@app.post("/users", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db_session)):

    """
    Creates a new user in the database.

    Args:
    - user (UserCreate): User details including username, email, and API key.
    - db (Session, optional): Database session.

    Returns:
    - User: Newly created user details.
    """
    
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    db_user = db.query(User).filter(User.api_key == user.api_key).first()
    if db_user:
        raise HTTPException(status_code=400, detail="API key already in use")
    
    new_user = User(
        username=user.username,
        email=user.email,
        api_key=user.api_key,
        created_at=datetime.datetime.now()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


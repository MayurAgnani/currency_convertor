import datetime
import json
from typing import Union
from sqlalchemy.orm import Session
from models import UserRequest

def create_response_body(from_currency: str, to_currency: str, amount: Union[int, float], conversion: float, rate: float, from_cache: bool) -> dict:
    """
    Creates a response body dictionary for currency conversion.

    Args:
    - from_currency (str): The source currency code.
    - to_currency (str): The target currency code.
    - amount (Union[int, float]): The amount to be converted.
    - conversion (float): The converted amount.
    - rate (float): The exchange rate used for conversion.
    - from_cache (bool): Indicates whether the rate was fetched from cache.

    Returns:
    - dict: A dictionary containing the conversion details.
    """
    return {
        "from_currency": from_currency,
        "to_currency": to_currency,
        "amount": amount,
        "converted_amount": conversion,
        "rate": rate,
        "from_cache": from_cache
    }

def store_user_request(validated_api_key: str, from_currency: str, to_currency: str, amount: Union[int, float], conversion: float, response_body: dict, db: Session) -> None:
    """
    Stores a user request in the database.

    Args:
    - validated_api_key (str): The validated API key of the user.
    - from_currency (str): The source currency code.
    - to_currency (str): The target currency code.
    - amount (Union[int, float]): The amount to be converted.
    - conversion (float): The converted amount.
    - response_body (dict): The response body dictionary to be stored.
    - db (Session): The SQLAlchemy database session.

    Returns:
    - None
    """
    user_request = UserRequest(
        api_key=validated_api_key,
        from_currency=from_currency,
        to_currency=to_currency,
        amount=amount,
        converted_amount=conversion,
        timestamp=datetime.datetime.now(),
        response_body=json.dumps(response_body)
    )
    
    db.add(user_request)
    db.commit()

def is_rate_limit_exceeded(user_requests, weekdays_limit, weekends_limit) -> bool:
    """
    Checks if the rate limit for user requests has been exceeded.

    Args:
    - user_requests (list): List of user requests.
    - weekdays_limit (int): Maximum allowed requests on weekdays.
    - weekends_limit (int): Maximum allowed requests on weekends.

    Returns:
    - bool: True if rate limit exceeded, False otherwise.
    """
    today = datetime.datetime.today().date()
    weekday = today.weekday()
    
    request_count = sum(1 for req in user_requests if req.timestamp.date() == today)
   
    return (weekday < 5 and request_count > weekdays_limit) or (weekday >= 5 and request_count > weekends_limit)

def calculate_conversion(amount: Union[int, float], rate: float) -> float:
    """
    Calculates the converted amount based on the given amount and exchange rate.

    Args:
    - amount (Union[int, float]): The amount to be converted.
    - rate (float): The exchange rate.

    Returns:
    - float: The converted amount.
    """
    return amount * rate

### Objective

Using Python and any framework, your task is to build a currency conversion service that includes FIAT and cryptocurrencies.

### Brief

In this challenge, your assignment is to build a service that makes conversions between different currencies. You will connect to an external API to request currency data, log & store requests of your users, and rate limit requests based on specific criteria. Your service must support at least the following currency pairs:

USD
EUR
BTC
ETH

### Tasks

-   Implement assignment using:

    -   Language: **Python**
    -   Framework: **any framework**

-   We recommend using the Coinbase API for exchange rates:

    https://developers.coinbase.com/api/v2#get-exchange-rates

-   Your service should be able to identify users. You may use any form of authentication that you think is suitable for the task (e.g., API keys, Username/Password)
-   Your service needs to store each request, the date/time it was performed, its parameters and the response body
-   Each user may perform 100 requests per workday (Monday-Friday) and 200 requests per day on weekends. After the quota is used up, you need to return an error message
-   The service must accept the following parameters:
    -   The source currency, the amount to be converted, and the final currency
    -   e.g. `?from=BTC&to=USD&amount=999.20`
-   Your service must return JSON in a structure you deem fit for the task
-   BONUS: find a clever strategy to cache responses from the external currency API

### Evaluation Criteria

-   **Python** best practices
-   Show us your work through your commit history
-   We're looking for you to produce working code, with enough room to demonstrate how to structure components in a small program
-   Completeness: Did you complete the features?
-   Correctness: Does the functionality act in sensible, thought-out ways?
-   Maintainability: Is it written in a clean, maintainable way?
-   Testing: Is the system adequately tested?

### CodeSubmit

Please organize, design, test, and document your code as if it were going into production - then push your changes to the master branch. After you have pushed your code, you may submit the assignment on the assignment page.

All the best and happy coding,


# Project Setup and Run Guide

## Prerequisites

Before starting, ensure you have the following installed:

- Python (preferably Python 3.7 or later)
- `pip` (Python package installer)
- `virtualenv` (optional but recommended for virtual environment management)

## Steps to Run the Project

cd python-currency-converter-btgnhd

python -m venv env

source env/bin/activate  # On 

pip3 install -r requirements.txt

uvicorn main:app --reload 


### API to create User

example:
curl -X POST "http://127.0.0.1:8000/users" -H "Content-Type: application/json" -d '{"username": "testuser3", "email": "test3@example.com", "api_key": "testapikey3"}'

#### Response:

{"username":"testuser3","email":"test3@example.com","api_key":"testapikey3"}


### API to create data with apikey

curl -X 'GET'   'http://localhost:8000/convert?from_currency=USD&to_currency=EUR&amount=100.0'   -H 'curreny_access_token:testapikey2'   -H 'Accept: application/json'

#### Response:

{"from_currency":"USD","to_currency":"EUR","amount":100,"converted_amount":93.07853456717868,"rate":"0.9307853456717867","from_cache":false}
 
### TODO

Add unit tests

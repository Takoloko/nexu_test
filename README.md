# Nexu Backend Coding Exercise - Solution

by Angel González


Talking with the cool engineering team, we decided to prioritize some of the features and use the following Tech Stack as we had 2 hours to deliver the coding solution to Frontend. 

## Tech Stack ##
- Python: Main programming language.
- Flask: Lightweight framework for handling HTTP requests and API routes.
- SQLite: Database for storing models data.
- Postman: Used for API testing and endpoint validation.

## INSTRUCTIONS ##

- Download the files
- Install the required dependencies for the app.py program to execute
- Run app.py on terminal
- Test the endpoints on browser

## Funcionalities

- **GET/brands**: Returns the list of all the model brands
- **GET/brands/brand_name/models**: Returns the list of car models based on their brand name
- **GET/models**: Returns the full list of Nexu car models.
- **GET/models?greater=&lower=**: Filters car models on lower and greater parameters.
- **PUT/models/:id**: Updates the average price of the desired car model.

Really enjoyed the excercise, found some challenges on the population of the database with the json file, but really had fun.

How would I proceed with more time?

- Restructure database according to requirement to include brands table
- Correct brands/brands_name/models as it should be with brand_id
- Finish the implementation of the pending endpoints
- Implement linted code, probably with Flake8.
- Unit Tests for each endpoint





# quotes-service-python
A simple Python CRUD API for Quotes.

## Getting started

### Set up a Python Virtual Environment

#### Create
```
python3 -m venv <path to venv>
```
Note that Python 3.10 was used to develop this application.

#### Activate
#### Windows
```
<path to venv>\Scripts\activate
```
#### Unix based (macOS and Linux)
```
source <path to venv>/bin/activate
```

### Install Dependencies
```
pip install -r requirements.txt
```

### To run App
```
uvicorn main:app --host 0.0.0.0 --port 80
```
Add the `--reload` option if you wish for it to reload with every file change.

#### API Documentation
You can view a full documentation (OpenAPI Standard) of the app by viewing http://127.0.0.1/docs once running the app.

The API supports the following requests:
-   Create quote
    -   Method: POST
    -   URL: /api/quote
    -   Parameters:
        -   quote: Quote in quection (ex: 'Live life')(required)
        -   author_name: Person who the quote belongs to (ex: 'Morgan Freeman') (required)
    -   Responses:
        -   201: Quote created successfully


-   Get a list of all the quotes
    -   Method: GET
    -   URL: /api/quote
    -   Responses:
        -   200: Get all quotes successfully


-   Read details of a quote
    -   Method: GET
    -   URL: /api/quote/{id}
    -   {id}: The id of the quote in question
    -   Responses:
        -   200: Got quote successfully
        -   404: Quote does not exist


-   Update details of a quote

    -   Method: PUT
    -   URL: /api/quote/{id}
    -   {id}: The id of the quote in question
    -   Parameters:
        -   quote: Quote in question (ex: 'Live life')(required if author_name not given)
        -   author_name: Person who the quote belongs to (ex: 'Morgan Freeman') (required if quote not given)
    -   Responses:
        -   200: Quote updated successfully
            -   quote: holding details of the quote now updated
        -   404: Quote does not exist


-   Delete a quote
    -   Method: DELETE
    -   URL: /api/quote/{id}
    -   {id}: The id of the quote in question
    -   Responses:
        -   200: Quote deleted successfully
        -   404: Quote does not exist

## Contributing

### Initialize pre-commit
`pre-commit` is used to format commits according to our coding standards. Initializing it here will install hook scripts into your local git repo.
```
pre-commit install
```

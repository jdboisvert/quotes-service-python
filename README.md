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

## Contributing

### Initialize pre-commit
`pre-commit` is used to format commits according to our coding standards. Initializing it here will install hook scripts into your local git repo.
```
pre-commit install
```

## Quotes REST API details

The API supports the following requests:

-   Create quote

    -   Method: POST
    -   URL: /api/quote
    -   Parameters:
        -   quote: Quote in quection (ex: 'Live life')(required)
        -   author_name: Person who the quote belongs to (ex: 'Morgan Freeman') (required)
    -   Responses:
        -   201: Quote created successfully
            -   quote: holding values of the quote
        -   409: Error registering quote

-   Get a list of all the quotes

    -   Method: GET
    -   URL: /api/quotes
    -   Responses:
        -   200: Get all quotes successfully
            -   quotes: holding an array of all the quotes
        -   500: Error getting quotes

-   Read details of a quote

    -   Method: GET
    -   URL: /api/quote/details/{id}
    -   {id}: The id of the quote in question
    -   Responses:
        -   200: Got quote successfully
            -   quote: holding details of the quote
        -   404: Quote does not exist
        -   500: Error getting quote

-   Update details of a quote

    -   Method: PUT
    -   URL: /api/quote/update/{id}
    -   {id}: The id of the quote in question
    -   Parameters:
        -   quote: Quote in quection (ex: 'Live life')(required if author_name not given)
        -   author_name: Person who the quote belongs to (ex: 'Morgan Freeman') (required if quote not given)
    -   Responses:
        -   200: Quote updated successfully
            -   quote: holding details of the quote now updated
        -   404: Quote does not exist
        -   409: Error updatting quote

-   Delete a quote
    -   Method: DELETE
    -   URL: /api/quote/delete/{id}
    -   {id}: The id of the quote in question
    -   Responses:
        -   200: Quote deleted successfully
        -   404: Quote does not exist
        -   500: Error deleting quote

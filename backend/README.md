# **Prerequisites**

-   **Python 3.10**

-   **Pip 22.3**

-   **Docker 2.8**

-   **PostgreSQL**

# **Local Deploy**

-   Go to main directory with `cd backend`

-   Create virtual enviroment with `python -m venv venv`

-   Run venv with `venv\scripts\activate` or
    `source ./venv/scripts/activate`

-   Install python packages with `pip install -r requirements.txt`

-   Create and run docker containter with `docker-compose up --build`

-   To stop container you can use `docker-compose stop`

# **How to use existing database with Flask-Migrate**

-   Create *migrations* folder with `flask db init`

-   Create automatic revision script with `flask db migrate`

-   Sets the revision in the database to the HEAD, without performing
    any migrations with `flask db stamp head`

-   Set local database as current with `flask db upgrade`

# **Usefully CLI commands**

-   Push local database to Docker with `docker exec -i backend-db-1
    psql -U nocarend -d stock < stock.db.sql`

-   See schemes with `\l`, choose our database with
    `\c stock`. After it just write SQL commands like
    `SELECT * FROM "USER"`

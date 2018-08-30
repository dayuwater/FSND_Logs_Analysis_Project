> # Log Analysis Project

# Description
- This code uses Python 2
- I created 3 custom views to facilitate SQL queries, see the instruction below for how to create the views
- This code utilizes Object-Oriented Design in Python. In other words, I created a class for the database:
    - This class handles the database connection and disconnection:
        - It connects to the database before querying 
        - It disconnects itself after all querying
    - All the questions and queries are stored in the class fields:
        - See `self.queries` for all the SQL queries and their cooresponding questions
    - It iterates through all the questions, runs all the SQL statements, and generates formatted output

# How to run the code
- Install the Python library for PostgreSQL: `pip install psycopg2`
- Create SQL views:
    - View 1: Article View Count:
    ```{SQL}
    CREATE VIEW article_count AS 
        SELECT articles.id,  articles.title, count(*) AS cnt 
        FROM articles INNER JOIN log ON concat('/article/',articles.slug) = log.path
        GROUP BY articles.id ORDER BY cnt DESC;
    ```

    - View 2: Connection Count group by date:
    ```{SQL}
    CREATE VIEW connection_count_by_date AS 
        SELECT count(*), date_trunc('day',time) FROM log GROUP BY date_trunc('day',time);
    ```

    - View 3: Error count group by date
    ```{SQL}
    CREATE VIEW error_count_by_date AS 
        SELECT count(*), date_trunc('day',time) 
        FROM (
            SELECT * FROM log WHERE cast(substring(status,1,3) as int) >= 400
        ) AS error 
        GROPUP BY date_trunc('day',time);
    ```

- `python project.py`

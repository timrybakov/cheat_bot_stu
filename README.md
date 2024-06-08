
### STU_CHEAT_BOT
## About project:
The project was created to make it easy to add documentation to AWS S3 cloud storage. 
The project includes a user interface and an interface for the administrator.
The bot is available for any user, the admin panel allows moderating the content received from the user.

## How to start project:

* Execute sequentially at the command line:
  - Clone the repository:
    ```
    git@github.com:timrybakov/cheat_bot_stu.git && cd cheat_bot_stu
    ```

  - Create and activate virtual environment:
    ```
    poetry install && poetry shell
    ```
    
 - Add environment variables:
    ```
    export AUTH_TOKEN=<bot_token>
    export TUNNEL_URL=<ngrok_tunnel_url>
    export ADMINS_ID=<admin_telegram_id>,<another_admin_telegram_id>
    export DB_HOST=<database_host>
    export DB_PORT=<database_port>
    export DB_USER=<database_user>
    export DB_PASS=<database_password>
    export DB_NAME=<database_name>
    ```

  - Start project:
    ```
    uvicorn main:app --reload
    ```

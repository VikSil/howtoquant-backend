# Deployment instructions

This manual contains instructions on how to deploy the repo on pythonanywhere hosting service. For full functionality always-on script are required to run microservices via cron jobs. Always-on scripts are a paid-for feature of pythonanywhere. The minimum custom bundle allows for one always-on script, one website, 2000s CPU per 24 hours and 1 GB of disk storage, at the price of 5 USD per month. This should be sufficient to host a fully functional version of this website.

For the purposes of this manual it is assumed that the pythonanywhere username is "*__howtoquant__*"

Some of the information in this manual is from [this](https://www.youtube.com/watch?v=xtnUwvjOThg) useful tutorial, with some project-specific details added.

## Setting up the repo

1. On pythonanywhere **Dashboard**, click `$Bash` button in the `New console section`. This will open a new Bash console.
1. Clone the repository into pythonanywhere with this command:

        git clone https://github.com/VikSil/howtoquant-backend

At this point the usage should be around 3s CPU and 14MB of storage.

3. Create vitrual environment with this command:

       mkvirtualenv --python=/usr/bin/python3.10 venv

At this point the usage should be around 41s CPU and 70MB of storage.

4. Navigate into the project directory with this command:

       cd how*

5. Install all of the project dependencies with this command (this will take 5-10 minutes to complete):

       pip install -r requirements.txt

At this point the usage should be around 100s CPU and 370MB of storage.

## Creating Web application

1. Open pythonanywhere **Web** dashboard. 
1. Click on `Add a new web app` button.
1. Choose the default domain name and click `Next` (domain name is configured on the front-end side via Netlify).
1. Choose **Manual configuration** - the screen will change.
1. Choose **Python 3.10** - the screen will change.
1. Click `Next` button - the Web dashboard will open.
1. In the `Virtualenv` section of the Web dashboard add path to virtualenv. Click the red link, type `venv` into the box and confirm.
1. In the `Code` section above click on the **WSGI configuration file** link - the file will open
1. Replace the content of the file with the following code

        import os
        import sys

        path = '/home/howtoquant/howtoquant-backend'
        if path not in sys.path:
            sys.path.append(path)

        os.environ['DJANGO_SETTINGS_MODULE'] = 'howtoquant.settings'

        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()

1. Click `Save` button.

## Adding configuration and monkey-fixes

1. In venv console execute the following commands:

        cd how*
        mkdir logs
        mkdir .envs
        cd .envs
        touch .env_prod
        nano .env_prod

1. In the editing screen that will open, paste the environment variables.
        ENVIRONMENT=production

        DB_ENGINE=django.db.backends.mysql
        DB_NAME=howtoquant$[database]
        DB_USER=howtoquant
        DB_PASSWORD=[password]
        DB_HOST=howtoquant.mysql.pythonanywhere-services.com
        DB_PORT=3306

        POLYGON_API_KEY=[api_key]

        SECRET_KEY=[secret_key]

1. Press `Ctrl + X`, then `Y`, then `Enter`.
1. Execute the following commands:

        cd ..
        nano settings.py

1. In the editing screen that will open:

* switch line

       env.read_env(BASE_DIR /'howtoquant/.envs/.env_dev')

  to

       env.read_env(BASE_DIR /'howtoquant/.envs/.env_prod')

* switch line

       ALLOWED_HOSTS = []

  to

       ALLOWED_HOSTS = ["127.0.0.1",
            'howtoquant.mysql.pythonanywhere-services.com',
            'howtoquant.pythonanywhere.com']

* comment out line

       CORS_ALLOWED_ORIGINS = ['http://localhost:5173',]

  and uncomment

        CORS_ORIGIN_ALLOW_ALL = True

6. Press `Ctrl + X`, then `Y`, then `Enter`.

1. Execute the following commands:

        cd ~
        cd .virtualenvs/venv/lib/python3.10/site-packages/corsheaders
        nano checks.py

1. In the editing screen that will open switch line

       from collections import Sequence

    to

       from collections.abc import Sequence

1. Press `Ctrl + X`, then `Y`, then `Enter`.

1. Execute the following command:

        nano signals.py

1. In the editing screen that will open switch line

       check_request_enabled = Signal(providing_args=['request'])

    to

       check_request_enabled = Signal('request')

1. Press `Ctrl + X`, then `Y`, then `Enter`.

## Creating and seeding the database

1. Open pythonanywhere **Databases** dashboard.
1. If you have previously created a database for the website, you will need to reset it (otherwise, proceed to step 4.). Click on the database name in the `Your databases` section - MySQL console will open.
1. Drop the database with the following query, where [database] is the database name. These will be identical to the link that you clicked in the previous step.

        drop database howtoquant$[database]

1. In `Create database` section of **Databases** dashboard, enter a new database name and click `Create` button. The new database will appear in the list above.
1. Click on the database name in the `Your databases` section - MySQL console will open.
1. Switch back to the venv Bash console and run the following commands:

        cd ~
        cd how*
        python manage.py migrate

1. Switch back to the MySQL console and run in the contents of vanilla scripts in the following sequence:

* classifiers\db\db_setup_classifiers.sql
* classifiers\db\vanilla_seed_classifiers.sql
* staticdata\db\db_setup_staticdata.sql
* staticdata\db\vanilla_seed_staticdata.sql
* marketdata\db\db_setup_marketdata.sql
* marketdata\db\vanilla_seed_marketdata.sql
* accounting\db\db_setup_accounting.sql
* accounting\db\vanilla_seed_accounting.sql
* config\db\db_setup_config.sql

## Setting up always-on script

1. Open pythonanywhere **Tasks** dashboard.
1. In the `Always-on tasks` section add a new always-on task: 

        source /home/howtoquant/.virtualenvs/venv/bin/activate && cd how* && python manage.py runcrons

1. Click `Create` button.
1. Click on the `View task log` button (first in `Actions` column) - this will open the log file.
1. After the script has started, it should continously log every 60 seconds output similar to:

        Sep  2 22:57:55 Running Crons
        Sep  2 22:57:55 ========================================
        Sep  2 22:57:55 [✔] config.rollforward
        Sep  2 22:57:55 [✘] config.flow_booker
        Sep  2 22:57:55 [✔] config.position_manager
        Sep  2 22:57:55 [✔] config.cash_manager
        Sep  2 22:57:55 [✔] config.asset_manager

## Final step

Once all of the above are done, click the big, green `Reload` button on the Web dashboard and wait for it to reload.

## Post-deployment tests

1. Run the following queries in the MySQL console:

        SELECT * FROM staticdata_identifier; -- should return three tickers
        SELECT * FROM config_msg_queue; -- should return an empty set

1. Navigate to `https://howtoquant.pythonanywhere.com/accounting/api/asset_ladder` - this should return a JSON with status `OK` and `null` dataset on `asset_ladder` key.

1. Navigate to `https://howtoquant.pythonanywhere.com/accounting/api/cash_ladder?end_date=[date]`, where [date] is T+2 in format YYYY-MM-DD - this should return a JSON with status `OK` and `null` dataset on `asset_ladder` key.

1. Navigate to `https://howtoquant.pythonanywhere.com/classifiers/api/countries` - this should return a JSOn with a list of active countries.

1. Navigate to `https://howtoquant.pythonanywhere.com/staticdata/api/equities` - this should return a JSON with three equities.

1. Send a PUT request to `https://howtoquant.pythonanywhere.com//staticdata/api/instruments` with the following body:

        {
            "ticker":"NVDA",
            "service":"polygon.io"
        }

1. Navigate to `https://howtoquant.pythonanywhere.com/staticdata/api/equities` - this should now return a JSON with four equities, including NVDIA.

1. Send a PUT request to `https://howtoquant.pythonanywhere.com/marketdata/api/prices/new` with the following body:

        {
            "tickers":["NVDA"],
            "date_from": "2024-08-01",
            "date_to": "2024-09-01"
        }

    this should return a download_id.

1. Send a PUT request to `https://howtoquant.pythonanywhere.com/marketdata/api/prices/download` with the following body:

        {
            "download_id": [download_id from the previous step],
            "options":"overrideall"
        }

    this should return result "OK"

1. Navigate to `https://howtoquant.pythonanywhere.com/marketdata/api/prices` - this should return a JSON with the saved  prices

1. Send a PUT request to `https://howtoquant.pythonanywhere.com/accounting/api/trades` with the following body:

        {
            "ticker":"TSLA",
            "direction":"B",
            "quantity": 10,
            "price":200,
            "book_name": "Long Short",
            "strategy_name": "Long Only",
            "counterparty": "Counterparty"
        }

    this should return trade details

1. Navigate to `https://howtoquant.pythonanywhere.com/accounting/api/trades` - this should return a JSON with the saved trade

1. Wait for up to 10 minutes for the services to process the trade into ladders.

1. Navigate to `https://howtoquant.pythonanywhere.com/accounting/api/asset_ladder` - this should now return a JSON with a new record in the ladder.

1. Navigate to `https://howtoquant.pythonanywhere.com/accounting/api/cash_ladder?end_date=[date]`, where [date] is T+2 in format YYYY-MM-DD - this should now return a JSON with a new record in the ladder.

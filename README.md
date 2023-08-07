## Local development

### Frontend

1. Set up local environment

- Enter the frontend folder with `cd .\frontend\`
- Create .env file at the project root, the same folder where package.json is located.
- Add required variables to .env file like the example below, replace urls with bmpnus project host.
```
BUILD_PATH = '/usr/local/apache2/htdocs/'
REACT_APP_API_HOST = 'http://127.0.0.1:8000'
BROWSER = None
```
2. Install dependencies

- Install the dependencies with `npm install`.

3. Start project

- Execute the project with `npm start`.

### Backend

1. Set up local environment

- Enter the frontend folder with `cd .\backend\`
- Create .env file at the project root, the same folder where manage.py is located.
- Add required variables to .env file like the example below:
```
DATABASE_name="ebpm"
DATABASE_USER="postgres"
DATABASE_PASSWORD="postgres"
DATABASE_HOST="localhost"
DATABASE_PORT="5432"
```

2. Install dependencies

- Install the dependencies with `pip install requirements.txt`.

3. Migrate database

- Execute the database migration with `python manage.py migrate`.

4. Start project

- Execute the project with `python manage.py runserver`.

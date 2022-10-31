# pastag-healthcare

Pastag healthcare is a health tracker that tracks blood pressure and weight

This repository includes the full server of the pastag application.

Tested on python 3.6

# Running Tests

Since this software uses postgres sql.

You might need to run this app to apply tests
CREATE USER readme; and ALTER USER readme CREATEDB;

# Installation

1. Activate your virtual environment (Make sure it's python 3.6)

2. Install the dependencies

```bash
$ pip install -r requirements.txt
```

4. Configure .env files (.env.example should help)


5. Run migrations

```bash
$ python manage.py migrate
```

6. Run npm install

```bash
$ npm install
```

7. Launch the development server

```bash
$ python manage.py runserver
```

# Compile Using Babel and Rollup

```bash
$ npm run build
```
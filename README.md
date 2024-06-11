# Food Tracker

This is a food-tracking application built using **Django 4**, **HTML 5**, **CSS 3** and **Bootstrap 5** with a **Bootswatch** theme. The app uses a **PostgreSQL** database to store data. Charts were built using **Chart.js 2**. And the customizable admin panel using **Jazzmin**.

![Screenshot 2024-03-24 114038](https://github.com/Neem-Sheth/SAS-Fat-To-Slim---Techmill/assets/124123479/1d2e5f49-e176-4cc0-94f7-a718b8e52285)


![Screenshot 2024-03-24 114055](https://github.com/Neem-Sheth/SAS-Fat-To-Slim---Techmill/assets/124123479/498b0b3e-6c07-4c07-b606-adae05f3eee5)


![Screenshot 2024-03-24 114119](https://github.com/Neem-Sheth/SAS-Fat-To-Slim---Techmill/assets/124123479/00812ed1-6c5f-4ad8-a0d7-90de70e95219)


![Screenshot 2024-03-24 114211](https://github.com/Neem-Sheth/SAS-Fat-To-Slim---Techmill/assets/124123479/ffdcf52c-c16a-49fd-9c38-315a32cee871)


![Screenshot 2024-03-24 114229](https://github.com/Neem-Sheth/SAS-Fat-To-Slim---Techmill/assets/124123479/1bd5ec62-0164-4491-881c-79b18da456f8)


### Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the application](#run-the-application)
- [Running the tests](#run-the-tests)
- [Adding data to the application](#add-data-to-the-application)


### Prerequisites

Install the following prerequisites:

1. [Python 3.8-3.11](https://www.python.org/downloads/)
<br> This project uses **Django v4.2.4**. For Django to work, you must install a correct version of Python on your machine. More information [here](https://django.readthedocs.io/en/stable/faq/install.html).
2. [PostgreSQL](https://www.postgresql.org/download/)
3. [Visual Studio Code](https://code.visualstudio.com/download)


### Installation

#### 1. Create a virtual environment

From the **root** directory, run:

```bash
python -m venv venv
```

#### 2. Activate the virtual environment

From the **root** directory, run:

On Windows:

```bash
venv\scripts\activate
```

#### 3. Install required dependencies

From the **root** directory, run:

```bash
pip install -r requirements.txt
```

#### 4. Set up a PostgreSQL database

With **PostgreSQL** up and running, in a new Terminal window, run:

```bash
dropdb --if-exists food
```

Start **psql**, which is a terminal-based front-end to PostgreSQL, by running the command:

```bash
psql postgres
```

Create a new PostgreSQL database:

```sql
CREATE DATABASE food;
```

Create a new database admin user:

```sql
CREATE USER yourusername WITH SUPERUSER PASSWORD 'yourpassword';
```

To quit **psql**, run:

```bash
\q
```

#### 5. Set up environment variables

From the **root** directory,:

Create the **.env** file manually by navigating in Visual Studio Code to the Explorer and selecting the option **New File**.

Next, declare environment variables in the **.env** file. Make sure you don't use quotation marks around the strings. 
Add appropriate Twilio Credentials for Twilio Whatsapp API.

```bash
SECRET_KEY=yoursecretkey
DEBUG=True
DATABASE_NAME=food
DATABASE_USER=
DATABASE_PASS=
DATABASE_HOST=localhost

TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
```

#### 6. Run migrations

From the **root** directory, run:

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

#### 7. Create an admin user to access the Django Admin interface

From the **root** directory, run:

```bash
python manage.py createsuperuser
```

When prompted, enter a username, email, and password.


### Run the application

From the **root** directory, run:

```bash
python manage.py runserver
```

### View the application

Go to http://127.0.0.1:8000/ to view the application.

### Add data to the application

Add data through Django Admin.

Go to http://127.0.0.1:8000/admin to access the Django Admin interface and sign in using the admin credentials.


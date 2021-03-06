# Mexican Hand Sign Language Image Recognition

## Test the application
In order to manually test this application, it is required to enter to the following url and follow the instructions on the page.

[Test app in my personal website](http://www.erikiado.com/)

NOTE: In order to test the correct functionality, an image with the following characteristics needs to be uploaded:
* Dimensions: 20x20x1
* (x1) refers that the image is a binary image or a mask with just white and black pixels.

NOTE 2: The application is in spanish given the target audience are mexican students.

NOTE 3: Test images are provided under the test_images folder on the repository.
## System Requirements

* [Python 3.5](https://www.python.org/downloads/)
* [PostgreSQL 9.5+](https://wiki.postgresql.org/wiki/Detailed_installation_guides)

## Database Setup

After downloading (https://www.postgresql.org/download/) and installing PostgreSQL, you should be able to switch to the postgres user on your system and start a session in the postgresql interpreter.

```bash
$ su postgres

$ psql
```

Next, we will create a database and an admin user for our project. Later on we will use this information to setup the database on our project and to activate it through our virtual environments.
```sql
CREATE DATABASE project_name_db;
CREATE ROLE project_db_admin WITH LOGIN PASSWORD 'db_admin_password';
GRANT ALL PRIVILEGES ON DATABASE project_name_db TO project_db_admin;
ALTER USER project_db_admin CREATEDB;
```


## Virtual Environments

### Virtualenv

You will need to create a virtual environment in order to isolate all the packages that are required for the project. We provide instructions on how to do it with [`virtualenv`](https://virtualenv.pypa.io/en/stable/)

First find the path to your `python 3.5` installation by running

```bash
$ which python3.5
PATH TO PYTHON 3.5
```

Then create the virtual environment like this. (We use different virtualenvironments for different functions, such as testing, development, production, and CI, each of them has different requirements, you should at least create an environment for development and one for testing.)
```bash
$ virtualenv --python='PATH TO PYTHON 3.5' /path/to/your/venv/NAME_OF_YOUR_ENV
```

We use environment variables to separate sensitive information and keys from the code, you should set the following ones.


```bash
DJANGO_SETTINGS_MODULE='erikiado.settings.development' // The last part depends on the environment you are on
SECRET_KEY='Generate one here. (http://www.miniwebtool.com/django-secret-key-generator/)'
DB_NAME='project_name_db' // From Database Setup
DB_USER='project_user_admin'
DB_PASSWORD='db_admin_password'
DB_HOST='localhost' // For local development 127.0.0.1 or localhost
DB_PORT=''
```

In order to set them in your virtualenv just go to `/path/to/your/venv/NAME_OF_YOUR_ENV/bin/activate` and in the section for deactivate add at the end

```bash
unset NAME_OF_ENV_VAR
```
And set the variable at the end of the file like this

```bash
export NAME_OF_ENV_VAR='VALUE OF VAR'
```

After you are finished you can activate your virtual environment by running
```bash
$ source /path/to/your/venv/NAME_OF_YOUR_ENV/bin/activate
```

And deactivate it just by running this command on the terminal
```bash
$ deactivate
```


## Installing the Project Requirements

You will need to install different packages depending on the environment you are working on.

```bash
$ pip install -r reqs.txt
```

## Running the project

Once you have finished the setup, you can run the project.

```bash
Run the migrations
$ python manage.py migrate
Start the development server
$ python manage.py runserver
```
After this you can go to your browser and go to http://localhost:8000, and you should be able to see the project running.

## Running the tests
Since this application is wrapped around the django framework I took advantage of its test framework which executes all the test inside each application and gives us some perks in order to unittest and to make integration tests.
To run the tests, after the project can be ran, execute the following command:

```bash
$ python manage.py test
```

## Standards Used
Standards for documentation and code style were used.

### Code Style
The PEP-8 standard for code was used in the development of this project.
The tool flake8 which is part of the dependencies is used to lint the code following this standard.
https://www.python.org/dev/peps/pep-0008/

### Documentation
For the documentation the numpy standard is being used.
https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt

# Beatitud Server

## Setup a development station
1. install docker
2. install docker-compose
3. create a directory 'env' (it won't be pushed) to store critical information that MUST not appear in your repo.

    a/ create a file django_variables.env
    
    b/ set:
    ```text
    DJANGO_SETTINGS_MODULE=beatitud_back.settings.local
    SECRET_KEY=#SET A KEY#
    ```
    
    c/ create a file db_postgres_variables.env
    
    d/ set:
    ```text
    DB_USER=beatitud
    DB_DATABASE=beatitud
    DB_PASSWORD=#SET A PASSWORD#
    ```
        
4. docker-compose up --build -d 
5. docker-compose exec django /bin/bash
6. python manage.py migrate
7. python manage.py createsuperuser
        
        
## Structure (TO READ)
```
beatitud_back
|-   apps
|-  |- app_name
|-  |-  |- contrib
|-  |-  |-  |- drf # Django rest framework
|-  |-  |-  |-  |- tests
|-  |-  |-  |-  |- serializers
|-  |-  |-  |-  |- urls
|-  |-  |-  |-  |- views
|-  |-  |- fixtures # for tests
|-  |-  |- tests
|-  |-  |- migrations 
|-  |-  |- __init__
|-  |-  |- ... (everything genereated by django-admin 
                startapp except from those move into contrib/drf)
|-   env                                     # Apps env var
|-   beatitud_back                              # All settings for this project
```
1- As Django said, every app should be independent from the project that's why we put them in a different directory. It is really important to think each app as a gear that could be used by another system in the future.
2- Since we are using Django rest framework we set this contribution in each app in a subdirectory with every files changed by this contribution so as to be able to choose another contribution one day and know exactly what we have to alter.
3- So every script or tools of an app should stay at the root of the app directory.
But views must be moved in the drf directory. And urls could be moved or should redirect to another urls in drf.



## Using python in container
Always remember to use 
```bash
python manage.py shell
```
If not you will have to do at every launch after
```python
import django
django.setup()
```
Otherwise settings in console won't be populated.
See https://docs.djangoproject.com/en/2.1/topics/settings/.
(You can setup pycharm to do it automatically in order to use its console.)


## Connection to Beatitud VM

```shell
$ ssh ubuntu@beatitud.io
```

Pull all git repos:
```shell
git submodule update --recursive --remote
```

Build django without cache :
```shell
$  sudo docker-compose build --no-cache django
```
# PurBeurre Project
OC project n°10

In the continuity of offering good everyday products, this project aims to allow
everyone to be able to substitute a product with a healthier equivalent.
To do this, we use the API of OpenFoodFacts and sort on the nutritional-score,
nova-scores and eco-score of each product.

#### Languages:
* Python3.8
* HTML5
* CSS3
* Javascript

#### Tools:
* Django (version 3.2.7)
* Bootstrap (for design)
* PostgreSQL

#### API:
* OpenFoodFacts

### Prerequisites:
* Python3
* pipenv

## Program flow: local use
1. Download this app :
```
git clone https://github.com/RiwsPy/OC_P8.git
```

2. Create your own PostgreSQL database

3. Open the OC_P8 folder

4. Rename _.env_sample_ in _.env_

5. Write in your own django key and database login

6. Install the virtual environment
```
    pipenv install
    pipenv shell
```

7. Import data from the API OpenFoodFacts
```
    ./manage.py uDB
```

8. Start the application
```
    ./manage.py runserver
```

By default, your application is available here: 
http://127.0.0.1:8000/


## Program flow: online use
This application is available in Heroku: 
https://healthy-product.herokuapp.com/


### Architecture:
- .env
- Procfile
- Pipfile
- Pipfile.lock
- manage.py
- PurBeurre/
    - asgi.py
    - settings.py
    - urls.py
    - wsgi.py
- catalogue/
    - fixtures/
    - tests/
        - db_product_mock.json
        - test_import_off.py
        - test_models.py
        - test_pages.py
    - admin.py
    - apps.py
    - forms.py
    - models.py
    - urls.py
    - views.py
- static/
    - css/
    - img/
    - js/
- templates/layouts/
    - 404.html
    - 500.html
    - base.html
    - header.html
    - mentions.html
    - message.html
    - product_presentation.html
    - search_form_nav.html
    - search.htmll
- user/
    - templates/
        - account.html
        - favorite.html
        - login.html
        - register.html
    - tests/
        - geckodriver.exe
        - test_functionnal.py
        - tests.py
    - admin.py
    - apps.py
    - forms.py
    - models.py
    - urls.py
    - views.py


NB:
the selenium functionnal test requires the installation of Firefox web browser on your computer, it is also necessary to have a geckodriver file compatible with your computer system (you must place this file in user/tests/ folder, the geckodriver current is only compatible with Ubuntu).
See also : https://github.com/mozilla/geckodriver/releases

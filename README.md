# private_url_shortener

a URL shortening service that generates links that are not feasibly guessed - suitable for automatic login links, documents with obfuscated URLs, etc.

## Run

Use the image:

`docker run -it -p 8000:8000 jhmaddox/private_url_shortener`

or from source:

    > git clone git@github.com:firstjob/private_url_shortener.git
    > cd private_url_shortener
    > virtualenv -p python3 ENV
    > source ENV/bin/activate
    > pip install -U pip
    > pip install -r requirements.txt
    > python manage.py runserver

## Usage

    > curl http://localhost:8000/api/shortened-url/ --data "url=http://www.google.com"
    {"created":"2017-01-07T00:36:59.949406Z","expires":null,"result_url":"/1/33QhjM/","url":"http://www.google.com"}
    
    > curl -Ls -o /dev/null -w %{url_effective} http://localhost:8000/1/33QhjM/
    http://www.google.com/

    (or open your browser to http://localhost:8000/1/33QhjM/ and verify the redirect)
    
## Admin

Use `python manage.py createsuperuser` to create a login, then visit `/admin/` for a basic CMS.

## Options

The following environmental variables can be used to configure the webservice:

- ALLOWED_HOSTS
  - Set the hostname where the service is deployed. Comma separate for multiple values. (see [Django documentation](https://docs.djangoproject.com/en/1.10/ref/settings/#allowed-hosts))

- DATABASE_ENGINE
  - Set to your preferred database engine:
    - django.db.backends.sqlite3 *(default)*
    - django.db.backends.mysql
    - django.db.backends.postgresql

- DATABASE_HOST
  - Set to your database host *(if any)*

- DATABASE_NAME
  - Set to your database name or database filename for sqlite

- DATABASE_PASSWORD
  - Set to your database password *(if any)*
 
- DATABASE_PORT
  - Set to your database port *(defaults to database engine's default port)*
 
- DATABASE_USER
  - Set to your database user *(if any)*
  
- DEBUG
  - Set to True to enable Django debug mode
  
- SECRET_KEY
  - Configures secret key for hmac generation. Use a long random string (see [Django Secret Key Generator](http://www.miniwebtool.com/django-secret-key-generator/))

- PRIVATE_SHORTENER_API_SECRET_KEY
  - Configures secret key for API authorization
    - defaults to empty string, API does not require authentication
    - if set, only bearer can create shortened URLs (see [Authorization](/#Authorization))

- PRIVATE_SHORTENER_SIG_LENGTH
  - Configures shortened URL signature length
    - the signature is encoded in base 62
    - signature length defaults to 6 characters (truncated hmac)
    - maximum length is 22 characters

- PRIVATE_SHORTENER_REDIRECT_EXPIRED_URL
  - Configures a URL to redirect users to if the requested URL has expired

- PRIVATE_SHORTENER_REDIRECT_INVALID_URL
  - Configures a URL to redirect users to if the requested URL is invalid

- STATIC_ROOT
  - Configures the location of the staticfiles root directory. (see [Django documentation](https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-STATIC_ROOT))
  
- STATIC_URL
  - Configures the staticfiles URL prefix. *(defaults to /static/)* (see [Django documentation](https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-STATIC_URL))

- TIME_ZONE
  - Configures Django timezone setting. *(defaults to UTC)* (see https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-TIME_ZONE)

## Examples

The following example configurations are provided:

- docker-compose:
  - `docker-compose -f example_conf/docker-compose.sqlite.yml up`
  - `docker-compose -f example_conf/docker-compose.mysql.yml up`
  - `docker-compose -f example_conf/docker-compose.postgres.yml up`
- kubernetes
  - `kubectl apply -f example_conf/kubernetes.yml`
 

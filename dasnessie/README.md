# WishList

A simple wish list website.

## Installation

These install instructions are for uberspace 7, using gunicorn.

1. Clone this repo onto your server
2. Install gunicorn for python 3: `pip3.6 install gunicorn`
2. Install Django for python 3: `pip3.6 install Django`
3. Make a subdomain folder, eg somewhere in `/var/www/virtual/<username>/<subdomain>`
4. Make a folder for static files somwhere in that folder, eg `/var/www/virtual/<username>/<subdomain>/static`
5. Set your [web backends](https://manual.uberspace.de/web-backends.html) using the `uberspace web backend` utility. The subdomain needs to be set to a port on which gunicorn will later listen (such as `8000`), the static files need to be served by apache. Example: 

        $ uberspace web backend list
        <subdomain>/static apache
        <subdomain>/ http:8000
        / apache

6. In your copy of this repo, edit `dasnessie/settings.py`:
    1. Set `STATIC_ROOT` to the folder for static files you just created
    2. Set `WISHLIST_URL` to the base url under which the site will run
    3. Set `WISHLIST_OWNER_S` to the name that should be set in the header
    3. Set `WISHLIST_TITLE` to the title of the list, eg 'Wishlist'
    4. Set `ALLOWED_HOSTS` to include your host
    5. Ensure that `DEBUG` is set to false
7. Run `python3 manage.py collectstatic` in the folder that contains `manage.py` to copy your static files to the folder you set
8. Run `python manage.py migrate` in the folder that contains `manage.py` to set up the database
9. Make a service: In `~/etc/services.d/`, make a file called something like `wishlist.ini` that contains the following:

        [program:wishlist]
        command=gunicorn -b '0.0.0.0:8000' dasnessie.wsgi
        directory=<path to repo>/dasnessie/
        autostart=true
        autorestart=true
        redirect_stderr=true

10. Run the service:
    1. Update the service list: `supervisorctl reread`
    2. Start the deamon: `supervisorctl update`
    3. Run the service: `supervisorctl start wishlist`

## Update

For updating, do the following:

1. Run `git pull` to get the latest version
2. Run `python3 manage.py collectstatic` in the folder that contains `manage.py` to copy your static files to the folder you set
3. Run `python manage.py migrate` in the folder that contains `manage.py` to set up the database
4. Restart the service: `supervisorctl restart wishlist`
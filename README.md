# WishList

A simple wish list website.

Copyright (C) 2019  dasNessie

## Installation

These install instructions are for uberspace 7, using gunicorn.

1. Clone this repo onto your server
2. Install the dependencies for python 3: `pip3.6 install -r requirements.txt`
2. Install gunicorn for python 3: `pip3.6 install gunicorn`
3. Make a subdomain folder, eg somewhere in `/var/www/virtual/<username>/<subdomain>`
4. Make a folder for static files somwhere in that folder, eg `/var/www/virtual/<username>/<subdomain>/static`
5. Set your [web backends](https://manual.uberspace.de/web-backends.html) using the `uberspace web backend` utility. The subdomain needs to be set to a port on which gunicorn will later listen (such as `8000`), the static files need to be served by apache. Example: 

        $ uberspace web backend list
        <subdomain>/static apache
        <subdomain>/ http:8000
        / apache

6. In your copy of this repo, create a file called `.env` and add the following settings:
    1. Set `SECRET_KEY` to an appropriate (random) value
    2. Set `STATIC_ROOT` to the folder for static files you just created
    3. Set `ALLOWED_HOSTS` to include your host
    4. Set `WISHLIST_URL` to the base url under which the site will run
    5. Set `WISHLIST_OWNER_S` to the name that should be set in the header
    6. Set `WISHLIST_TITLE` to the title of the list, eg 'Wishlist'
    7. SET `LANGUAGE_CODE` to the language your installation should have. If you don't set this, it will default to German
    8. The file should now look like this:

            SECRET_KEY = '012lhdwi8az1#%$eygb-%9z^x3r)i-24$51mh(i$-_!^+4yq3f'
            STATIC_ROOT = '/var/www/virtual/dasnessie/wunschzettel.dasnessie.de/static'
            ALLOWED_HOSTS = 'https://wunschzettel.dasnessie.de'
            WISHLIST_URL = 'https://wunschzettel.dasnessie.de'
            WISHLIST_OWNER_S = 'Nessies'
            WISHLIST_TITLE = 'Wunschzettel'
            LANGUAGE_CODE = 'de'

7. Run `python3 manage.py collectstatic` in the folder that contains `manage.py` to copy your static files to the folder you set
8. Run `python manage.py migrate` in the folder that contains `manage.py` to set up the database
8. Run `python manage.py createsuperuser` to create a user for the admin interface. You can use that user account later to add items to the list.
8. Run `python manage.py compilemessages` to generate the language files.
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
11. Add items to you list: Go to the URL under which the site is running. Go to /admin from there, log in with the data from step 10 and start adding wishes

Please let me know if you encounter any problems following these instructions!

## Update

For updating, do the following:

1. Run `git pull` to get the latest version
2. Run `python3 manage.py collectstatic` in the folder that contains `manage.py` to copy your static files to the folder you set
3. Run `python manage.py migrate` in the folder that contains `manage.py` to set up the database
4. Restart the service: `supervisorctl restart wishlist`

## License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
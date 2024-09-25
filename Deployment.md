# Deployment

## Manual deployment on a Virtual Private Server (VPS)

Domain name: [victorng.fr](https://victorng.fr/)

### Frontend

The Vue.js **frontend** is served by an Apache web server.
The `dist` folder is under `/srv/www/en-cavale-visual` on the VPS.

### Backend

The web server proxy API request to the Flask backend application.

Install the necessary packages in order to build Python 3.11.

Start Flask app as a background process:

```sh

```

gunicorn -b localhost:5000 -w 4 encavale:app --daemon

```

### Web Server

Here is the Apache configuration:

```

<VirtualHost \*:80>
ServerAdmin victorng@hotmail.fr
ServerName victorng.fr
ServerAlias www.victorng.fr
DocumentRoot /srv/www/en-cavale-visual

    <Directory /srv/www/en-cavale-visual>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    # Proxy API requests to the Flask application
    # Assuming your API is served on localhost:5000
    <Location /api>
        ProxyPass http://127.0.0.1:5000/api
        ProxyPassReverse http://127.0.0.1:5000/api
    </Location>

    # Optional: Redirect all other requests (like Vue.js router URLs) to index.html
    <IfModule mod_rewrite.c>
        RewriteEngine On
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule ^ /index.html [L]
    </IfModule>

    ErrorLog ${APACHE_LOG_DIR}/victorng.fr_error.log
    CustomLog ${APACHE_LOG_DIR}/victorng.fr_access.log combined

</VirtualHost>
```

Enable Apache modules:

```shell
sudo a2enmod proxy proxy_http rewrite
```

Enable HTTPS on [victorng.fr](https://victorng.fr/) using [certbot](https://certbot.eff.org/) (Let's Encrypt certificate). Modify Both HTTP (Port 80) and HTTPS (Port 443) configurations.

After configuration changes:

```sh
sudo systemctl restart apache2
```

### Database

Backup and restore the local Postgres DB to the remote server.

```sh
docker run --rm --network=host -v $(pwd):/backup -e PGPASSWORD=example postgres:14 pg_dump -h localhost -U postgres
-d postgres --schema-only -F c -f /backup/backup_file_schema.dump
```

```sh
pg_restore -U postgres -h localhost -d postgres --clean --create -c backup_file.dump
```

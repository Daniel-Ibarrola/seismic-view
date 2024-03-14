# Earthworm Graphing App

App to visualize earthworm data in real time.

## Deployment to nginx

To build the app for production use the following commands

```shell
npm run build
npm run preview
```
The last command will start a server to view the website in production mode.
If everything is working as expected the app static files can be server in nginx.
To do that copy the dist folder created by the build command to the path were nginx
will look for the static files (typically /var/www/site-name).


## Developing

You can start the development server (port 5173) with:

```shell
make dev
```

Now go to http://localhost:5173 to see the React app.

To run the tests use. The development server should be started first:

```shell
make test
```

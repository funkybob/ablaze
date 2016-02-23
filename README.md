# ablaze
A veneer over aiohttp to make life less tedious


# Creating an app

1. Create a config.ini
   ```
   # A list of config section -> module mappings
   [ablaze]
   templates=ablaze.templates
   models=ablaze.models
   app=myapp

   [templates]
   paths=templates/

   [models]
   apps=myapp.auth,myapp.page

   [app]
   ```

2. Launch it

   ```
   $ python -m ablaze config.ini
   ```

# How it works

First, the config file is loaded and stashed on the app instance as
`app['config']`.

It then iterates through each item in `[ablaze]', imports the module specified,
and invokes ``setup`` in it, passing the ``Application`` instance and its
config dict.

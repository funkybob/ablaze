# ablaze
A veneer over aiohttp to make life less tedious


# Creating an app

1. Create a config.ini
   ```
   [main]
   modules=models,templates

   [templates]
   paths=templates/

   [models]
   apps=auth,page
   ```

2. Create an app

   ```python
   import os
   import ablaze

   BASE_DIR = os.path.dirname(os.path.abspath(__file__))

   ablaze.launch(os.path.join(BASE_DIR, 'config.ini'))
   ```

# How it works

First, the config file is loaded and stashed on the app instance as
`app['config']`.

Then, each module listed in [main]->modules is imported, and its `setup`
coroutine is invoked, passed the `app` instance.

Each module can gather its config from the `app['config']` ConigParser instance.

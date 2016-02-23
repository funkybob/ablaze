# ablaze
A veneer over aiohttp to make life less tedious


# Creating an app

1. Create a config.ini

   [main]
   modules=models,templates

   [templates]
   paths=templates/

   [models]
   apps=auth,page

2. Create an app

   import os
   import ablaze

   BASE_DIR = os.path.dirname(os.path.abspath(__file__))

   ablaze.launch(os.path.join(BASE_DIR, 'config.ini'))

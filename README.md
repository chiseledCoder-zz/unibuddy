#### Coding Challenge from Unibuddy

the_app.views consists of both the tasks

#### Installation:
1. clone the repo
2. create virtualenv
2. activate virtualenv
3. run pip install -r requirements.txt
4. run python -m the_app/views.py

##### Alternative installation:
to run it in django locally follow:
1. create virtualenv 
2. activate virtualenv
3. run pip install -r requirements.txt 
4. run ./manage.py migrate
5. run ./manage.py runserver
Before running the server, change return type from json.dumps() to JsonResponse().

##### Dependencies:
- [Requests](https://requests.readthedocs.io/en/master/)

to make the entire local application available to anywhere in the world, then 
install [ngrok](https://ngrok.com/)
after installation run `ngrok http 8000`
ngrok will provide a url which can be shared with anyone.


#### Future Implementations:
- Correction of typos in query using [pyspellchecker](https://pypi.org/project/pyspellchecker/).
- Avoid redundancy of summary.
- Improved search algorithm for only unique words.
 
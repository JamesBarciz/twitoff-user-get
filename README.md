# Lambda School TwitOff: Tweepy Development Assistance

The purpose of this application is to assist students in the Lambda School Data Science curriculum who are having
trouble obtaining Twitter Developer credentials for the Unit 3 _TwitOff_ application.

With the above credentials, we can obtain user-created Tweets using the `tweepy` package and render them at an endpoint
as JSON for students to work with.

### DISCLAIMER:
The developer credentials used in this application are read-only and ***will not*** post Tweets to Twitter.
The purpose of the _TwitOff_ application made in Unit 3 - Sprint 3 is to decide - using _Logistic Regression_ - who is
more likely to say a user-created Tweet based on the last 200 Tweets of two or more Twitter users.

## [The Application](https://lambda-ds-twit-assist.herokuapp.com/)

### Tech Stack

This application uses _Python 3.8.5_ and is built using the _[FastAPI](fastapi.tiangolo.com)_ framework.  While we spent
the entirety of Sprint 3 learning _[Flask](flask.palletsprojects.com)_, I decided FastAPI would be better in this
scenario because the purpose of this application is to display user Tweets as JSON at an endpoint.

_[Tweepy](https://docs.tweepy.org/en/latest/)_ is used in this application - needing Twitter Developer credentials - to
connect to the Twitter API, so we can obtain user Tweets.

In order to deploy this application to _[Heroku](heroku.com)_, we need the assistance of an ASGI server called
_[Uvicorn](https://www.uvicorn.org/)_.

### Directory Structure

---
```
├─ app                    → App Directory
│   ├─ tests              → Tests (probably not needed - came with template)
│   │    ├─ __init__.py
│   │    └─ test_main.py
│   │
│   ├─ __init__.py
│   ├─ main.py            → Main Application
│   ├─ twitter.py         → Connects to Twitter API
│   └─ user.py
│
├─ .gitignore
├─ LICENSE
├─ Pipfile
├─ Procfile
├─ README.md
└─ requirements.txt
```
---

### How it Works:

The `twitter.py` file makes a call to the Twitter API for a user, and their Twitter timeline.

At an endpoint, we take the pertinent info needed for our 
_[Flask-SQLAlchemy ORM](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)_ on the _TwitOff_ app end and build it
into a dictionary to be rendered as JSON.

In order to obtain any user, you only need to add the route `/user/` to the end of the Heroku URL in addition to the
Twitter handle of any Twitter user.  For example, if we want Tweets by Elon Musk, we would need to type in the browser
`/user/elonmusk` - try it out for yourself by following this
[link](https://lambda-ds-twit-assist.herokuapp.com/user/elonmusk) (this app uses free Heroku Dynos therefore, the app
could take a while to spin up), you may have to refresh the page if an empty list of Tweets is displayed.

#### _Side Note_:

Even though I say you may need to refresh if you get an empty list of Tweets at the endpoint, if it remains empty, it is
entirely possible that the user's last 200 entries of activity in their timeline have only been Retweets or replies to
other Tweets.  In this case, __your user will not have any Tweets displayed at this endpoint and therefore, you should
seek out another user__.

### What Should You Do Next?

Now that we have the Tweets displayed as JSON at an endpoint, all one needs to do is use the `requests` package to
obtain the text at that endpoint.  For simplicity's sake, I have included a script that will assist in doing this which
I will explain afterwards.

```python3
import requests
import ast

from .model import DB, User, Tweet


def get_user_and_tweets(username):

    HEROKU_URL = 'https://lambda-ds-twit-assist.herokuapp.com/user/'

    user = ast.literal_eval(requests.get(HEROKU_URL + username).text)

    try:
        if User.query.get(user['twitter_handle']['id']):
            db_user = User.query.get(user['twitter_handle']['id'])
        else:
            db_user = User(id=user['twitter_handle']['id'],
                           name=user['twitter_handle']['username'])
        DB.session.add(db_user)

        for tweet in user['tweets']:
            db_tweet = Tweet(id=tweet['id'], text=tweet['full_text'])
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
    except Exception as e:
        raise e
    else:
        DB.session.commit()
```

The process is put into a single function which accepts a username in the form of a Twitter handle (excluding the `@`)

As stated above, you need the `requests` package to get the text out of the endpoint however, since the JSON will be
rendered in Python as a string, we will also use the `ast` library to 'de-stringify' the JSON and turn it back into a
regular old Python dictionary.

Depending on the name of your script containing your Flask-SQLAlchemy ORM, you may need to change 
`from .model import ...` to something else - convention for this course has always called the script `model.py` as well
as use `DB` for the database, `User` and `Tweet` for the table names.

For those unfamiliar with sourcing a value from keys in a dictionary, the shorthand way of doing it is to type out the
variable name for the `dict` object and put the name of the keys needed one at a time in square brackets.  For example,
in our output below, we have some information on the Twitter user Lewis Black 
([@TheLewisBlack](https://twitter.com/TheLewisBlack)):

```JSON
{"twitter_handle":{"username":"TheLewisBlack","id":344955115}, "tweets": ...}
```

To obtain the username and user ID from this nested dictionary, we would first use the key `"twitter_handle"` followed
by the `"username"` or `"id"` as demonstrated below assuming it is contained in a variable called `userJSON`.

```python3
userJSON['twitter_handle']['username'] --> "TheLewisBlack"
userJSON['twitter_handle']['id']       --> 344955115
```

### For the Flask Application

To start with, I would suggest adding the below to your Flask Application.

```python3
@app.route('/user', methods=['GET'])
def add_user():
    twitter_handle = request.args['twitter_handle']
    get_user_and_tweets(twitter_handle)
    return 'User added'
```

At the `/user` route in your browser, you can add a query string to input the username.  For example, to make a request
to get Lewis Black's Tweets, you would type in your browser the route and query string:
`/user?twitter_handle=TheLewisBlack`

### Closing

In the future, this application may be hosted elsewhere as we are using the free tier of Heroku and the application will
sleep after a brief time of not using it.

If there are any questions regarding this application or suggested fixes, feel free to make a Pull Request or email me
at `james.barciz@lambdaschool.com`
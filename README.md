# Oso Python Quickstart

Follow along [here](https://docs.osohq.com/getting-started/quickstart.html).

## Instructions

1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the server: `FLASK_APP=app.server python -m flask run`

## Make some changes

If you visit
[http://localhost:5000/repo/gmail/user1/delete](http://localhost:5000/repo/gmail/user1/delete), you
should get a 200 response. If you visit
[http://localhost:5000/repo/react/user1/delete](http://localhost:5000/repo/react/user1/delete), you
should see a message permission deny.

[http://localhost:5000/repo/react/user1/read](http://localhost:5000/repo/react/user1/read), you
should get a 200 response, bscause the `react` repo is marked as public

[http://localhost:5000/repo/user1](http://localhost:5000/repo/user1), you should see repo you
can read it, include public repo and your repo

[http://localhost:5000/repo/react](http://localhost:5000/repo/react), you should
see a proper 200 response, because the `react` repository is marked as public
in `app/models.py`.

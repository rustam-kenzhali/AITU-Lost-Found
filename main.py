# pip instal Flask, flask-login, flask-sqlalchemy
from website import create_app

app = create_app()

if __name__ == '__main__':  # only if we run main.py, not if we import this file
    app.run(debug=True)     # we execute this line
    # debug = True : mean that every change in the code automaticli rerun the webserver
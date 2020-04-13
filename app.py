from flask import Flask, render_template
from data import db_session
app = Flask(__name__)


@app.route('/')
def default():
    return render_template('index.html')


if __name__ == '__main__':
    db_session.global_init('db/lets_blog.db')
    # app.run(host='127.0.0.1', port=8900)

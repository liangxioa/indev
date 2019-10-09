# coding:utf-8
from flask import Flask, request

from controller import userController

app = Flask(__name__)

app.register_blueprint(userController.userRouter)


@app.route('/')
def index():
    return '404'



if __name__ == '__main__':
    app.run()

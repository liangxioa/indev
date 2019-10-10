# coding:utf-8
import sys

from flask import Blueprint, request
from model import userModel

userRouter = Blueprint('user', __name__, url_prefix="/user")  # 蓝图的对象的名称=Blueprint('自定义蓝图名称',__name__)

'''
返回数据的默认格式
'''
returnData = {"data": None, "msg": "请求失败", "success": False}

'''
用户登录

:param username: 用户名
:param password: 用户密码
:return: 返回值为returnData
'''


@userRouter.route('/login', methods=["POST"])
def login():
    username = request.form['username']
    password = request.form["password"]
    try:
        result = userModel.login(username, password)
        if result:
            returnData["msg"] = "登录成功"
            returnData["success"] = True
        else:
            returnData["msg"] = "账号或密码不正确"
    except:
        returnData["msg"] = "登录失败"
        print("Unexpected error:", sys.exc_info()[0])
    return returnData


'''
用户注册

:param username: 用户名
:param password: 用户密码
:return: 返回值为returnData
'''


@userRouter.route('/reg', methods=["POST"])
def reg():
    username = request.form['username']
    password = request.form["password"]
    try:
        hasUser = userModel.getUserIDByUserName(username)  # 查询该用户名是否存在
        if hasUser:
            returnData["msg"] = "该用户已存在"
        else:
            try:
                result = userModel.insertUser(username, password)  # 创建新用户
                print(result)
                if result:
                    returnData["msg"] = "注册成功"
                    returnData["success"] = True
                else:
                    returnData["msg"] = "注册失败"
            except:
                returnData["msg"] = "注册失败"
                print("错误：创建新用户报错，错误信息：", sys.exc_info()[0])
    except:
        returnData["msg"] = "注册失败"
        print("错误：查询用户名是否存在报错，错误信息：", sys.exc_info()[0])

    return returnData

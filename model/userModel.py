# coding:utf-8
from util import MyDbUtils

mysql = MyDbUtils.Mysql()


def login(username, password):
    sql = "SELECT id FROM user WHERE username=%s and password=%s"
    result = mysql.selectone(sql, [username, password])
    return result


def insertUser(username, password):
    sql = "INSERT INTO user (username,password) VALUES (%s,%s)"
    result = mysql.insert(sql, (str(username), str(password)))
    return result


def getUserById(id):
    sql = "SELECT * FROM user WHERE id=%s"
    result = mysql.selectone(sql, id)
    return result


def getUserIDByUserName(username):
    sql = "SELECT id FROM user WHERE username=%s"
    result = mysql.selectone(sql, username)
    return result

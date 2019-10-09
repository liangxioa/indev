# coding:utf-8
from util import DB_pool as db


def login(username, password):
    sql = "SELECT id FROM user WHERE username=%s and password=%s"
    result = db.getOne(sql, [username, password])
    return result


def insertUser(username, password):
    sql = "INSERT INTO user (username,password) VALUES (%s,%s)"
    result = db.insertOne(sql, [username, password])
    return result


def getUserById(id):
    sql = "SELECT * FROM user WHERE id=%s"
    result = db.insertOne(sql, [id])
    return result

def getUserIDByUserName(username):
    sql = "SELECT id FROM user WHERE username=%s"
    result = db.insertOne(sql, [username])
    return result

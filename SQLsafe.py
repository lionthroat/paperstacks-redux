from app import app
from flaskext.mysql import MySQL
from db import mysql
import time
import pymysql
import pymysql.cursors
from flask import Flask, Response, render_template
from flask import request, redirect

def fetch(query = None, query_params = ()):
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query, query_params)
    connection.commit() # equivalent of saving database changes
    dictionary = cursor.fetchall()
    cursor.close()
    connection.close()

    return dictionary

def db_update(query = None, params = ()):
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query, params)
    connection.commit() # equivalent of saving database changes
    cursor.close()
    connection.close()

    return

def stringsafe(string):
    quotes = "\""
    escaped_quotes = "\\\""
    quote = "\'"
    escaped_quote = "\\\'"
    string = string.replace(quotes, escaped_quotes)
    string = string.replace(quote, escaped_quote)
    return string

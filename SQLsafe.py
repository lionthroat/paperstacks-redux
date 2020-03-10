from app import app
from flaskext.mysql import MySQL
from db import mysql
import time
import pymysql
import pymysql.cursors
from flask import Flask, Response, render_template
from flask import request, redirect

def fetch(query = None, query_params = ()):
    if query is None or len(query.strip()) == 0:
        print("query is empty! Please pass a SQL query in query")
        return None

    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute(query, query_params)

    connection.commit() # the equivalent of saving your database changes

    dictionary = cursor.fetchall()

    cursor.close()
    connection.close()

    return dictionary

def stringsafe(string):
    quotes = "\""
    escaped_quotes = "\\\""
    quote = "\'"
    escaped_quote = "\\\'"
    string = string.replace(quotes, escaped_quotes)
    string = string.replace(quote, escaped_quote)
    return string

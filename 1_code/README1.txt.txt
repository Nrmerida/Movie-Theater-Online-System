to run my code you need to setup mysql make / change these connection types of all of them or make the server exactly like this 
host='localhost',
database='movie_theater_storage',
 user='root',
 password='turbo'

Then import the tables provided in .sql files

get the following imports/addons in your preffered way
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error

now once everything is setup the only thing you have to do is go to whatever your local host is running on the web browser and run app.py and the website should launch

The test login I made is a username of 2 and a PW of 2
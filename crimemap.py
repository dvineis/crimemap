from __future__ import print_function
#from dbhelper import DBHelper
import dbconfig
#if dbconfig.test:
#from mockdbhelper import MockDBHelper as DBHelper
#else:
#from dbhelper import DBHelper
from dbhelper import DBHelper
from flask import Flask
from flask import render_template
from flask import request
import json
import datetime
import dateparser
import os
import string


app = Flask(__name__)
DB = DBHelper()
categories = ['mugging', 'break-in']

#format date function
def format_date(userdate):
    date = dateparser.parse(userdate)
    try:
        return datetime.datetime.strftime(date, "%Y-%m-%d")
    except TypeError:
        return None
## sanitize the description inpout field
#make new validation error
def sanitize_string(userinput):
    whitelist = string.ascii_letters + string.digits + " !?$.,;:-'()&"
    return [x for x in userinput if x in whitelist]

@app.route("/")
def home(error_message=None):
    crimes = DB.get_all_crimes()
    crimes = json.dumps(crimes)
    return render_template("home.html", crimes=crimes, categories=categories, error_message=error_message)


    
@app.route("/submitcrime", methods=['POST'])
def submitcrime():
    category = request.form.get("category")
    date = request.form.get("date")
    try:
        latitude = float(request.form.get("latitude"))
        longitude = float(request.form.get("longitude"))
    except ValueError:
        return home()
    category = request.form.get("category")
    if category not in categories:
        return home()
    date = format_date(request.form.get("date"))
    if not date:
        return home("Invalid date. Please use yyyy-mm-dd format")
    #description = sanitize_string(request.form.get("description"))
    description = request.form.get("description")
    DB.add_crime(category, date, latitude, longitude, description)
    return home()

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

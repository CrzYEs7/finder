import csv
import datetime
import pytz
import requests
import urllib
import uuid

from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def guess_manufacturer(reference):
    """Guess and return the manufacturer name of each part by the first digits of their reference"""
    for manufacturer in brands_list_check:
        for begin in brands_list_check[manufacturer]:
            reference = str(reference).strip().lower()
            if reference.startswith(begin):
                return manufacturer

# initial of the references by manufacturers
brands_list_check = {
    'bosch':['f026', 'f01', 'f00', '1457', '0986', '0445', '0281', '1987', '2467'],
    'spidan':['sp-'],
    'valeo':['vl'],
    'trw':['jar', 'jte', 'jts', 'gdb', 'jts', 'jbu', 'jbj', 'pfb', 'pmf'],
    'ina':['532', '535', '534', '533', '531'],
    'opel':['6/'],
    'peugeot':['p'],
    '3rg':['3rg'],
    'diversos':['kr', 'ab', 'cc', 'hr', 'tz', 'ack'],
    'motul':['mt'],
    'indieparts':['ip-'],
    'elring':['er'],
    'purflux':['fcs'],
    'mahle':['lx', 'kx', 'ox', 'oc', 'kc', 'kl', 'la', 'lak', 'oz', 'hx'],
    'nrf':['nrf'],
    'fare':['far']
}

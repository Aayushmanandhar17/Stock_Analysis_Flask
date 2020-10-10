import flask
from flask import render_template, jsonify,json
import pandas as pd
import datetime
import pandas_datareader.data as web
class visual_class:
    company_name="TSLA"
    close_price=0
    def __init__(self):

        print("Constructor created")

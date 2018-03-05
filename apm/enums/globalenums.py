"""Define all global enumerations
Such as: default status value, default datetime etc.
Different from config.py
"""
from datetime import datetime

#PORT for this application
DEFAULT_PORT = 6688
#index page for this application, value is 'blueprint_name.function_name'
DEFAULT_INDEX = 'user.user_login'

#default value for status column in database
DEFAULT_STATUS_VALUE = '1'
#default value for 'xxx_date' column in database
DEFAULT_DATETIME = datetime.now()

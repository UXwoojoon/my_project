# /weather_api.py
import requests
from datetime import datetime, timedelta

datetoday = datetime.today()
DT = datetoday.strftime("20%y.%m.%d")
print(DT)
from datetime import datetime, timedelta
from django.conf import settings
import requests


EXECUTION_TIME = datetime.strptime(settings.EXECUTION_TIME, "%H:%M:%S").time()

def schedule_api():
	end_time = (datetime.combine(datetime.today(), EXECUTION_TIME) + timedelta(minutes=5)).time()
	current_time = datetime.now().time()
	if EXECUTION_TIME <= current_time <= end_time:
		response = requests.post(f"http://{settings.SERVER_DOMAIN}/send_reminder")

	else:
		print(f"\n skipping {current_time=}")


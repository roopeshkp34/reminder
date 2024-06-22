from django.shortcuts import render
from django.http.response import JsonResponse
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from reminder.models import Person, LastDone,Token
from reminder.helper import send_mail, generate_random_token

'''
Basic view for displaying our scheduled job
'''
def index(request):
	return render(request, 'index.html')

@csrf_exempt
def send_notification(request):
	# if request.user.is_authenticated:
		if request.method == "POST":
			try:
				last_done = LastDone.objects.filter(is_active=True).latest("created_at")
				today = timezone.now().date()
				if last_done.created_at.date() == today:
					return JsonResponse({"success": False, "message": "Already sent the mail"})
				
			except LastDone.DoesNotExist:
				last_done = None

			all_persons = Person.objects.order_by("first_name")
			if last_done:
				next_person = all_persons.filter(first_name__gt=last_done.person_id.first_name).first()
				if not next_person:
					next_person = all_persons.filter().first()
			else:
				next_person = all_persons.filter().first()
			token = generate_random_token()
			Token.objects.create(token=token, person_id=next_person)
			send_mail(to_email=next_person.email, name=next_person.first_name, token=token)
			
			new_obj = LastDone()
			new_obj.person_id = next_person
			new_obj.save()


			return JsonResponse({"success": True})
		else:
			return JsonResponse({"success": False, "message": "Method not allowed"})
	# else:
	# 	return JsonResponse({"success": False, "message": "Unauthorized"})

@csrf_exempt
def not_available(request, token):
	if request.method == "GET":
		token_obj = Token.objects.get(token=token)
		if not token_obj:
			return render(request, 'index.html', {"success": False, "message": "Invalid Token"})
		token_obj.is_read = True
		token_obj.save
		return render(request, 'index.html', {"success": True,})
	else:
		return render(request, 'index.html', {"success": False, "message": "Method not allowed"})

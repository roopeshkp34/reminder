from django.shortcuts import render
from django.http.response import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from reminder.models import Person, LastDone,Token
from reminder.helper import generate_message_for_initial, generate_random_token, generate_message_for_re_assign

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
			generate_message_for_initial(to_email=next_person.email, name=next_person.first_name, token=token)
			
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
		token_obj = Token.objects.filter(token=token, is_active=True).first()
		if not token_obj:
			return render(request, 'not_available.html', {"success": False, "message": "Invalid Token"})
		token_obj.is_read = True
		token_obj.save()
		return render(request, 'not_available.html', {"success": True,})
	else:
		try:
			token_obj = Token.objects.filter(token=token, is_read=True, is_active=True).first()
			if not token_obj:
				return JsonResponse({"success": False, "message": "Invalid Token"})

			reason = request.POST["reason"]
			if not reason:
				return JsonResponse({"success": False, "message": f"Key error"})
			today = timezone.now().date()
			today_entries = LastDone.objects.filter(created_at__year=today.year, created_at__month=today.month, created_at__day=today.day).all()


			if today_entries.count() >= Person.objects.filter(is_active=True).count() - 1:
				return JsonResponse({"success": False, "message": "Sorry! You can't skip today."})

			last_done = LastDone.objects.filter(person_id=token_obj.person_id).latest("created_at")
			all_persons = Person.objects.order_by("first_name")
			next_person =all_persons.filter(first_name__gt=last_done.person_id.first_name).first()
			if not next_person:
				next_person = all_persons.filter().first()
			token = generate_random_token()
			Token.objects.create(token=token, person_id=next_person)
			generate_message_for_re_assign(name=next_person.first_name, to_email=next_person.email, token=token, pervious_person=last_done.person_id.first_name)

			last_done.not_done_reason = reason
			last_done.save()

			token_obj.is_active = False
			token_obj.save()

			new_obj = LastDone()
			new_obj.person_id = next_person
			new_obj.save()
			

			return JsonResponse({"success": True, "message": "Success"})
		except Exception as e:
			return JsonResponse({"success": False, "message": str(e)})


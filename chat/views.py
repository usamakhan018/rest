from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Chat
from itertools import chain
from .utils import get_or_create_chat
from articles.decorators import ajax_required
from django.http import JsonResponse
from account.models import Account
@login_required
def chat_view(request, user_id):
	context = {}
		
	room1 = Chat.objects.filter(user1=request.user, is_active=True)
	room2 = Chat.objects.filter(user2=request.user, is_active=True)

	rooms = list(chain(room1, room2))
	other_users = []
	for room in rooms:

		other_user = room.user1
		if other_user == request.user:
			other_user = room.user2
			other_users.append(other_user)
	print(other_users)
	context['other_users'] = other_users
	return render(request, 'chat/chat.html', context)

@ajax_required
def get_or_create_chat_view(request):
	context = {}
	user = request.user

	user_id = request.POST.get('user_id')
	if user_id:
		try:
			account = Account.objects.get(pk=user_id)
		except Account.DoesNotExist:
			return JsonResponse({'status': 'error', 'header': 'error', 'data': 'account id not correct'})
		chat = get_or_create_chat(user1=user, user2=account)
	return JsonResponse({'status': 'ok', 'header': 'ok', 'data': 'success', 'chat_id': str(chat.id)})
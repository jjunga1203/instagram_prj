from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.db.models import Q
from accounts.models import User

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user)
    contents = []

    for notify in notifications:

        msg_user = User.objects.get(pk=notify.msg_user_id)

        contents.append( {
            'user_img': msg_user.profile_url,
            'msg': notify.message,
            'created_at': notify.created_at,
        })
            

    context = {
        'contents': contents
        }
    return render(request, 'notifications/notifications.html', context)

from .models import Notification

def unread_notifications_count(request):
    """
    Ajoute le nombre de notifications non lues au contexte de chaque requête.
    """
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
    else:
        count = 0
    return {'unread_notifications_count': count}
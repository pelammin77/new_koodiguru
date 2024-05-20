from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

def delete_unactivated_users():
    print("Hep")
    User = get_user_model()
    time_threshold = timezone.now() - timedelta(hours=1)
    
    unactivated_users = User.objects.filter(date_joined__lt=time_threshold, is_active=False)
   #count = unactivated_users.count()
    
    unactivated_users.delete()
    # kirjoitetaan logia 
    
    #print(f"Poistettiin {count} ei-aktivoitunutta käyttäjää.")

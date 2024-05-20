from django.contrib.auth import get_user_model
from main_app.models import UserTask, Task

User = get_user_model()

# Käydään läpi kaikki käyttäjät
for user in User.objects.all():
    # Lasketaan käyttäjän pisteet
    total_points = 0
    solved_tasks = UserTask.objects.filter(user=user, status='solved')
    for user_task in solved_tasks:
        task = Task.objects.get(id=user_task.task_id)
        total_points += task.points

    # Päivitetään käyttäjän pisteet
    user.points = total_points
    user.save()
    print(f"Käyttäjän {user.username} pisteet päivitetty: {total_points}")

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from datetime import datetime
from django.utils import timezone
from embed_video.fields import EmbedVideoField


def get_default_category():
    return TutorialCategory.objects.get_or_create(name="Pythonin perusteet")[0].id


def get_default_task_category():
    return TaskCategory.objects.get_or_create(name="Tulostus")[0].id


def get_empty_list():
    return []


# Create your models here.
class UserRole(models.TextChoices):
    TESTER = "tester", "Testaaja" 
    TEACHER = "teacher", "Opettaja"
    STUDENT = "student", "Oppilas"
    ADMIN = "admin", "Admin"

from django.conf import settings

class User(AbstractUser):
    
    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)

    user_permissions = models.ManyToManyField(
        Permission, blank=True, related_name="custom_user_permissions"
    )
    first_name = models.CharField("Etunimi", max_length=30)
    last_name = models.CharField("Sukunimi", max_length=30)
    role = models.CharField(
        max_length=20, choices=UserRole.choices, default=UserRole.STUDENT
    )
    email = models.EmailField("Sähköposti", unique=True)
    change_password = models.BooleanField(default=False)
    premium_start = models.DateTimeField(null=True, blank=True)
    premium_end = models.DateTimeField(null=True, blank=True)
    editor_theme = models.CharField(max_length=100, default="default")
    points = models.IntegerField(default=0, verbose_name="Pisteet")
    level = models.IntegerField(default=0, verbose_name="Taso")
    LEVEL_THRESHOLDS = [50, 150, 200, 500, 800]
    # created_at = models.DateTimeField(auto_now_add=True)

    @property
    def level_icon_url(self):
        # Määritellään tasojen ja vastaavien ikonien polut
        icons = {
            0: 'img/user_level_icons/ beginner_level_icon_small.png',
            1: 'img/user_level_icons/new_harjoittelija_logo_small.png',
            2: 'img/user_level_icons/kehittaja_logo_small.png',
            3: 'img/user_level_icons/metari_taso_logo_small.png',
            4: 'img/user_level_icons/guru_tason_logo_small.png',
            5: 'img/user_level_icons/legend_level_logo_small.png',
            # Lisää tarvittaessa
        }
         # Yritä hakea ikonin polku käyttäjän nykyiselle tasolle
        icon_path = icons.get(self.current_level)
        if icon_path:
               return f"{settings.STATIC_URL}{icon_path}"
        else:
            return None



    @property
    def is_premium(self):
        now = timezone.now()
        return (
            self.premium_start is not None
            and self.premium_end is not None
            and self.premium_start <= now <= self.premium_end
        )
    
    def level_name(self):
        level_names = {
            0: 'Aloittelija',
            1: 'Harjoittelija',
            2: 'Kehittäjä',
            3: 'Mestari',
            4: 'Guru',
            5: 'Legenda',
            
            # Voit lisätä lisää tasojen nimiä tarpeen mukaan
        }
        # Käytä `current_level`-propertyä tason nimen hakemiseen
        return level_names.get(self.current_level, 'Tuntematon taso')
    
   
    @property
    def current_level(self):
        # Määrittele tasojen kynnysarvot tässä, poista ensimmäinen arvo 0,
        # koska kaikki käyttäjät alle 50 pistettä ovat automaattisesti tasolla 0.
        
        
        # Käyttäjä on automaattisesti tasolla 0, jos pisteet ovat alle ensimmäisen kynnysarvon.
        level = 0
        for threshold in User.LEVEL_THRESHOLDS:
            if self.points >= threshold:
                level += 1
            else:
                break
        return level
    
    @property
    def progress_percentage(self):
       
        current_level_index = self.current_level - 1  # Oletetaan, että level_index alkaa 0:sta
        if current_level_index < 0:
            # Jos käyttäjä on aloittelijan tasolla, palautetaan suoraan pisteiden prosentuaalinen osuus ensimmäisestä kynnyksestä
            return (self.points / User.LEVEL_THRESHOLDS[0]) * 100
        elif current_level_index >= len(User.LEVEL_THRESHOLDS) - 1:
            # Jos käyttäjä on saavuttanut korkeimman tason, palautetaan 100%
            return 100
        else:
            # Lasketaan edistyminen nykyisen ja seuraavan tason välillä
            previous_level_threshold = User.LEVEL_THRESHOLDS[current_level_index]
            next_level_threshold = User.LEVEL_THRESHOLDS[current_level_index + 1]
            progress_within_level = (self.points - previous_level_threshold) / (next_level_threshold - previous_level_threshold)
            return progress_within_level * 100

    def add_points(self, points):
        # Funktio pisteiden lisäämiseksi käyttäjälle
        self.points += points
        self.save()

    def __str__(self):
        return self.username
    
    
    @property
    def completed_tasks_count(self):
        return self.usertask_set.filter(status='solved').count()

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_staff = True  # Sallii pääsyn admin-sivustolle
            self.role = UserRole.ADMIN  # Jos päätät ottaa role-kentän takaisin käyttöön
        super().save(*args, **kwargs)




class TutorialCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



from PIL import Image


from ckeditor.fields import RichTextField


class Tutorial(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField()
    content = RichTextField()
    category = models.ForeignKey(
        TutorialCategory, on_delete=models.CASCADE, default=get_default_category
    )
    # course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    # video = EmbedVideoField()  # same like models.URLField()
    video_url = models.URLField(blank=True, null=True)
    tutorialLogo = models.ImageField(
        upload_to="tuto_logos/", default="tuto_logos/default_tuto.png"
    )

    def __str__(self):
        return self.title


class TaskCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name







class Course(models.Model):
    courseTitle = models.CharField(max_length=200)
    coursePublishDate = models.DateTimeField("Luontipäivä", default=datetime.now)
    courseDescription = models.TextField()
    prerequisites = models.TextField(default="Ei esitietoja")  # esitiedot
    is_premium = models.BooleanField(default=False)
    is_all_free = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    is_test_state = models.BooleanField(default=False)
    tutorials = models.ManyToManyField(Tutorial, related_name="courses", blank=True)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="creator_id",  # Lyhyempi nimi sarakkeelle
    )
    courseLogo = models.ImageField(
        upload_to="course_logos/", default="course_logos/no_logo.png"
    )

    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.courseTitle






class Task(models.Model):
    LANGUAGE_CHOICES = [
        ("Python", "Python"),
        ("Java", "Java"),
        ("Javascript", "JavaScript"),
        ("C", "C"),
        ("C++", "C++"),
        ("C#", "C#"),
        ("Pseudo", "Pseudo"),
	("Vaativuuslakelmat","vaativuuslaskelmat"),

        # add more programming languages if needed
    ]

    DIFFICULTY_CHOICES = [
        ("aloittelija", "Aloittelija"),
        ("harjoittelija", "Harjoittelija"),
        ("kehittäjä", "Kehittäjä"),
        ("mestari", "Mestari"),
        ("guru", "Guru"),
    ]
    
    DIFFICULTY_POINTS = {
        "aloittelija": 1,
        "harjoittelija": 2,
        "kehittäjä": 3,
        "mestari": 4,
        "guru": 5,
    }
    

    taskTitle = models.CharField(max_length=200)
    taskPublishDate = models.DateTimeField("Publish date")
    taskDescription = models.TextField()
    taskStarterCode = models.TextField(null=True)
    taskInputs = models.TextField(null=True, blank=True, default=get_empty_list)
    language = models.CharField(
        max_length=20, choices=LANGUAGE_CHOICES, default="Python"
    )
    difficulty = models.CharField(
        max_length=20, choices=DIFFICULTY_CHOICES, default="aloittelija"
    )
    
    @property
    def points(self):
        """Palauttaa tehtävän vaikeustason mukaiset pisteet."""
        return self.DIFFICULTY_POINTS.get(self.difficulty, 0)
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    tutorial = models.ForeignKey(
        Tutorial, on_delete=models.SET_NULL, null=True, blank=True
    )
    category = models.ForeignKey(
        TaskCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=get_default_task_category,
    )
    video_url = models.URLField(blank=True, null=True)
    is_free = models.BooleanField(default=True)
    is_hidden = models.BooleanField(default=False)
    run_tests = models.BooleanField(default=True)
    

    def __str__(self):
        return self.taskTitle


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Answer(models.Model):
    answerText = models.TextField()  # mallivastaus esi koodi
    answerOutput = models.TextField()
    answerPublishDate = models.DateTimeField("Publish date", default=datetime.now)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    answerTuto = models.TextField(null=True, blank=True)
    aswerVideo = models.URLField(blank=True, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"Vastaus tehtävään: {self.task.taskTitle}"


class TaskTest(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    test_code = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Test for {self.task.taskTitle}"


# suosikki kurssit
class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


# tekeilä olevat kurssit
class OngoingCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


# suoritetut kurssit
class PerformedCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class UserTask(models.Model):
    STATUS_CHOICES = [
        ("started", "Aloitettu"),
        ("solved", "Ratkaistu"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ["user", "task"]
        db_table = "user_task"  # Lyhyempi nimi taululle
        constraints = [
            models.UniqueConstraint(
                fields=["user", "task"],
                name="user_task_uniq",  # Lyhyempi nimi rajoitteelle
            )
        ]

    def __str__(self):
        # Return a string representation combining user and task
        return f"{self.user} - {self.task} - {self.status}"


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    answer = models.TextField()

    class Meta:
        unique_together = ["user", "task"]

    def __str__(self):
        # Return a string representation combining user and the related task
        return f"{self.user} - {self.task}"

    def save(self, *args, **kwargs):
        # Poista tyhjät merkit vastauksesta ennen tallennusta
        self.answer = self.answer.strip()
        self.answer = self.answer.strip("\n")
        super(UserAnswer, self).save(*args, **kwargs)

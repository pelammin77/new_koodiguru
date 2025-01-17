from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.db import models
from ckeditor.widgets import CKEditorWidget
from django import forms

class CourseAdmin(admin.ModelAdmin):
    list_display = ['courseTitle', 'creator', 'coursePublishDate']  # Määrittele, mitä kenttiä haluat näyttää admin-listaussivulla
    exclude = ['creator',]  # Jätä 'creator' kenttä pois admin-lomakkeesta
    filter_horizontal = ('tutorials',)  # Mahdollistaa tutoriaalien valitsemisen käyttöliittymässä

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Tarkistetaan, onko objekti uusi (ei vielä tallennettu)
            obj.creator = request.user  # Aseta kurssin luojaksi nykyinen käyttäjä
        super().save_model(request, obj, form, change)  # Kutsu yliluokan save_model metodia tallentamaan objekti



class UserAdmin(UserAdmin):
    # Päivitetään olemassa olevien käyttäjien muokkausnäkymä sisältämään 'role'
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'role')}),  # Lisätty 'role' tänne
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 
                                       'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Päivitetään uusien käyttäjien luontinäkymä sisältämään 'role'
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'role')}),  # Lisätty 'role' tänne
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 
                                       'groups', 'user_permissions')}),
    )

    # Lista näytettävistä kentistä käyttäjälistauksessa
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    # Kentät, joiden mukaan käyttäjälistauksessa voi suodattaa
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'groups')



class AnswerInline(admin.StackedInline): 
    model = Answer
    extra = 1  # kuinka monta tyhjää vastauskenttää haluat näkyvän oletuksena

class TestInline(admin.StackedInline):
    model = TaskTest
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "answer":
            # Olettaen, että olet TaskAdminin muokkausnäkymässä
            task_id = request.resolver_match.kwargs.get('object_id')
            if task_id:
                kwargs["queryset"] = Answer.objects.filter(task_id=task_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class TaskAdmin(admin.ModelAdmin):
    inlines = [AnswerInline, TestInline]

   
    fieldsets = (
        (('Task info'), {'fields': ('taskTitle', 'taskPublishDate', 'taskDescription', 'taskStarterCode', 'taskInputs', 'language', 'difficulty', 'course', 'category', 'is_free', 'video_url')}),
        (('Tutorials'), {'fields': ('tutorial',)}),
    )

class TaskInline(admin.StackedInline):
    model = Task
    extra = 0  # kuinka monta tyhjää tehtäväkenttää haluat näkyvän oletuksena

class TutorialAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Tutorial
        fields = '__all__'


class TutorialAdmin(admin.ModelAdmin):
    inlines = [TaskInline]

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_posted']  # Määrittele tässä, mitä kenttiä haluat näyttää admin-listaussivulla
    exclude = ['author',]  # Jätä 'author' kenttä pois admin-lomakkeesta

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Tarkistetaan, onko objekti uusi (ei vielä tallennettu)
            obj.author = request.user  # Aseta author-kenttä nykyiseksi käyttäjäksi
        super().save_model(request, obj, form, change)  # Kutsu yliluokan save_model metodia tallentamaan objekti



admin.site.register(User, UserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(UserCourse)
admin.site.register(UserTask)
admin.site.register(UserAnswer)
admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(TutorialCategory)
admin.site.register(TaskCategory)
admin.site.register(Post, PostAdmin)

class LambdaUsageAdmin(admin.ModelAdmin):
    list_display = ['user', 'task', 'timestamp']
    list_filter = ['user', 'task', 'timestamp']
    search_fields = ['user__username', 'task__taskTitle']
    ordering = ['-timestamp']

admin.site.register(LambdaUsage, LambdaUsageAdmin)

class LambdaUsageStatsAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_executions', 'executions_today', 'last_execution']
    list_filter = ['last_execution_date']
    search_fields = ['user__username']
    ordering = ['-total_executions']
    readonly_fields = ['total_executions', 'last_execution', 'executions_today', 'last_execution_date']

admin.site.register(LambdaUsageStats, LambdaUsageStatsAdmin)


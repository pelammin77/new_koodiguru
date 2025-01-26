import jwt
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .forms import NewUserForm, CustomUserChangeForm, PasswordCheckForm
from django.contrib import messages
from django.contrib.auth import views as auth_views
import signal
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.encoding import force_str
from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

import main_app.CodeRunner as runner 
import logging
#from code_runner.views import run_python_code
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import get_user_model
import io
import sys
from diff_match_patch import diff_match_patch
import jwt
from datetime import datetime, timedelta

from .models import (
    UserRole,
    Course,
    Task,
    Answer,
    UserCourse,
    UserTask,
    UserAnswer,
    Tutorial,
    TutorialCategory,
    TaskTest,
    Post
)

from code_runner.lambda_executor import LambdaCodeExecutor

code_executor = LambdaCodeExecutor()

logger = logging.getLogger(__name__)
import os

secret_key = os.environ.get("SECRET_KEY")


def is_admin(user):
    return user.is_superuser  # Tarkistaa, onko käyttäjä ylläpitäjä



def coming_soon(request):
    #return render(request, "main_app/coming_soon.html")
    return render(request, "main_app/index.html")
    


def home(request):
    return render(request, "main_app/index.html")
    # return HttpResponse("Koodiguru avataan pian")
    
    
def purchase_premium(request):
    return render(request, "main_app/purchase_premium.html")


def register_view(request):
    if request.user.is_authenticated:
        messages.info(
            request, f"{request.user.first_name}, olet jo kirjautunut sisään."
        )
        return redirect("main_app:profile")
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            protocol = "https" if request.is_secure() else "http"
            mail_subject = "Aktivoi KoodiGuru-tilisi."

            activation_token = generate_activation_token(user)
            activation_link = (
                f"{protocol}://{current_site.domain}/activate/{activation_token}"
            )

            # Päivitä sähköpostiviesti sisältämään uusi aktivointilinkki
            message = render_to_string(
                "registration/registration_confirm_email_template.html",
                {"user": user, "activation_link": activation_link},
            )

            """
            # Generoi vahvistuslinkki
            current_site = get_current_site(request)
            mail_subject = 'Aktivoi KoodiGuru-tilisi.'
            protocol = 'https' if request.is_secure() else 'http'
            message = render_to_string('registration/registration_confirm_email_template.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'protocol': protocol,
            })"""

            # Lähetä vahvistuslinkki sähköpostitse
            send_mail(mail_subject, message, "noreply@koodiguru.com", [user.email])

            logger.info(
                "Käyttäjä %s loi tunnuksen. Aktivointi sähköposti lähetetty",
                user.username,
            )

            return render(request, "registration/registration_confirm_sent.html")

    else:
        form = NewUserForm()

    return render(
        request=request, template_name="main_app/register.html", context={"form": form}
    )


User = get_user_model()
def activate_account(request, token):
    User = get_user_model()
    
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        user_id = payload.get('user_id')
        user = User.objects.get(pk=user_id)
        if user.is_active:
            messages.success(request, "Tilisi on jo aktivoitu! Voit kirjautua sisään.")
            logger.info("Käyttäjä yritti aktivoida tilinsä uudestaan", user.username)
            return redirect("main_app:login")
        # Purkaa JWT-tokenin
       
        
        
       
            
        # Aktivoi käyttäjätunnus
        user.is_active = True
        user.save()
        messages.success(request, "Tilisi on nyt aktivoitu! Voit kirjautua sisään.")
        logger.info("Käyttäjä %s aktivoi tunnuksen", user.username)
        return redirect("main_app:login")

    except User.DoesNotExist:
        messages.error(request, "Aktivointilinkki on vanhentunut tai virheellinen! Yritä luoda tili uudestaan!")
        logger.error("Aktivointilinkki on virheellinen tai käyttäjää ei löydy.")
        return redirect("main_app:register")

    except (jwt.ExpiredSignatureError, jwt.DecodeError):
        messages.error(request, "Aktivointilinkki on vanhentunut tai virheellinen!")
        logger.error("Aktivointilinkki on vanhentunut tai virheellinen.")
        return redirect("main_app:register")

def generate_activation_token(user):
    payload = {"user_id": user.id, "exp": datetime.utcnow() + timedelta(minutes=30)}
    return jwt.encode(payload, secret_key, algorithm="HS256")


from django.contrib.auth.hashers import check_password


def login_view(request):
    if request.user.is_authenticated:
        messages.info(
            request, f"{request.user.first_name}, olet jo kirjautunut sisään."
        )
        return redirect("main_app:profile")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                name = user.first_name
                messages.success(request, f"{name}, sinut on kirjattu sisään.")
                logger.info("Käyttäjä %s kirjautui sisään", user.username)
                login(request, user)
                return redirect("main_app:profile")
            else:
                messages.error(
                    request,
                    f"Virheellinen käyttäjätunnus tai salasana, yritä uudelleen.",
                )
                logger.warning(
                    "Käyttäjän %s kirjautuminen epäonnistui", username
                )  # Käytetään suoraan username-muuttujaa
        else:
            messages.error(
                request, f"Virheellinen käyttäjätunnus tai salasana, yritä uudelleen."
            )
            # Tässä vaiheessa emme tiedä käyttäjänimeä, joten emme voi logata sitä.
            logger.warning("Kirjautuminen epäonnistui.")

    form = AuthenticationForm()
    return render(
        request=request, template_name="main_app/login.html", context={"form": form}
    )

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from .models import User  # Olettaen, että User-malli on samassa sovelluksessa

@login_required
@user_passes_test(is_admin)
def report_view(request):
    users = User.objects.all().order_by('role', '-points')  # Järjestetään ensin roolin ja sitten pisteiden mukaan

    # Kerää lisätietoja jokaisesta käyttäjästä
    for user in users:
        user.completed_tasks = UserTask.objects.filter(user=user, status='solved').count()
        user.current_level_name = user.level_name()

    return render(request, 'main_app/report.html', {'users': users})


@login_required
def profile(request):
    user = request.user
    
    # Käytetään käyttäjän `current_level` ja `progress_percentage` määritelmiä
    current_level = user.current_level
    progress_percentage = user.progress_percentage
    
    # Määritellään värit eri tasoille, voidaan mukauttaa tarpeen mukaan
    level_colors = ["bg-success", "bg-info", "bg-warning", "bg-danger", "bg-primary", "bg-secondary"]
    
    # Luodaan tieto vain nykyiselle tasolle
    level_data = {
        'level': current_level,
        'percentage': progress_percentage,
        'color': level_colors[current_level % len(level_colors)],  # Valitse väri listasta
    }
    
    return render(request, "main_app/profile.html", {
        "user": user,
        "level_data": level_data,  # Huomaa, että nyt käytämme yksikkömuotoa 'level_data'
    })

@login_required
def logout_view(request):
    name = request.user.first_name
    logout(request)
    # Lisää viesti
    messages.success(request, f"{name}, sinut on kirjattu ulos.")
    logger.info("Käyttäjä %s kirjautui ulos", name)
    return redirect("/")


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        password_form = PasswordCheckForm(request.POST)
        if form.is_valid() and password_form.is_valid():
            password = password_form.cleaned_data.get("password")
            if not check_password(password, request.user.password):
                password_form.add_error('password', 'Antamasi salasana ei ole oikea.')
            else:
                form.save()
                messages.success(request, "Profiili päivitetty onnistuneesti!")
                return redirect("main_app:profile")
        else:
            messages.error(request, "Virhe päivittäessä profiilia.")
    else:
        form = CustomUserChangeForm(instance=request.user)
        password_form = PasswordCheckForm()
    return render(
        request,
        "main_app/edit_profile.html",
        {"form": form, "password_form": password_form},
    )


class CustomPasswordChangeView(auth_views.PasswordChangeView):
    template_name = "registration/password_change_template.html"
    success_url = reverse_lazy("main_app:profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Salasanasi on vaihdettu onnistuneesti!")
        return response

    def form_invalid(self, form):
        # Don't add a generic error message here since the form will show field-specific errors
        return super().form_invalid(form)


from django.db.models import Count
from django.utils import timezone
from .models import Course, UserCourse

from django.db.models import Count

def course_list(request):
    is_tester = request.user.is_authenticated and request.user.role == 'tester'

    # Huomaa, että korjaamme tässä num_tutorials-annotaation
    courses_query = Course.objects.prefetch_related('tutorials').annotate(
        num_tasks=Count("task", distinct=True),
    ).all()

    courses_to_show = []
    for course in courses_query:
        course.num_tutorials = course.tutorials.count()  # Lisätään tutoriaalien määrä suoraan kurssiobjektiin
        show_course = not course.is_hidden or request.user.is_staff or (is_tester and course.is_test_state)
        if show_course:
            courses_to_show.append(course)

    user_courses = []
    if request.user.is_authenticated:
        user_courses = UserCourse.objects.filter(user=request.user).values_list("course", flat=True)

    context = {
        "courses": courses_to_show,
        "user_courses": user_courses,
        "is_tester": is_tester
    }
    return render(request, "main_app/course_list.html", context)




def contact(request):
    return render(request, "main_app/contact.html")

def post_list(request):
    posts = Post.objects.all().order_by('-date_posted')
    return render(request, 'main_app/post_list.html', {'posts': posts})

def post_detail(request, post_id):
    # Hae postaus tietokannasta käyttäen sen ID:tä. Jos postausta ei löydy, palauta 404-virhe.
    post = get_object_or_404(Post, pk=post_id)

    # Välitä postaus templateen ja renderöi sivu
    return render(request, 'main_app/post_detail.html', {'post': post})




from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
def course_detail(request, course_id):
   
    course = get_object_or_404(Course, id=course_id)
    if not course.is_all_free and not request.user.is_authenticated:
        return HttpResponseForbidden("Sinun täytyy olla kirjautunut sisään nähdäksesi tämän kurssin tiedot.")
    tasks = Task.objects.filter(course=course).order_by("category", "taskTitle")
    tutorials = Tutorial.objects.filter(courses=course)  # Muutettu käyttämään 'courses' suhdetta
    if request.user.is_authenticated:
        user_tasks = UserTask.objects.filter(user=request.user, task__in=tasks)
        user_task_status_dict = {ut.task_id: ut.status for ut in user_tasks}
    else:
        user_task_status_dict = {}

    context = {
        "course": course,
        "tasks": tasks,
        "user_task_status": user_task_status_dict,
        "tutorials": tutorials,
    }

    return render(request, "main_app/course_detail.html", context)




def tutorial_detail(request, tutorial_id):
    tutorial = get_object_or_404(Tutorial, id=tutorial_id)
    task_id = request.session.get("task_id")  # Haetaan task_id istunnosta
    context = {
        "tutorial": tutorial,
        "task_id": task_id,  # Lisätään task_id kontekstiin
    }
    return render(request, "main_app/tutorial_detail.html", context)

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden

from django.shortcuts import render, get_object_or_404, redirect

def perform_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    request.session["task_id"] = task.id
    answer = Answer.objects.get(task=task)

    # Tarkista, kuuluuko tehtävä täysin vapaaseen kurssiin
    if task.course.is_all_free and not request.user.is_authenticated :
        # Jos tehtävä kuuluu täysin vapaaseen kurssiin
        template = "main_app/perform_task_ano.html"  # Anonyymille käyttäjälle tarkoitettu template
    else:
        # Jos tehtävä ei kuulu täysin vapaaseen kurssiin ja käyttäjä ei ole kirjautunut sisään
        if not request.user.is_authenticated:
            return redirect('login_url')  # Ohjaa kirjautumissivulle
        template = "main_app/perform_task.html"  # Kirjautuneelle käyttäjälle tarkoitettu template

    # Aseta editor_theme oletusarvo, jos käyttäjä ei ole kirjautunut sisään
    editor_theme = "default" if not request.user.is_authenticated else request.user.editor_theme

    # Käsittele UserAnswer vain, jos käyttäjä on kirjautunut sisään
    user_answer = None
    if request.user.is_authenticated:
        user_answer = UserAnswer.objects.filter(user=request.user, task=task).first()

    status = "started"  # Default status
    if request.method == "POST":
        status = request.POST.get("status", status)  # Use POST status if exists

    # Luo tai päivitä UserTask vain, jos käyttäjä on kirjautunut sisään
    task_status = None
    if request.user.is_authenticated:
        user_task, created = UserTask.objects.get_or_create(
            user=request.user, task=task, defaults={"status": status}
        )
        if not created and request.method == "POST":
            user_task.status = status
            user_task.save()
        task_status = user_task.status

    # Poista ylimääräiset rivinvaihdot ja välilyönnit vastauksesta
    answer.answerOutput = answer.answerOutput.replace("\r\n", "\n")

    return render(
        request,
        template,
        {
            "task": task,
            "answer": answer,
            "user_answer": user_answer,
            "task_status": task_status,
            "editor_theme": editor_theme,
        },
    )

from django.db.models import Count, Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def search(request):
    query = request.GET.get("q", "")  # Haettu termi

    # Suoritetaan haku eri malleissa
    courses = Course.objects.filter(
        Q(courseTitle__icontains=query) | Q(courseDescription__icontains=query)
    )
    tasks = Task.objects.filter(
        Q(taskTitle__icontains=query) | Q(taskDescription__icontains=query)
    )
    tutorials = Tutorial.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    )

    # Annotoi kurssit tehtävien ja tutoriaalien määrällä
    courses = courses.annotate(
        num_tasks=Count("task", distinct=True),
        num_tutorials=Count("tutorials", distinct=True),  # Käytä 'tutorials' kenttää
    )

    # Hae käyttäjän suorittamat tehtävät
    if request.user.is_authenticated:
        user_tasks = UserTask.objects.filter(user=request.user)
        user_task_status = {task.task.id: task.status for task in user_tasks}
        user_courses = UserCourse.objects.filter(user=request.user).values_list(
            "course", flat=True
        )
    else:
        user_task_status = {}
        user_courses = []

    return render(
        request,
        "main_app/search_results.html",
        {
            "query": query,
            "courses": courses,
            "tasks": tasks,
            "tutorials": tutorials,
            "user_task_status": user_task_status,
            "user_courses": user_courses,
        },
    )


from func_timeout import func_timeout, FunctionTimedOut
from django.http import JsonResponse
import io
import sys
from main_app.models import TaskTest

def process_code(code, inputs=[], task=None):
    print("Saadut syötteet:", inputs)
    def input_func(prompt=None):
        if prompt:
            print(prompt, end="")
        if inputs:
            input_value = inputs.pop(0)
            print(input_value)
            return input_value
        else:
            return 0

    custom_globals = {"input": input_func, "_source_code": code, "__name__": "__main__"}

    # Hae testikoodi tietokannasta, jos mahdollista
    test_code = None
    if task:
        task_test_instance = TaskTest.objects.filter(task=task).first()
        if task_test_instance:
            test_code = task_test_instance.test_code

    def exec_code():
        new_stdout = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = new_stdout
        try:
            exec(code, custom_globals)
            if test_code:
                exec(test_code, custom_globals)
                test_result = custom_globals.get("test_function", lambda x: (True, ""))(custom_globals)
                if not test_result[0]:
                    raise Exception("TestFailed:\n" + test_result[1])
        except Exception as e:
            sys.stdout = old_stdout
            return {"error": str(e), "output": ""}
        output = new_stdout.getvalue()
        sys.stdout = old_stdout
        return {"output": output}

    try:
        # Sovelletaan aikakatkaisua kaikkiin suorituksiin
        result = func_timeout(1, exec_code)
    except FunctionTimedOut:
        return JsonResponse({"error": "Timeout error", "output": ""})
    except Exception as e:
        return JsonResponse({"error": str(e), "output": ""})

    # Palautetaan JsonResponse riippuen suorituksen tuloksesta
    if "error" in result:
        return JsonResponse({"error": result["error"], "output": ""})
    else:
        return JsonResponse({"output": result["output"]})




import requests
from django.http import JsonResponse

def process_code_rest_api(code, inputs=[], task_id=None, language="python"):
    print(f"Lähetetään koodi suoritettavaksi kielellä: {language}")
    url = "http://run-code:8000/run_code/execute/"

    # Hae testikoodi tietokannasta käyttäen task_id:tä
    test_code = None
    if task_id is not None:
        try:
            task_test_instance = TaskTest.objects.filter(task_id=task_id).first()
            if task_test_instance:
                test_code = task_test_instance.test_code
                print(f"Haettu testikoodi tehtävälle {task_id}")
        except TaskTest.DoesNotExist:
            print(f"Testikoodia ei löytynyt tehtävälle {task_id}")

    data = {
        "code": code,
        "inputs": inputs,
        "test_code": test_code,  # Lisätty testikoodi
        "language": language
    }

    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=data, headers=headers)
        print("Response on", response)
        try:
            response_data = response.json()
            if response.status_code == 200:
                return JsonResponse(response_data)
            else:
                return JsonResponse({"error": "API error", "details": response_data}, status=response.status_code)
        except ValueError:
            return JsonResponse({"error": "API did not return JSON", "details": response.text}, status=500)
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e), "output": ""}, status=500)

import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

def test_code(request):
    if request.method == "POST":
        code = request.POST.get("code", "")
        language = request.POST.get("language", "").lower()
        debug_mode = request.POST.get("debug", "false").lower() == "true"
        task_id = request.POST.get("task_id")
        
        try:
            task = Task.objects.get(id=task_id)
            task_inputs = eval(task.taskInputs)
            
            # Get test code
            test_code = None
            task_test = TaskTest.objects.filter(task=task).first()
            if task_test:
                test_code = task_test.test_code

            if language == "python":
                output = code_executor.execute_code(
                    code=code,
                    inputs=task_inputs,
                    test_code=test_code,
                    debug=debug_mode,
                    user=request.user if request.user.is_authenticated else None,
                    task=task
                )
                logger.info("Käyttäjä %s ajoi koodia tehtävässä %s", request.user.username if request.user.is_authenticated else "anonymous", task_id)
                return output
            elif language == "pseudo":
                return JsonResponse({"output": ""})
            else:
                return JsonResponse(
                    {"error": f"Unsupported language: {language}", "output": ""}
                )
        except Exception as e:
            logger.error(f"Error in test_code: {str(e)}")
            return JsonResponse({
                "error": str(e), 
                "output": "",
                "debug_info": traceback.format_exc() if debug_mode else None
            })
        
@csrf_exempt
@require_http_methods(["POST"])
def run_code_ano(request):
    try:
        data = json.loads(request.body)
        code = data.get("code", "")
        language = data.get("language", "").lower()
        user_inputs = data.get("user_inputs", [])
        task_id = data.get("task_id")

        if language != "python":
            return JsonResponse({"error": f"Unsupported language: {language}", "output": ""})

        # Get task if task_id is provided
        task = None
        if task_id:
            try:
                task = Task.objects.get(id=task_id)
            except Task.DoesNotExist:
                pass

        # Execute code using Lambda
        result = code_executor.execute_code(
            code=code,
            inputs=user_inputs,
            user=request.user if request.user.is_authenticated else None,
            task=task
        )
        
        logger.info("Anonymous code execution completed")
        return result

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON", "output": ""})
    except Exception as e:
        logger.error(f"Error executing anonymous code: {str(e)}")
        return JsonResponse({"error": str(e), "output": ""})



import io
import sys
from django.http import JsonResponse
from .models import TaskTest  # Oletan, että TaskTest-malli on määritelty .models-moduulissa



@login_required
@csrf_exempt
def update_task_status_started(request):
    try:
        if request.method == "POST":
            user = request.user
            task_id = request.POST.get("task_id")
            task_status = get_object_or_404(
                UserTask, user=request.user, task_id=task_id
            )
            task_status.status = "started"
            task_status.save()
            logger.info("Käyttäjä %s aloitti tehtävän %s", user.username, task_id)

            return JsonResponse(
                {"message": "Task status updated to started."}, status=200
            )
    except Exception as e:
        print("Error updating task status:", e)
        return JsonResponse({"error": str(e)}, status=400)

@login_required
@csrf_exempt
def update_task_status_solved(request):
    if request.method == "POST":
        user = request.user
        task_id = request.POST.get("task_id")
        task = get_object_or_404(Task, pk=task_id)
        
        # Haetaan UserTask-objekti, luodaan se tarvittaessa
        user_task, created = UserTask.objects.get_or_create(
            user=user, 
            task=task, 
            defaults={'status': 'started'}  # Oletusarvo, jos objektia ei ole olemassa
        )
        
        if user_task.status != 'solved':
            # Tehtävää ei ole aiemmin ratkaistu, päivitä käyttäjän pisteet
            user.add_points(task.points)
            # Päivitä tehtävän tila 'solved'-tilaan
            user_task.status = 'solved'
            user_task.save()
            logger.info("Käyttäjä %s ratkaisi tehtävän %s ensimmäistä kertaa. Pisteitä lisätty: %s", user.username, task_id, task.points)
            return JsonResponse({"message": "Task status updated to solved and points added."}, status=200)
        else:
            # Tehtävä on jo ratkaistu aiemmin, ei lisätä pisteitä uudelleen
            logger.info("Käyttäjä %s yritti ratkaista tehtävän %s uudestaan. Pisteitä ei lisätty.", user.username, task_id)
            return JsonResponse({"message": "Task already solved, no points added."}, status=200)


@csrf_exempt
def save_code(request):
    if request.method == "POST":
        user = request.user
        task_id = request.POST.get("task_id")
        code = request.POST.get("code")

        task = Task.objects.get(id=task_id)

        user_answer, created = UserAnswer.objects.get_or_create(user=user, task=task)
        user_answer.answer = code
        user_answer.save()
        logger.info(
            "Käyttäjä %s tallensi vastauksen tehtävään %s", user.username, task_id
        )
        return JsonResponse({"message": "Code saved successfully"})

    return JsonResponse({"error": "Invalid request"}, status=400)


def review_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    # Tarkistetaan, kuuluuko tehtävä vapaaseen kurssiin
    if not task.course.is_all_free:
        # Jos käyttäjä ei ole kirjautunut sisään ja kurssi ei ole vapaa, estetään pääsy
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Tämä sisältö vaatii kirjautumisen.")
    
    answer = Answer.objects.filter(task=task).first()
    
    # Haetaan käyttäjän vastaus, jos käyttäjä on kirjautunut sisään
    user_answer = None
    if request.user.is_authenticated:
        user_answer = UserAnswer.objects.filter(user=request.user, task=task).first()
    
      # Määritetään seuraava tehtävä
    next_task = Task.objects.filter(course=task.course, id__gt=task.id).order_by('id').first()
    
    return render(
        request,
        "main_app/review_task.html",
        {"task": task, "answer": answer, "user_answer": user_answer,
        "next_task": next_task,},
    )

from django.http import JsonResponse


@login_required
def save_editor_theme(request):
    if request.method == "POST" and request.user.is_authenticated:
        theme = request.POST.get("theme")
        if theme:
            request.user.editor_theme = theme  # Oletan, että sinulla on `profile`-malli, joka liittyy `User`-malliin ja siinä on `editor_theme`-kenttä.
            request.user.save()
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error", "message": "Teema puuttuu."})
    return JsonResponse({"status": "error", "message": "Ei sallittu."})


def add_course_to_user(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    UserCourse.objects.create(user=request.user, course=course)
    return redirect("main_app:profile")


def remove_course_from_user(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    UserCourse.objects.filter(user=request.user, course=course).delete()
    return redirect("main_app:course_list")


from django.core.mail import EmailMultiAlternatives


@csrf_exempt  # voit poistaa tämän, jos käytät CSRF-tunnistetta
@login_required
def send_email(request):
    if request.method == "POST":
        name = (
            request.user.first_name + " " + request.user.last_name
        )  # request.POST.get('nameInput', '')
        email = request.user.email  # request.POST.get('emailInput', '')
        message = request.POST.get("messageTextArea", "")
        subject = f"Yhteydenotto KoodiGurusta käyttäjältä: {name}"

        email_message = EmailMultiAlternatives(
            subject,
            message,
            "koodiguruoficial@gmail.com",  # Lähettäjän sähköpostiosoite
            ["koodiguruoficial@gmail.com"],  # Vastaanottajan sähköpostiosoite
            reply_to=[email],
        )

        email_message.attach_alternative(message, "text/html; charset=UTF-8")
        email_message.send()
        messages.info(
            request,
            f" Kiitos viestistä {request.user.first_name}, viestisi on lähetetty onnistuneesti! Vastaamme viestiisi mahdollisimman pian.",
        )
        return redirect("main_app:profile")

    else:
        return JsonResponse({"error": "Invalid request method."})


class CustomPasswordResetView(PasswordResetView):
    template_name = "registration/password_reset_template.html"
    email_template_name = (
        "registration/password_reset_email_template.html"  # lisää tämä
    )
    success_url = reverse_lazy("main_app:password_reset_done")


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "registration/password_reset_done_template.html"
    email_template_name = "registration/password_reset_email_template.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm_template.html"
    success_url = reverse_lazy("main_app:password_reset_complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "registration/password_reset_complete_template.html"

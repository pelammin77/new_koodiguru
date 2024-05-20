from django_cron import CronJobBase, Schedule
from .tasks import delete_unactivated_users

class DeleteUnactivatedUsersCronJob(CronJobBase):
    RUN_EVERY_MINS = 1  # Tehtävä ajetaan 30 minuutin välein 

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'main_app.delete_unactivated_users'  # Uniikki tunniste cron-tehtävälle

    def do(self):
        delete_unactivated_users()

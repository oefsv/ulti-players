from django.core.management import call_command


def backup():
    call_command("dbbackup")
    call_command("mediabackup")

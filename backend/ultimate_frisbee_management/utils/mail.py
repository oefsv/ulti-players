import logging
from typing import List

from django.contrib.auth.models import User
from django.core import mail
from django.db.models import QuerySet
from sesame.utils import get_query_string

from django.http import HttpResponse
from django.template import loader


from ..models import Person,PersonToClubMembership
from _datetime import date


def send_conflict_notification(request, persons: QuerySet ):
    connection = mail.get_connection()

    today = date.today()
    last_year = date(year=today.year-1, month=12, day=31)

    # Manually open the connection
    connection.open()
    messages = []
    for p in persons:
        if not p.eligibile_nationals:
            club_memberships: List[PersonToClubMembership] = p.get_current_clubmemberships()
            templates = loader.get_template("mails/nationals_conflict/send_conflict_notification_user.j2"),
            context={
                'person': p,
                'club_memberships': club_memberships,
                'last_year': last_year,
                'request':request
            }
            msg = mail.EmailMessage(
                    subject=f'Konflikt bei der Vereinsmeldung von {p.firstname} {p.lastname}',
                    body= templates[0].render(context),
                    to= [p.user.email],
                    from_email="admin@admin.admin",
                    connection=connection
                )
            msg.content_subtype="html"
            messages.append(msg)

            for m in club_memberships:
                for admin in User.objects.filter(groups__name=f'club_admin_{m.club.name}'):
                    admin_p = Person.objects.get(user=admin)
                    gender = "r" if admin_p.sex == "m" else ""
                    body = f"Liebe{gender} {admin_p.firstname},<br>"
                    body += f"{p.firstname} {p.lastname} wurde für dieses Jahr bei den folgenden Vereinen gemeldet: <br>"
                    for m in club_memberships:
                        body += f"{m.club.name}. <br>"
                
                    body += f"""Dies hat zur Folge, dass von beiden Vereinen der Verbandsbeitrag 
                    eingezogen wird. Stimmen im Verband erhält jedoch keiner.
                    Die Vereine wurden ebenfalls kontaktiert um diese Problem zu lösen.
                    Du kannst den Konflikt mit einem Klick auf den entsprechenden Link lösen. <br>
                    ACHTUNG: <br>
                    Durch klicken wird die Vereinsmitgliedschaft von {p.firstname} {p.lastname} in der Datenbank mit 31.12. 
                    des letzten Jahres als beendet eingetragen. Falls du einen kannst du im Admin portal die Daten auch manuell wieder ändern.<br>
                    """
                
                    body +=f'<a href="http://localhost:8000/{get_query_string(admin)}">Mitgliedschaft von {p.firstname} {p.lastname} bei {m.club.name} mit {last_year.strftime("%d.%m.%Y")}  beenden.</a><br>'

                    msg = mail.EmailMessage(
                            subject=f'Konflikt bei der Vereinsmeldung von {p.firstname} {p.lastname}',
                            body=body,
                            to= [admin.email],
                            connection=connection,  
                        )
                    msg.content_subtype="html"
                    messages.append(msg)


    # Send the two emails in a single call -
    connection.send_messages(messages)
    # The connection was already open so send_messages() doesn't close it.
    # We need to manually close the connection.
    connection.close()
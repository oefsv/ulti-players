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

            for m in club_memberships:
                admin_emails =  User.objects.filter(groups__name=f'club_admin_{m.club.name}').values_list("email",flat=True)
                
                club_memberships: List[PersonToClubMembership] = p.get_current_clubmemberships()
                templates = loader.get_template("mails/nationals_conflict/send_conflict_notification_club_admin.j2"),
                context={
                    'person': p,
                    'club_memberships': club_memberships,
                    'affected_club_membership': m,
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

    # Send the two emails in a single call -
    connection.send_messages(messages)
    # The connection was already open so send_messages() doesn't close it.
    # We need to manually close the connection.
    connection.close()
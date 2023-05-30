

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ultimate_frisbee_management.settings")
django.setup()

from ultimate_frisbee_management.models import Person
from datetime import datetime
from django.db import models
from django.db.models import F


def update_birthdate():
    # Get all instances of YourModel
    instances = Person.objects.all()

    # Iterate over each instance
    updated_instances = []
    for instance in instances:
        # Get the previous year's value
        year = instance.birthdate.year

        # Set the date field to January 1st of the previous year
        updated_date = datetime(year, 1, 1)

        # Update the instance using F() and assign it to a new object
        updated_instance = Person(id=instance.id, birthdate=updated_date)
        updated_instances.append(updated_instance)

    # Bulk update the date field for all instances
    Person.objects.bulk_update(updated_instances, ['birthdate'])


# Call the function to update the date field
update_birthdate()
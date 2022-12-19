import datetime
from collections import OrderedDict

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from .models import Application
from users.models import User


def change_user_debt(application: OrderedDict) -> None:
    user = User.objects.get(id=application['user'])
    user.debt += application['value']
    user.save()


def get_application_by_pk(pk):
    try:
        return Application.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404


def approve_application(application: Application) -> None:
    application.approved = True
    set_answer_date(application)
    application.save()


def set_answer_date(application: Application) -> None:
    application.answer_date = datetime.datetime.now()
    application.save()

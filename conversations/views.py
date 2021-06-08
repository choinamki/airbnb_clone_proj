from django.db.models import Q
from users import models as user_models
from . import models


def go_conversation(request, a_pk, b_pk):
    user_one = user_models.User.objects.get_or_none(pk=a_pk)
    user_two = user_models.User.objects.get_or_none(pk=b_pk)
    if user_one is not None and user_two is not None:
        conversations = models.Conversations.objects.get(Q(participatns=user_one) & Q(participants=user_two))

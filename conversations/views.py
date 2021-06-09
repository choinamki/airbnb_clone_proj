from django.shortcuts import redirect, reverse
from django.db.models import Q
from django.views.generic import DetailView
from users import models as user_models
from . import models


def go_conversation(request, a_pk, b_pk):
    print(a_pk)
    print(b_pk)
    user_one = user_models.User.objects.get_or_none(pk=a_pk)
    print(user_one)
    user_two = user_models.User.objects.get_or_none(pk=b_pk)
    print(user_two)
    if user_one is not None and user_two is not None:
        try:
            conversations = models.Conversations.objects.get(Q(participants=user_one) & Q(participants=user_two))
        except models.Conversations.DoesNotExist:
            conversations = models.Conversations.objects.create()
            conversations.participants.add(user_one, user_two)
        return redirect(reverse('conversations:detail', kwargs={'pk': conversations.pk}))


class ConversationDetailView(DetailView):
    model = models.Conversations
    template_name = 'conversations/conversation_detail.html'

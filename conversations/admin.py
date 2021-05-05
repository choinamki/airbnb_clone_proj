from django.contrib import admin
from . import models


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    """ Message Admin Definition """

    list_display = ('__str__', 'created',)


@admin.register(models.Conversations)
class ConversationsAdmin(admin.ModelAdmin):
    """ Conversation Admin Definition """

    list_display = ('__str__', 'count_messages', 'count_participants',)

from django.contrib import admin
from . import models


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    """ Message Admin Definition """
    pass


@admin.register(models.Conversations)
class ConversationsAdmin(admin.ModelAdmin):
    """ Conversation Admin Definition """
    pass

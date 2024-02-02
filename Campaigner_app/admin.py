from django.contrib import admin

# Register your models here.
from .models import Subscriber, Campaign, CampaignSubscriber

admin.site.register(Subscriber)
admin.site.register(Campaign)
admin.site.register(CampaignSubscriber)

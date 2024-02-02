from django.urls import path
from . import views

urlpatterns = [
    path('subscribers/', views.add_subscriber, name='subscriber-list'),
    path('unsubscribe/<str:email>/', views.unsubscribe, name='unsubscribe'),
    path('add_campaign/', views.add_campaign, name='add_campaign'),
    path('send_daily_campaign/', views.send_campaign_emails, name='send_daily_campaign'),
    
    # Add more URLs for campaigns and other views as needed
]
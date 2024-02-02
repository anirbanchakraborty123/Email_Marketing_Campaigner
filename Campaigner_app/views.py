from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .models import Subscriber, Campaign, CampaignSubscriber
from .serializers import SubscriberSerializer, CampaignSerializer
from .tasks import send_campaign_emails

@api_view(['POST'])
def add_subscriber(request):
    serializer = SubscriberSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def unsubscribe(request, email):
    subscriber = get_object_or_404(Subscriber, email=email)
    subscriber.user_is_active = False
    subscriber.save()
    return Response({'status': 'unsubscribed'})

@api_view(['POST'])
def add_campaign(request):
    serializer = CampaignSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def send_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    if campaign:
        send_campaign_emails.delay(campaign.id)
        campaign.is_sent = True
        campaign.save()
    return Response({'status': 'scheduled for sending'})



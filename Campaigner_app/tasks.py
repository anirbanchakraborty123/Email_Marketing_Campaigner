from celery import shared_task
from django.core.mail import send_mail
from .models import Subscriber,Campaign, CampaignSubscriber
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from Email_Campaigner.settings import EMAIL_HOST_USER
from multiprocessing import Pool

def send_campaign_email(campaign, recipient_list):
    subject = campaign.subject
    message = campaign.plain_text_content

    # Load the base email template
    base_template = get_template('base_campaign_template.html')

    # Render the campaign email content
    context = {
        'subject': campaign.subject,
        'preview_text': campaign.preview_text,
        'article_url': campaign.article_url,
        'html_content': campaign.html_content,
        'plain_text_content': campaign.plain_text_content,
    }
    email_content = base_template.render(context)

    # Create and send the email to all recipients
    msg = EmailMultiAlternatives(subject, message, EMAIL_HOST_USER, recipient_list)
    msg.attach_alternative(email_content, "text/html")
    msg.send()


@shared_task
def send_campaign_emails(campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    subscriber_list = Subscriber.objects.filter(is_active=True)

    if subscriber_list:
        recipient_list = [subscriber.email for subscriber in subscriber_list]

        # Send the same campaign to all subscribers in parallel
        with Pool(processes=4) as pool:
            pool.starmap(send_campaign_email, [(campaign, recipient_list)])


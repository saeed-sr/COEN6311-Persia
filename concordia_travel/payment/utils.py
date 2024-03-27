from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_booking_confirmation_email(user, booking):
    subject = 'Your Concordia Travel Booking Confirmation'
    html_message = render_to_string('payment/booking_confirmation_email.html', {'user': user, 'booking': booking})
    plain_message = strip_tags(html_message)
    from_email = 'concordiatravel@concordiatravel.me'
    to = user.email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
from rest_framework import permissions
from rest_framework.views import APIView
from django.core.mail import send_mail
from .models import Contact
from rest_framework.response import Response


class ContactCreateView(APIView):
    permission_classes = (permissions.AllowAny)

    def post(self, request, format=None):
        data = self.request.data

        try:
            send_mail(
                data['subject'],
                'Name: ' + data['name']
                + '\nEmail: ' + data['email']
                + '\n\nMessage: ' + data['message'],
                'xiaosha9728@outlook.com',
                ['xiaosha9728@outlook.com'],
                fail_silently=False
            )

            contact = Contact(name=data['name'], email=data['email'], subject=data['subject'], message=data['message'])
            contact.save()

            return Response({'success': 'Message sent successfully'})
        except Exception as e:
            print(e)
            return Response({'error': 'Message failed to send'})

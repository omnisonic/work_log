from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# for sending emails ref: https://www.jbssolutions.com/resources/blog/sending-automated-emails-django-signals/
from django.core.mail import send_mail # for sending emails
from django.db.models.signals import post_save # for sending emails
from django.dispatch import receiver # for sending emails


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    hours_worked = models.DecimalField(default=0.0,max_digits=2, decimal_places=1)
    screen_shot = models.ImageField(default='default.jpg',upload_to='screen_shots/')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})



@receiver(post_save, sender=Post) # for sending emails
def new_post_notification_email(sender, instance, created, **kwargs):
    if created:

        name = instance.author
        content = instance.content
        date = instance.date_posted
        hours = instance.hours_worked
        subject = f'New log Entry created by {instance.author} '# Todo: add author name.
        message = 'A new post has been created!\n' # Todo: add link to post, and author, and date, and hours worked, content.
        message += "Author: " + str(name) + "\n"
        message += "Date: " + str(date) + "\n"
        message += "Hours Worked: " + str(hours) + "\n"
        message += "Content: " + str(content) + "\n"

        send_mail(
            subject,
            message,
            'jctech@jctech.xyz',
            ['jctech@jctech.xyz'],
            fail_silently=False,
        )



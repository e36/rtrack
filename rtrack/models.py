from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.


class Username(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    isspamaccount = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Report(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class UserReportLink(models.Model):
    name = models.ForeignKey(Username)
    timestamp = models.DateTimeField(auto_now_add=True)
    report = models.ForeignKey(Report)

    def __str__(self):
        return str(self.name) + " " + str(self.report)


class UserReportLinkFormModel(models.Model):
    # this model is just to bridge the gap between the view (which has just a charfield) and the model which needs
    # a foreign key
    name = models.CharField(max_length=100)


class UrlReportLink(models.Model):
    url = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    report = models.ForeignKey(Report)

    def __str__(self):
        return self.url


class NoteReportLink(models.Model):
    note = models.TextField()
    author = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    report = models.ForeignKey(Report)

    def __str__(self):
        return self.note


class NoteReportLinkFormModel(models.Model):
    note = models.TextField()


class UsernameNote(models.Model):
    username = models.ForeignKey(Username)
    author = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField()


class UsernameNoteFormModel(models.Model):
    note = models.TextField()


class UsernameModmailLink(models.Model):
    username = models.ForeignKey(Username)
    timestamp = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=200)


class UsernameSearch(models.Model):
    username = models.CharField(max_length=200) # doesn't need to be a foreignkey() because we aren't linking it


class ModmailLink(models.Model):
    user = models.ForeignKey(Username)
    # timestamp is when the record was added to the database
    timestamp = models.DateTimeField(auto_now_add=True)
    modmail_id = models.CharField(max_length=50)
    subject = models.CharField(max_length=250)
    # created_utc is when the message was submitted in reddit - This is being pulled for now
    # created_utc = models.CharField(max_length=25)

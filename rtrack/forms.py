from django import forms
from rtrack.models import *


class ReportForm(forms.ModelForm):
    title = forms.CharField(max_length=100, help_text="Title:")
    description = forms.CharField(widget=forms.Textarea, help_text="Description:")

    class Meta:
        model = Report
        fields = ['title', 'description']


class UserReportLinkForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    # report = forms.CharField()

    class Meta:
        model = UserReportLinkFormModel
        fields = ['name']
        # exclude = ['report']


class UrlReportLinkForm(forms.ModelForm):
    url = forms.URLField

    class Meta:
        model = UrlReportLink
        fields = ['url']


class NoteReportLinkForm(forms.ModelForm):
    note = forms.Textarea

    class Meta:
        model = NoteReportLinkFormModel
        fields = ['note']


class UsernameNoteForm(forms.ModelForm):
    note = forms.Textarea

    class Meta:
        model = UsernameNoteFormModel
        fields = ['note']


class UsernameSearchForm(forms.ModelForm):
    username = forms.CharField

    class Meta:
        model = UsernameSearch
        fields = ['username']


class ModmailLinkForm(forms.ModelForm):
    modmail_id = forms.CharField(max_length=50, help_text='Modmail ID: ')
    subject = forms.CharField(max_length=250, help_text='Subject: ')
    # created_utc = forms.CharField(max_length=25, help_text='Created UTC: ')

    class Meta:
        model = ModmailLink
        fields = ['subject', 'modmail_id']


class LoginFormModelForm(forms.ModelForm):
    user = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    redirect_next = forms.CharField(max_length=100)

    class Meta:
        model = LoginFormModel
        fields = ['user', 'password']


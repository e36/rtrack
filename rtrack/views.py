from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rtrack.forms import *
from rtrack.models import *
from rtrack.other import *
# Create your views here.

# TODO Implement timezones somehow, may require user accounts

@login_required
def index(request):
    report_list = Report.objects.order_by('-last_updated')
    userreferencedata = builduserlist()
    context = {'report_list': report_list,
               'refdata': userreferencedata,
               }
    return render(request, 'rtrack/index.html', context)


@login_required
def reportview(request, report_id):
    report_data = Report.objects.get(id=report_id)
    userlinkdata = UserReportLink.objects.filter(report=report_id)
    urllinkdata = UrlReportLink.objects.filter(report=report_id)
    notelinkdata = NoteReportLink.objects.filter(report=report_id)

    context = {'report_data': report_data,
               'userlinkdata': userlinkdata,
               'urllinkdata': urllinkdata,
               'notelinkdata': notelinkdata,
               }

    return render(request, 'rtrack/reportview.html', context)


@login_required
def createreport(request):

    if request.method == "POST":
        # An HTTP POST?
        form = ReportForm(request.POST)

        # Check that we've been provided a valid form
        if form.is_valid():
            # save the new report in the database
            # I'm ditching the form.save() so I can directly create the report object- it'll be easier to redirect
            # to the form view this way
            # form.save(commit=True)
            title = form.cleaned_data['title']
            desc = form.cleaned_data['description']

            new_report = Report.objects.create(title=title, description=desc)

            # go to the new report view
            url = reverse('report', kwargs={'report_id': new_report.id})
            return HttpResponseRedirect(url)

            # now call the index view
            # return index(request)
        else:
            # the form contained errors - just print to the terminal for now
            print(form.errors)

    else:
        # if the request was not a POST, display the form to enter details
        form = ReportForm()

    # bad form or form details, no form supplied, etc
    # Render the form with any error messages
    return render(request, 'rtrack/createreport.html', {'form': form})


@login_required
def create_association(request, report_id):
    if request.method == "POST":
        form = UserReportLinkForm(request.POST)

        if form.is_valid():

            # grab cleaned name data
            user_name = form.cleaned_data['name']

            # get name and report objects
            # create the username object if it doesn't already exist
            user_obj, c = Username.objects.get_or_create(name=user_name)
            report_obj = Report.objects.get(pk=report_id)

            # create the object - I'm using get_or_create so it only creates a DB entry if it doesn't already exist
            UserReportLink.objects.get_or_create(name=user_obj, report=report_obj)

            # return back to the report view
            url = reverse('report', kwargs={'report_id': report_id})
            return HttpResponseRedirect(url)
        else:
            print(form.errors)
    else:
        form = UserReportLinkForm()

    return render(request, 'rtrack/createassociation.html', {'form': form, 'report_id': report_id})


@login_required
def create_url_link(request, report_id):
    if request.method == "POST":
        form = UrlReportLinkForm(request.POST)

        if form.is_valid():

            # grab cleaned url datas
            url = form.cleaned_data['url']

            # get report object
            report_obj = Report.objects.get(pk=report_id)

            # get_or_create the url link db entry
            UrlReportLink.objects.get_or_create(url=url, report=report_obj)

            # return back to the report view
            url = reverse('report', kwargs={'report_id': report_id})
            return HttpResponseRedirect(url)
        else:
            print(form.errors)
    else:
        form = UrlReportLinkForm()

    return render(request, 'rtrack/create_url_link.html', {'form': form, 'report_id': report_id})


@login_required
def create_note_link(request, report_id):
    if request.method == "POST":
        form = NoteReportLinkForm(request.POST)

        if form.is_valid():

            # grab cleaned note datas
            note = form.cleaned_data['note']

            # get report object
            report_obj = Report.objects.get(pk=report_id)

            # get_or_create the url link db entry
            NoteReportLink.objects.get_or_create(note=note, report=report_obj)

            # return back to the report view
            url = reverse('report', kwargs={'report_id': report_id})
            return HttpResponseRedirect(url)
        else:
            print(form.errors)
    else:
        form = NoteReportLinkForm()

    return render(request, 'rtrack/create_note_link.html', {'form': form, 'report_id': report_id})


@login_required
def user_page(request, user_name):
    # get username object
    userdata = Username.objects.get(name=user_name)

    # get associated links
    linkdata = UserReportLink.objects.filter(name=userdata)

    # get user note data
    usernote = UsernameNote.objects.filter(username=userdata).order_by('-timestamp')

    # get modmail links
    modmail = ModmailLink.objects.filter(user=userdata)

    # get report data for each link
    # init empty list for holding report tuples
    reportdata = []
    for ilink in linkdata:
        rp = Report.objects.get(title=ilink.report)
        reportdata.append(rp)

    # data to be sent to the view
    context = {'userdata': userdata,
               'linkdata': linkdata,
               'reportdata': reportdata,
               'usernotes': usernote,
               'modmail': modmail,
               }

    return render(request, 'rtrack/users.html', context)


@login_required
def user_add_note(request, user_name):
    if request.method == "POST":
        form = UsernameNoteForm(request.POST)

        if form.is_valid():

            # grab cleaned note data
            note = form.cleaned_data['note']

            # get user data
            user_data = Username.objects.get(name=user_name)

            # create the note
            UsernameNote.objects.create(username=user_data, note=note)

            # return to the user_page view
            url = reverse('user_page', kwargs={'user_name': user_name})
            return HttpResponseRedirect(url)
        else:
            print(form.errors)
    else:
        form = UsernameNoteForm()

    return render(request, 'rtrack/create_usernote.html', {'form': form, 'user_name': user_name})


@login_required
def user_search(request):
    if request.method == "POST":
        form = UsernameSearchForm(request.POST)

        if form.is_valid():

            # get form data
            searchname = form.cleaned_data['username']

            # "search" the Usernames model. __startswith is what I'm using until I can find a better method
            foundnames = Username.objects.filter(name__startswith=searchname)

            #build context
            context = {'username': searchname,
                       'queryresult': foundnames,
                       }

            return render(request, 'rtrack/search.html', context)
        else:
            print(form.errors)
    else:
        form = UsernameSearchForm()

    return render(request, 'rtrack/search.html', {'form': form})


@login_required
def add_user(request):
    if request.method == "POST":

        # we are going to reuse the UsernameSearchForm, because all we need
        # is a charfield and not another identical model
        form = UsernameSearchForm(request.POST)

        if form.is_valid():

            #   grab cleaned user name
            username = form.cleaned_data['username']

            # create the object if it doesn't already exist
            Username.objects.get_or_create(name=username)

            # redirect to the user view
            url = reverse('user_page', kwargs={'user_name': username})
            return HttpResponseRedirect(url)
        else:
            print(form.errors)
    else:
        form = UsernameSearchForm()

        return render(request, 'rtrack/create_user.html', {'form': form})


@login_required
def create_modmail_link(request, user_name):
    if request.method == "POST":

        form = ModmailLinkForm(request.POST)

        if form.is_valid():

            # get username object
            user_obj = Username.objects.get(name=user_name)

            # get cleaned data ['subject', 'modmail_id', 'created_utc']
            subject = form.cleaned_data['subject']
            modmail_id = form.cleaned_data['modmail_id']
            #created_utc = form.cleaned_data['created_utc']

            # create the link
            ModmailLink.objects.get_or_create(user=user_obj, subject=subject, modmail_id=modmail_id)

            # redirect to the user view
            url = reverse('user_page', kwargs={'user_name': user_name})
            return HttpResponseRedirect(url)
        else:
            print(form.errors)
    else:
        form = ModmailLinkForm()

        return render(request, 'rtrack/create_modmail_link.html', {'form': form, 'user_name': user_name})


def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Gather the username and password provided by the user.
        # This information is obtained from the login form.


        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your rtrack account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}").format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'registration/login.html', {})


@login_required
def user_logout(request):
    # since we know the user is logged in, we can just log them out
    logout(request)

    # now take the user back to the homepage
    return HttpResponseRedirect(reverse('login'))
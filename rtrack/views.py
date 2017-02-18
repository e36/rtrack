from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt

from rtrack.other import *

from datetime import datetime

from rtrack.slack import handle_slack_request
# Create your views here.


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
    urllinkdatafiltered = UrlReportLink.objects.filter(report=report_id).order_by('-timestamp')[:5]
    userlinkdatafiltered = UserReportLink.objects.filter(report=report_id).order_by('-timestamp')[:5]

    context = {'report_data': report_data,
               'userlinkdata': userlinkdata,
               'urllinkdata': urllinkdata,
               'notelinkdata': notelinkdata,
               'urllinkdatafiltered': urllinkdatafiltered,
               'userlinkdatafiltered': userlinkdatafiltered,
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

    # get report name
    report_obj = Report.objects.get(id=report_id)

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

    return render(request, 'rtrack/createassociation.html', {'form': form, 'report_id': report_id, 'report_title': report_obj.title})


@login_required
def create_association_ajax(request, report_id):

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

            # update the report last_updated field
            report_obj.last_updated = datetime.utcnow()
            report_obj.save()

            # return back to the report view
            url = reverse('report', kwargs={'report_id': report_id})
            return HttpResponseRedirect(url)
        else:
            print(form.errors)
    else:
        form = UserReportLinkForm()

    url = reverse('report', kwargs={'report_id': report_id})
    return HttpResponseRedirect(url)


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
def create_url_link_ajax(request, report_id):
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

            # update the report last_updated field
            report_obj.last_updated = datetime.utcnow()
            report_obj.save()

            return HttpResponseRedirect(url)
        else:
            print(form.errors)
    else:
        form = UrlReportLinkForm()

    url = reverse('report', kwargs={'report_id': report_id})
    return HttpResponseRedirect(url)


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
def create_note_link_ajax(request, report_id):
    if request.method == "POST":
        form = NoteReportLinkForm(request.POST)

        if form.is_valid():

            # grab cleaned note datas
            note = form.cleaned_data['note']

            # get self data
            self_data = User.objects.get(username=request.user.username)

            # get report object
            report_obj = Report.objects.get(pk=report_id)

            # get_or_create the url link db entry
            NoteReportLink.objects.get_or_create(note=note, author=self_data, report=report_obj)

            # update the report last_updated field
            report_obj.last_updated = datetime.utcnow()
            report_obj.save()

            # return back to the report view
            url = reverse('report', kwargs={'report_id': report_id})
            return HttpResponseRedirect(url)
        else:
            print(form.errors)
    else:
        form = NoteReportLinkForm()

    url = reverse('report', kwargs={'report_id': report_id})
    return HttpResponseRedirect(url)


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

            # get self data
            self_data = User.objects.get(username=request.user.username)

            # create the note
            UsernameNote.objects.create(username=user_data, author=self_data, note=note)

            # return to the user_page view
            url = reverse('user_page', kwargs={'user_name': user_name})
            return HttpResponseRedirect(url)
        else:
            print(form.errors)
    else:
        form = UsernameNoteForm()

    return render(request, 'rtrack/create_usernote.html', {'form': form, 'user_name': user_name})


@login_required
def user_add_note_ajax(request, user_name):
    if request.method == "POST":
        form = UsernameNoteForm(request.POST)

        if form.is_valid():

            # grab cleaned note data
            note = form.cleaned_data['note']

            # get user data
            user_data = Username.objects.get(name=user_name)

            # get self data
            self_data = User.objects.get(username=request.user.username)

            # create the note
            UsernameNote.objects.create(username=user_data, author=self_data, note=note)

            # return to the user_page view
            url = reverse('user_page', kwargs={'user_name': user_name})
            return HttpResponseRedirect(url)
        else:
            print(form.errors)
    else:
        form = UsernameNoteForm()

    url = reverse('user_page', kwargs={'user_name': user_name})
    return HttpResponseRedirect(url)


@login_required
def search(request):
    if request.method == "POST":

        # get query string
        searchname = request.POST.get('search_text')

        # set queryresult to false
        queryresult = False

        # "search" the Usernames and Reports model. __contains is what I'm using until I can find a better method
        # we're searching both titles and descriptions in report
        foundnames = Username.objects.filter(name__icontains=searchname)
        foundreports = Report.objects.filter(title__icontains=searchname)
        founddesc = Report.objects.filter(description__icontains=searchname)

        # combine the two into a set so we eliminate any duplicates
        report_result = list(set(foundreports) | set(founddesc))

        # figure out if any results exists, and set queryresult to true if they do
        if report_result or foundnames:
            queryresult = True

        # build context
        context = {'query_text': searchname,
                   'user_result': foundnames,
                   'report_result': report_result,
                   'queryresult': queryresult,
                   }

        return render(request, 'rtrack/search.html', context)
    else:
        return render(request, 'rtrack/search.html', {})


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
            # created_utc = form.cleaned_data['created_utc']

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


@login_required
def create_modmail_link_ajax(request, user_name):
    if request.method == "POST":

        form = ModmailLinkForm(request.POST)

        if form.is_valid():

            # get username object
            user_obj = Username.objects.get(name=user_name)

            # get cleaned data ['subject', 'modmail_id', 'created_utc']
            subject = form.cleaned_data['subject']
            modmail_id = form.cleaned_data['modmail_id']
            # created_utc = form.cleaned_data['created_utc']

            # create the link
            ModmailLink.objects.get_or_create(user=user_obj, subject=subject, modmail_id=modmail_id)

            # redirect to the user view
            url = reverse('user_page', kwargs={'user_name': user_name})
            return HttpResponseRedirect(url)
        else:
            print(form.errors)
    else:
        form = ModmailLinkForm()

    url = reverse('user_page', kwargs={'user_name': user_name})
    return HttpResponseRedirect(url)


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
            errors = "Invalid login details"
            return render(request, "registration/login.html", {'errors': errors})

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


@login_required
def password_changed(request):
    # just a few to show that the password change was made successfully.
    return render(request, 'registration/password_change_complete.html', {})


@login_required
def remove_user_link(request, report_id, user_name):
    # removes a username from being associated with a report

    # get user objects
    user_obj = Username.objects.get(name=user_name)
    report_obj = Report.objects.get(id=report_id)

    # get the report link and delete it, because fuck it
    user_link = UserReportLink.objects.get(name=user_obj, report=report_obj)

    # only delete it if it exists, otherwise return to the report view
    if user_link:
        user_link.delete()
    else:
        # return back to the report view
        url = reverse('report', kwargs={'report_id': report_id})
        return HttpResponseRedirect(url)

    # return back to the report view
    url = reverse('report', kwargs={'report_id': report_id})
    return HttpResponseRedirect(url)


@login_required
def about(request):
    """
    Displays the about page.  Includes information about the system and a changelog
    :param request:
    :return: Nothing!
    """

    return render(request, 'rtrack/about.html')


@login_required
def readonly(request, report_id):
    """
    Gets report data and sends it to the readonly.html view.  This is basically just read-only data for sending
    To the admins
    :param request:
    :param report_id:
    :return:
    """
    report_data = Report.objects.get(id=report_id)
    userlinkdata = UserReportLink.objects.filter(report=report_id)
    urllinkdata = UrlReportLink.objects.filter(report=report_id)
    notelinkdata = NoteReportLink.objects.filter(report=report_id)

    # append "u/" to each username
    userlist = []
    for u in userlinkdata:
        username = "u/" + str(u.name)
        userlist.append(username)

    context = {'report_data': report_data,
               'userlist': userlist,
               'urllinkdata': urllinkdata,
               'notelinkdata': notelinkdata,
               }

    return render(request, 'rtrack/readonly.html', context)


@csrf_exempt
def slack_request(request):
    """
    Handles the incoming requests from slack
    :param request:
    :return:
    """

    slackdata = {
        'user_id': request.POST.get('user_id'),
        'user_name': request.POST.get('user_name'),
        'command': request.POST.get('command'),
        'text': request.POST.get('text'),
        'response_url': request.POST.get('response_url')
    }

    incoming_token = request.POST.get('token', '')

    if request.method == 'POST':

        # check to make sure that the token coming from the slack request matches the one in the settings
        if settings.SLACK_TOKEN == incoming_token:

            retdata = handle_slack_request(slackdata)

            return JsonResponse(retdata, content_type='application/json')
        else:
            return HttpResponse(status=403)

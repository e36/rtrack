"""
    This file handles the slack integration stuff.  Parsing the commands, getting and sending the data, etc.

    The view slack_request will send the command info as a dict:

    token=3o9f7whdildsgfo7isdgf
    team_id=T0001
    team_domain=example
    channel_id=C2147483705
    channel_name=test
    user_id=U2147483697
    user_name=Steve
    command=/weather
    text=94070
    response_url=https://hooks.slack.com/commands/1234/5678

    handle_slack_request is the main def, and where slack_request must send the data to.  It will handle all of the
    various parts of processing and returning data.
"""

from rtrack.models import Report

def handle_slack_request(slackdata):
    """
    Handles the processing of the slack request
    :param slackdata: the dict with the data from the slack request
    :return: nothing
    """

    # build the response dictionary
    response = {
        'response_type': 'in_channel',
        'text': '',
    }

    # 1 process the slack command
    if slackdata['command'] == '/rtrack':

        # split the text into separate elements
        text_elements = slackdata['text'].split(' ')

        # loop through each element and look for commands
        for element in text_elements:

            # list reports
            if element == 'list':

                response['text'] = list_reports()
                return response

    # 2 get any data

    # 3 format the layout

    # 4 return any data


def process_slack_command(command_text):
    """
    Parses the slack command.
    :param command_text: A string that doesn't include the /rtrack command: "report 5" would show report ID=5
    :return:
    """

def list_reports():
    """
    Returns a list of reports
    :return:
    """

    reports = Report.objects.order_by('pk').all()

    return_string = ""

    for report in reports:

        t = str(report.pk) + '\t' + str(report.title) + '\n'

        return_string += t

    return return_string


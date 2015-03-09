from rtrack.forms import *


def builduserlist():
    """
      this will take the username and count how many times they are referenced.
    :return: a list of dictionaries that will contain the name and reference count
            dict['name', 'count']
    """

    # init the list
    return_list = []

    # get a list of usernames
    user_list = Username.objects.all()

    # for each user, look up and count the number of links
    for user in user_list:
        # find all links that reference the username
        links = UserReportLink.objects.filter(name=user)

        # build the dictionary
        ldict = {'name': user.name,
                 'count': links.count()}

        # add to the return list
        return_list.append(ldict)

    # return the list
    return return_list


def get_user_notes(username):
    """

    :param username: the username to search for
    :return: a list of dicts [{'timestamp', 'note_text'}]
    """

    # get user data
    userdata = Username.objects.get(name=username)

    # init return list
    return_list = []


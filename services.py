import requests
import re


def is_user_exist(user_name, bot):
    return bot.get_user_id_from_username(user_name)


def get_author_from_media_link(link):
    """Instead nonworking: bot.get_media_info(media_id)."""
    response = requests.post(url=link)
    if response.ok:
        return find_inst_user(response.text)
    else:
        return None

    
def find_inst_user(_string):
    """Search and verify Instagram users.

    The regex expression was used from the article -
    https://blog.jstassen.com/2016/03/code-regex-for-instagram-username-and-hashtags/"""

    _regex = r'(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)'
    find_inst_user_list = re.findall(_regex, _string)
    if not find_inst_user_list:
        return None
    else:
        return find_inst_user_list[0]


def find_intersection_3_lists(list1, list2, list3):
    """Returns intersection of 3 lists."""
    _intersection_list = [x for x in set(list1) if x in set(list2)]
    intersection_list = [x for x in set(list3) if x in set(_intersection_list)]
    return intersection_list
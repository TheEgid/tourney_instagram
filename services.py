import requests
import re


def get_author_from_media_link(link):
    """Instead nonworking: bot.get_media_info(media_id)."""
    response = requests.get(url=link)
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


def find_intersection_3_sets(set1, set2, set3):
    """Returns intersection of 3 lists."""
    _intersection_set = set1.intersection(set2)
    intersection_set = _intersection_set.intersection(set3)
    return list(intersection_set)
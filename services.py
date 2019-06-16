import requests
import re


def get_author_from_media_link(link):
    """Instead nonworking: bot.get_media_info(media_id)."""
    response = requests.get(url=link)
    if response.ok:
        return find_inst_user(response.text)
    return None

    
def find_inst_user(_string):
    """Search and verify Instagram users.

    The regex expression was used from the article -
    https://blog.jstassen.com/2016/03/code-regex-for-instagram-username-and-hashtags/"""

    _regex = r'(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)'
    find_inst_user_list = re.findall(_regex, _string)
    if find_inst_user_list:
        return find_inst_user_list[0]
    return None
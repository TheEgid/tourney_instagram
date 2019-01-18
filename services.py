import logging
import requests
from instabot import Bot
import re
import os
import sys
from dotenv import load_dotenv
import pprint


def is_user_exist(user_name, bot):
    inst_id = bot.get_user_id_from_username(user_name)
    if inst_id is None:
        return None
    else:
        return inst_id

    
def get_author_from_media_link(link):
    """Instead nonworking: bot.get_media_info(media_id)."""
    response = requests.post(link=link)
    if response.ok:
        return find_inst_user(response.text)
    else:
        return None

    
def find_inst_user(_string):
    """Search and verify Instagram users."""
    _regex = r'(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)'
    find_inst_user_list = re.findall(_regex, _string)
    if not find_inst_user_list:
        return None
    else:
        return find_inst_user_list[0]


def find_intersection_3_lists (list1, list2, list3):
    _intersection_list = [x for x in list(set(list1)) if x in list(set(list2))]
    intersection_list = [x for x in list(set(list3)) if x in list(set(_intersection_list))]
    return intersection_list

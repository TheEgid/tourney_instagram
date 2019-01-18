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


def find_inst_user(_string):
    """Search and verify Instagram users."""
    _regex = r'(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)'
    find_inst_user_list = re.findall(_regex, _string)
    if not find_inst_user_list:
        return None
    else:
        return find_inst_user_list[0]


def get_all_inst_comments(post_url, bot):
    inst_comments = bot.get_media_id_from_link(post_url)
    all_inst_comments = []
    for comment in bot.get_media_comments_all(inst_comments):
        all_inst_comments.append(
            [comment['user_id'], comment['user']['username'], comment['text']])
    return all_inst_comments


def filter_comments(comments_list):
    _user_id, _username, _text = zip(*comments_list)
    _text = map(lambda x: find_inst_user(x), _text)
    users_comments_finded = list(zip(_user_id, _username, _text))
    users_comments_filtered = [[x[0], x[1], x[2]] for x in users_comments_finded if x[2] is not None]
    return users_comments_filtered


def check_friends(friends_list, bot):
    _user_id, _username, _text = zip(*friends_list)
    _text = map(lambda x: is_user_exist(x, bot=bot), _text)
    cheked_list = list(zip(_user_id, _username, _text))
    _frends_list = []
    for _user_id, _username, _text in cheked_list:
        if _text is not None:
            _frends_list.append((_user_id, _username))
    return list(set(_frends_list))


def get_all_likers(link, bot):
    """Get Instagram Users, who liked."""
    media_id = bot.get_media_id_from_link(link)
    return bot.get_media_likers(media_id)


def get_author_from_media_link(link):
    """Instead nonworking: bot.get_media_info(media_id)."""
    response = requests.post(link)
    if response.ok:
        return find_inst_user(response.text)
    else:
        return None


def get_all_followers(link, bot):
    """Get Instagram Followers."""
    _user = get_author_from_media_link(link=link)
    print(_user)
    return bot.get_user_followers(_user)

def find_intersection_3_lists (list1, list2, list3):
    _intersection_list = [x for x in list(set(list1)) if x in list(set(list2))]
    intersection_list = [x for x in list(set(list3)) if x in list(set(_intersection_list))]
    return intersection_list

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    LOGIN_INST = os.getenv("LOGIN_INST")
    PASSWORD_INST = str(os.getenv("PASSWORD_INST"))
    bot = Bot()
    bot.login(username=LOGIN_INST, password=PASSWORD_INST)
    post = 'https://www.instagram.com/p/BrbkCltHo2K/'
    # all_inst_comments_list = get_all_inst_comments(post_url=post, bot=bot)
    # filtered = filter_comments(all_inst_comments_list)
    # checked_friends_list = check_friends(friends_list=filtered, bot=bot)

    friends_list = [(16029089, 'vyvyonthatbeat'), (230824758, 'msgchan'),
              (3946295604, 'foodiema'), (929756969, 'jollechan'),
              (7052630766, 'proudalmaraz'), (15629820, 'xemiiboo'),
    (6066, 'createwithmi'), (55, 'aidairiarte')]

    users_id_noted_friend, _username = zip(*friends_list)
    users_id_followed = [7052630766, 55, 15629820, 6066, 7549645, 9099991]

    filtered_users_id = [x for x in list(set(users_id_noted_friend)) if x in list(set(users_id_followed))]
    print(filtered_users_id)



import os
import sys
import pickle
import pprint
from instabot import Bot
from dotenv import load_dotenv
import argparse

from services import get_author_from_media_link
from services import find_inst_user
from services import find_intersection_3_sets


def get_all_inst_comments(post_url, bot):
    inst_comments = bot.get_media_id_from_link(post_url)
    all_inst_comments = []
    for comment in bot.get_media_comments_all(inst_comments):
        all_inst_comments.append(
            [comment['user_id'], comment['user']['username'], comment['text']])
    return all_inst_comments


def filter_comments(comments_list):
    users_comments_filtered = []
    for comment_user_id, comment_username, comment_text in comments_list:
        _comment_text = find_inst_user(comment_text)
        if _comment_text is not None:
            users_comments_filtered.append((comment_user_id,
                                            comment_username,
                                            _comment_text))
    return users_comments_filtered


def check_all_taged_friends(friends_list, bot):
    frends_set = set()
    for comment_user_id, comment_username, comment_text in friends_list:
        text = bot.get_user_id_from_username(comment_text)
        if text is not None:
            frends_set.add(comment_user_id)
    return list(frends_set)


def get_taged_friends(link, bot):
    """Get Instagram Users, who taged_friends."""
    all_inst_comments_list = get_all_inst_comments(post_url=link, bot=bot)
    filtered_list = filter_comments(all_inst_comments_list)
    _taged_friends_list = check_all_taged_friends(friends_list=filtered_list,
                                                   bot=bot)
    taged_friends_list = [str(x) for x in _taged_friends_list]
    return set(taged_friends_list)


def get_all_likers(link, bot):
    """Get Instagram Users, who liked."""
    media_id = bot.get_media_id_from_link(link=link)
    return set(bot.get_media_likers(media_id))


def get_all_followers_picle_io(link, bot, io_file):
    """Get Instagram Followers and input/output Picle file."""
    _user = get_author_from_media_link(link=link)
    if not os.path.exists(io_file):
        all_followers = bot.get_user_followers(_user)
        with open(io_file, 'wb') as f:
            pickle.dump(all_followers, f)
        return set(all_followers)
    else:
        with open(io_file, 'rb') as f:
            all_followers = pickle.load(f)
        return set(all_followers)


def get_tourney_instagram_result_list(link, bot, id_list):
    """Tournament organizer exclusion."""
    organizer = get_author_from_media_link(link)
    organizer_id = bot.get_user_id_from_username(organizer)
    if organizer_id in id_list:
        id_list.remove(organizer_id)
    return id_list


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.insert(0, os.path.split(dir_path)[0])
    load_dotenv()
    LOGIN_INST = os.getenv("LOGIN_INST")
    PASSWORD_INST = os.getenv("PASSWORD_INST")
    bot = Bot()
    bot.login(username=LOGIN_INST, password=PASSWORD_INST)
    acceleration_file_name = 'data.pickle'

    parser = argparse.ArgumentParser()
    parser.add_argument("post", help="instagram post arg")
    parser.add_argument("test", nargs='?', help="test mode arg", )
    args = parser.parse_args()
    post = args.post

    if args.test == 'test':
        print('Test_mode')
    else:
        os.remove(acceleration_file_name)

    users_id_noted_friend_set = get_taged_friends(link=post, bot=bot)

    users_id_likers_set = get_all_likers(link=post, bot=bot)

    users_id_followers_set = get_all_followers_picle_io(link=post,
                                                         bot=bot,
                                                         io_file=
                                                         acceleration_file_name)

    result = find_intersection_3_sets(users_id_noted_friend_set,
                                       users_id_likers_set,
                                       users_id_followers_set)

    result_of_tourney = get_tourney_instagram_result_list(link=post, bot=bot,
                                                          id_list=result)
    pprint.pprint(result_of_tourney)

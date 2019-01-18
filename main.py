import os
import sys
import pickle
import pprint
from instabot import Bot
from dotenv import load_dotenv

from services import is_user_exist
from services import get_author_from_media_link
from services import find_inst_user
from services import find_intersection_3_lists 


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
    users_comments_filtered = [[x[0], x[1], x[2]] for x
                               in users_comments_finded if x[2] is not None]
    return users_comments_filtered


def check_all_taged_friends(friends_list, bot):
    _user_id, _username, _text = zip(*friends_list)
    _text = map(lambda x: is_user_exist(x, bot=bot), _text)
    checked_list = list(zip(_user_id, _username, _text))
    _frends_list = []
    for _user_id, _username, _text in checked_list:
        if _text is not None:
            _frends_list.append((_user_id, _username))
    return list(set(_frends_list))


def get_taged_friends(link, bot):
    """Get Instagram Users, who taged_friends."""
    all_inst_comments_list = get_all_inst_comments(post_url=link,
                                                   bot=bot)
    filtered_list = filter_comments(all_inst_comments_list)
    taged_friends_list = check_all_taged_friends(friends_list=filtered_list,
                                                   bot=bot)
    users_id_noted_friend, _username = zip(*taged_friends_list)
    users_id_noted_friend = [str(x) for x in users_id_noted_friend]
    return users_id_noted_friend


def get_all_likers(link, bot):
    """Get Instagram Users, who liked."""
    media_id = bot.get_media_id_from_link(link=link)
    return bot.get_media_likers(media_id)


def get_all_followers_picle_io(link, bot, io_file):
    """Get Instagram Followers and input/output Picle file."""
    _user = get_author_from_media_link(link=link)
    if not os.path.exists(io_file):
        all_followers = bot.get_user_followers(_user)
        with open(io_file, 'wb') as f:
            pickle.dump(all_followers, f)
        return all_followers
    else:
        with open(io_file, 'rb') as f:
            all_followers = pickle.load(f)
        return all_followers


def get_tourney_instagram_result_list(link, bot, id_list):
    """Tournament organizer exclusion."""
    organizer = get_author_from_media_link(link)
    organizer_id = is_user_exist(organizer, bot)
    try:
        id_list.remove(organizer_id)
        return id_list
    except ValueError:
        return id_list


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.insert(0, os.path.split(dir_path)[0])
    load_dotenv()
    LOGIN_INST = os.getenv("LOGIN_INST")
    PASSWORD_INST = str(os.getenv("PASSWORD_INST"))
    bot = Bot()
    bot.login(username=LOGIN_INST, password=PASSWORD_INST)
    acceleration_file_name = 'data.pickle'

    post = sys.argv[1]
    if len(sys.argv) == 2:
        os.remove(acceleration_file_name)
    else:
        if sys.argv[2] == 'test':
            print('Test_mode')
        else:
            os.remove(acceleration_file_name)

    users_id_noted_friend_list = get_taged_friends(link=post,bot=bot)

    users_id_likers_list = get_all_likers(link=post, bot=bot)

    users_id_followers_list = get_all_followers_picle_io(link=post,
                                                         bot=bot,
                                                         io_file=
                                                         acceleration_file_name)

    result = find_intersection_3_lists(users_id_noted_friend_list,
                                       users_id_likers_list,
                                       users_id_followers_list)

    result_of_tourney = get_tourney_instagram_result_list(link=post, bot=bot,
                                                          id_list=result)
    pprint.pprint(result_of_tourney)


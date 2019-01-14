import logging
from instabot import Bot
import requests


def inst_data(login, password, instagram_post_list, timeout_value=10):
    """Get instagram comments.
    Args:
        login(str): instagram login
        password(str): instagram password
		instagram_post(str): instagram link
        timeout_value(int): randomized timeout of posting
    """
    #instagram_post

    bot = Bot()
    bot.login(username=login, password=password)

    for instagram_post in instagram_post_list:
    #    caption = pic[:-4].split(' ')
    #    caption = ' '.join(caption[1:])
        timeout = random.randint(1, int(timeout_value * 0.5)) * timeout_value
    #    logging.info('timeout= ' + str(timeout))
    #    time.sleep(timeout)
        bot.upload_photo(pic, caption=caption) #!!!
        if bot.api.last_response.status_code is None:
            logging.info('response error! check the cookies! ' + str(
                bot.api.last_response))
        else:
            if bot.api.last_response.status_code != 200:
				raise ValueError('response error!')

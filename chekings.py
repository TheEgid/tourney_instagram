def is_user_liked():
    pass

def is_user_followed():
    pass

def is_user_exist(user_name):
    return 'finded'

	
def find_inst_user(_string):
    """Search and verify Instagram users."""
    _regex = r'(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)'
    find_inst_user_list = re.findall(_regex, _string)
    if not find_inst_user_list:
        return None
    else:
        find_inst_user_list = list(map(lambda x: is_user_exist(x), find_inst_user_list))
        return find_inst_user_list

def download_commentators:
    pass
    return {inst_id: str_comment}		
		
def check_frends_link(commentators):
	"""Search and verify Instagram users."""
    checked_commentators = {}
    for inst_id, str_comment in commentators.items():
        checked_str_comment = find_inst_user(str_comment)
        checked_commentators.update({inst_id: checked_str_comment})
    return checked_commentators



def get_inst_id():
    pass


def check_followers(commentators):
	"""Cheking Instagram Followers."""
    followers_list = []
    for inst_id, str_comment in commentators.items():
        if is_user_followed(inst_id):
            followers_list.append((inst_id, get_inst_id(inst_id)))
    return followers_list
	
def check_likers(commentators):
	"""Cheking Instagram Users, who liked."""
    likers_list = []
    for inst_id, str_comment in commentators.items():
        if is_user_liked(inst_id):
            likers_list.append((inst_id, get_inst_id(inst_id)))
    return likers_list

import datetime
import logging
import peewee
from pyinstamation.models import User, Follower, future_rand_date
from pyinstamation import CONFIG
from pyinstamation.bot import InstaBot


logger = logging.getLogger(__name__)


class Controller:

    def __init__(self, username):
        user, is_new = User.get_or_create(username=username)
        self.user = user
        self.is_new = is_new

    def set_users_followed(self, users):
        """
        :type users: list(namedtuple)
        """
        assert type(users) is list, 'users is not a list'
        for user in users:
            unfollow_date = future_rand_date(date=user.follow_date)
            try:
                Follower.create(user=self.user, username=user.username, unfollow_date=unfollow_date)
            except peewee.IntegrityError:
                logger.exception('%s is already present in following list', user.username)

    def get_users_to_unfollow(self):
        _users_to_unfollow = self.user.follower_set.select().where(
            Follower.following == True, Follower.unfollow_date < datetime.datetime.now())
        return _users_to_unfollow
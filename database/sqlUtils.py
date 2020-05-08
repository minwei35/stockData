from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils import configUtils

user = configUtils.get_config_value("db", "user")
password = configUtils.get_config_value("db", "password")
url = configUtils.get_config_value("db", "url")


def get_sqlalchemy_session():
    engine = create_engine('oracle://{user}:{password}@{url}'.format(user=user, password=password, url=url), echo=False)
    session = sessionmaker(engine)
    my_session = session()
    return my_session


def get_sqlalchemy_session_have_echo():
    engine = create_engine('oracle://{user}:{password}@{url}'.format(user=user, password=password, url=url), echo=True)
    session = sessionmaker(engine)
    my_session = session()
    return my_session


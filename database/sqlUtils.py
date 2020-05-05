import configparser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

cfg = configparser.ConfigParser()
cfg.read("../config/config.ini")
user = cfg.get("db", "user")
password = cfg.get("db", "password")
url = cfg.get("db", "url")


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


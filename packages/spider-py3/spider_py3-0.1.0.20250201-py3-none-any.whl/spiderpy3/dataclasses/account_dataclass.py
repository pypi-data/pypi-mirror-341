from dataclasses import dataclass


@dataclass
class AccountDataclass(object):
    owner: str
    platform: str
    username: str
    password: str

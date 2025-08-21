from aiogram import Router
from . import commands
from . import vote_sta


def get_routers() -> list[Router]:
    return [
        commands.router,
        vote_sta.router,
    ]
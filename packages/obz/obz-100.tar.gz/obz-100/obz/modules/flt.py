# This file is placed in the Public Domain.


"fleet"


from obr.fleet  import Fleet
from obr.thread import name


from . import fmt


def flt(event):
    bots = Fleet.bots.values()
    try:
        event.reply(fmt(list(Fleet.bots.values())[int(event.args[0])]))
    except (KeyError, IndexError, ValueError):
        event.reply(",".join([name(x).split(".")[-1] for x in bots]))

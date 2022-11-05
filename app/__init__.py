import os
import uuid
import json
import time
import asyncio
from concurrent.futures import ProcessPoolExecutor, Future
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from classes import Game, Player, Task, Location
from location import tglive_location, airtag_location

# load configuration files
config: dict = json.loads(open("config.json").read())
rule_set: dict = json.loads(open(f"data/{config['rules']}_rules.json").read())
tasks: list[Task] = [Task(**d) for d in json.loads(open(f"data/{config['city']}_tasks.json").read())]


# start game context
tb: AsyncTeleBot = AsyncTeleBot(os.environ["TELEGRAM_TOKEN"])
game_token: str = uuid.uuid4().hex[:6]
game_session: Game = Game(game_token, "signup", None, [], [])
print(f"Game token: {game_token}")


def broadcast_location():
    """
    Broadcasts AirTag location periodically to players.

    :return: None.
    """
    while True:
        if game_session.state == "in_progress":
            loc: Location = airtag_location(config["airtag_name"])
            players: list[Player] = game_session.players()
            for player in players:
                tb.send_location(player.chat_id, loc.latitude, loc.longitude)
        time.sleep(rule_set["update_freq"])

@tb.message_handler(commands=[game_token])
def register(message: Message) -> None:
    """
    Signs up a user with the appropriate token.

    :param message: message from user.
    :return: None.
    """
    player: Player = Player(message.from_user, message.chat.id, None, [])
    game_session.chasers.append(player)
    tb.reply_to(message, "You have successfully registered.")
    return


@tb.message_handler(commands=["leaderboard"])
def leaderboard(message: Message) -> None:
    """
    Displays player leaderboard.

    :param message: message from user.
    :return: None.
    """
    tb.reply_to(message, "**Player scores**\n".join([p.display() for p in game_session.players()]))
    return


@tb.message_handler(commands=["tasks"])
def show_tasks(message: Message) -> None:
    """
    Shows tasks that user has left to complete.

    :param message: message from user.
    :return: None.
    """
    player = game_session.get_player(message.from_user)
    valid_tasks = [t for t in tasks if t not in player.completed_tasks]
    tb.reply_to(message, "**Tasks**\n".join([t.display() for t in valid_tasks]))
    return

@tb.message_handler(commands=["START"])
def start_game(message: Message):
    """
    Admin command to start game.

    :param message: message from user.
    :return: None.
    """
    if message.chat.id != config["admin_user"]:
        tb.reply_to(message, "Access denied.")
        return
    game_session.state = "in_progress"
    tb.reply_to(message, "Game started.")
    print("**Players:**\n".join([p.display() for p in game_session.players()]))
    return


@tb.message_handler(commands=["SWITCH"])
def switch_runner(message: Message):
    """
    Switches runners and jails old runner.

    :param message: message from admin.
    :return: None.
    """
    if message.chat.id != config["admin_user"]:
        tb.reply_to(message, "Access denied.")
        return
    new_runner_id: str = message.text.split()[1]
    new_runner: Player = [p for p in game_session.chasers if p.user_data.id == new_runner_id][0]
    old_runner: Player = game_session.runner
    tb.send_message(new_runner.chat_id, "Your swap has been approved. You are the new runner, good luck!")
    tb.send_message(old_runner.chat_id, f"You have been caught. You must remain where you are for {rule_set['jail_time']/60} minutes.")
    game_session.runner = new_runner
    game_session.jailed.append(old_runner)
    game_session.chasers = [p for p in game_session.chasers if p != old_runner]
    return


@tb.message_handler(commands=["STOP"])
def end_game(message: Message) -> None:
    """
    Ends game and broadcasts results.

    :param message: message from admin.
    :return: None.
    """
    if message.chat.id != config["admin_user"]:
        tb.reply_to(message, "Access denied.")
        return
    game_session.state = "finished"
    players: list[Player] = game_session.players()
    winner: Player = max(players, key=lambda x: sum([t.score for t in x.completed_tasks]))
    for player in players:
        tb.send_message(player.chat_id, f"{winner.display} has won.")
    return


@tb.message_handler(content_types=["photo"])
def forward_media(message: Message) -> None:
    """
    Forwards media to admin.

    :param message: message from user.
    :return: None.
    """
    tb.send_photo(config["admin_user"], message.photo)
    tb.reply_to(message, "Your photo has been forwarded to the admin. Please standby for further instructions.")
    return


@tb.message_handler(func=lambda x: True)
def default_answer(message: Message) -> None:
    """
    Reply to unrecognized messages.

    :param message: message from user.
    :return: None.
    """
    tb.reply_to(message, "This is not a valid command.")
    return


# start game loop
with ProcessPoolExecutor(max_workers=1) as executor:
    tb_process: Future = executor.submit(asyncio.run(tb.polling()))
    broadcast_process: Future = executor.submit(broadcast_location())

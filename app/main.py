import os
import uuid
from concurrent.futures import ProcessPoolExecutor, Future
import telebot
from telebot.types import Message


tb = telebot.TeleBot(os.environ["TELEGRAM_TOKEN"])

if __name__ == "__main__":
    airtag_name: str = input("Airtag Name: ")
    game_token: str = uuid.uuid4().hex[:6]
    print(f"Game token: {game_token}")
    with ProcessPoolExecutor(max_workers=1) as executor:
        _bg: Future = executor.submit(tb.infinity_polling())
        while True:
            raise NotImplementedError


@tb.message_handler(commands=["leaderboard"])
def register(message: Message) -> None:
    raise NotImplementedError


@tb.message_handler(commands=["tasks"])
def show_tasks(message: Message) -> None:
    raise NotImplementedError


def admin_command(command: str) -> None:
    parsed_command = command.split()
    match parsed_command[0]:
        case "START":
            raise NotImplementedError
        case "SWITCH":
            raise NotImplementedError
        case "STOP":
            raise NotImplementedError

from telebot.types import Message, Location, User
from dataclasses import dataclass


@dataclass
class Player:
    user_data: User
    chat_id: str
    runner: bool
    last_location: Location
    last_seen: float
    jailed: bool
    valid: bool
    points: int


@dataclass
class Task:
    type: str
    description: Message
    location: Location | None

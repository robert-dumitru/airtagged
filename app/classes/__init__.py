from telebot.types import Message, User
from dataclasses import dataclass


@dataclass
class Location:
    latitude: float
    longitude: float
    radius: float | None
    time: float | None


@dataclass
class Task:
    id: str
    type: str
    score: int
    description: Message
    location: Location | None

    def display(self) -> str:
        return f"{self.type} | {self.description} | {self.score}"


@dataclass
class Player:
    user_data: User
    chat_id: int
    last_location: Location | None
    completed_tasks: list[Task]

    def display(self) -> str:
        score: int = sum(t.score for t in self.completed_tasks)
        return f"{self.user_data.full_name}: {score}"


@dataclass
class Game:
    id: str
    state: str
    runner: Player | None
    chasers: list[Player]
    jailed: list[Player]

    def players(self):
        return [self.runner] + self.chasers + self.jailed

    def get_player(self, user_data: User):
        return [p for p in self.players() if p.user_data == user_data][0]


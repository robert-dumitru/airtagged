# AirTagged

Welcome to AirTagged, a game to make exploring cities more exciting! This project was partially inspired by videos such 
as [this one](https://www.youtube.com/watch?v=GmC05wOc5Dw&t=4s). 

## Installation

To run the server, you will need a computer running macOS 12.0 (Monterey) or later, with an Apple AirTag connected to 
FindMy. You will also need a python 3.10 interpreter installed and the [poetry](https://python-poetry.org/) package
management system.

1. Set up a bot with the [botfather](https://telegram.me/BotFather) and set the environment variable ``TELEGRAM_TOKEN`` 
   to the token given to you.
2. Clone this repository and install dependencies:
   ```bash
   git clone https://github.com/robert-dumitru/airtagged
   cd airtagged
   poetry install
3. Edit ``app/config.json`` with your Airtag name, admin name, and rulesets.
4. Finally, use the following command to start the bot:
   ```bash
   poetry run app

## Usage

All interactions with the game are done through the telegram bot - the admin chat has a special status to allow admin
commands to be executed. When the bot is first started, a random code will be generated - this code can be used to sign 
up.

Once all players are ready, the admin can issue the ``\START`` command. The game progresses according to the rules, with 
requests for player switches being forwarded to the admin chat. If approved, the ``\SWITCH`` command can switch the 
runner in the game. Task progress is also handled similarly.

If at any point the game needs to be finished, the admin can issue the ``\STOP`` command. Have fun!

## Contributions

Improvements are welcome and encouraged - please open an issue first if you intend on making major changes.


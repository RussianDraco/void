# Void CLI-Game Manager

Welcome to Void, a game manager made for managing Python CLI-based/in terminal games. With Void, you can manage, install, update and publish CLI-based games.

## Installation
( Temporarily on testpypi )
`pip install -i https://test.pypi.org/simple/ void==0.1.0`

## Usage

To install a game:
`void install {game}`

To uninstall a game:
`void uninstall {game}`

To see what games exist:
`void games`

Further commands at:
`void` OR `void --help`

## How to add a CLI-based game

1. Create a fork of this repository.
2. In GAMES.json, add your game's information as such:
```
    "GAME_NAME": {
        "name": "GAME_NAME",
        "description": "GAME_DESCRIPTION",
        "version": "GAME_VERSION",
        "author": "YOUR_NAME_OR_USERNAME",
        "source": "LINK_TO_GAME'S_GITHUB"
    }
```
3. Commit your changes and create a PR to this repository.

**NOTE:** your game's repository HAS to have a **requirements.txt** with all neccesary python libraries/versions AND a **main.py** that runs the game

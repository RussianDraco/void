# Void Python Game Manager

Welcome to Void, a game manager made for managing and publishing Python terminal games. With Void, you can manage, install, update and publish Python games.

## Installation
( Temporarily on testpypi )
`pip install -i https://test.pypi.org/simple/ void==0.1.1`

## Usage

To install a game:
`void install {game}`

To uninstall a game:
`void uninstall {game}`

To see what games exist:
`void games`

Further commands at:
`void` OR `void --help`


Note: Not every games will work in all instances; some games may require a GUI that isn't available on some operating systems (i.e. some Linux distros)

## How to add a Python game

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
PS: Your game can have additional external files included in the github repo that will be added/used in installation
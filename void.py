import click
import requests
import json
import os
import subprocess
from pathlib import Path

def check_pip_runner():
    try:
        subprocess.run(["pip", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "pip"
    except Exception as e:
        try:
            subprocess.run(["pip3", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return "pip3"
        except Exception as e2:
            click.echo("Pip not found!")
            click.echo("Please install Pip for void to work")
            exit(1)
def check_python_runner():
    try:
        subprocess.run(["python", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "python"
    except Exception as e:
        try:
            subprocess.run(["python3", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return "python3"
        except Exception as e2:
            click.echo("Python not found!")
            click.echo("Please install Python 3.7 or higher for void to work")
            exit(1)
#Local env: ~/.void/ {installed.json, games/}
def local_env():
    local_env_ = str(Path.home()) + "/.void/"
    if not os.path.exists(local_env_):
        os.mkdir(local_env_)
    if not os.path.exists(local_env_ + "installed.json"):
        with open(local_env_ + "installed.json", "w") as f:
            json.dump({}, f)
        f.close()
    if not os.path.exists(local_env_ + "games/"):
        os.mkdir(local_env_ + "games/")
    if not os.path.exists(local_env_ + "config.json"):
        with open(local_env_ + "config.json", "w") as f:
            json.dump({"PYTHON_RUNNER": check_python_runner(), "PIP_RUNNER": check_pip_runner()}, f)
        f.close()
    return local_env_
def get_games():
    url = "https://raw.githubusercontent.com/RussianDraco/void/main/GAMES.json"
    response = str(requests.get(url).text)
    games = json.loads(response)
    return games
def get_installed():
    local_env_ = local_env()
    with open(local_env_ + "installed.json", "r") as f:
        installed = json.load(f)
    f.close()
    return installed
def get_config():
    local_env_ = local_env()
    with open(local_env_ + "config.json", "r") as f:
        config = json.load(f)
    f.close()

    #CHECK ALL SYSTEM VARIABLES
    if not config["PYTHON_RUNNER"]:
        config["PYTHON_RUNNER"] = check_python_runner()
    if not config["PIP_RUNNER"]:
        config["PIP_RUNNER"] = check_pip_runner()

    return config

#Game github repo structure: {game_name}/ main.py, requirements.txt, resources(optional)
def install_game(name, description, version, author, github_url):
    local_env_ = local_env()
    games_dir = local_env_ + "games/"
    game_dir = games_dir + name + "/"
    requirements_file = game_dir + "/requirements.txt"
    installed_file = local_env_ + "installed.json"

    subprocess.run(["git", "clone", github_url, game_dir])
    if os.path.exists(game_dir + ".git/"):
        subprocess.run(["rm", "-rf", game_dir + ".git/"])

    if os.path.exists(requirements_file):
        subprocess.run([get_config()['PIP_RUNNER'], "install", "-r", requirements_file])

    installed = get_installed()

    installed[name] = {"name": name, "description": description, "version": version, "author": author, "source": github_url}
    with open(installed_file, "w") as f:
        json.dump(installed, f)
    f.close()
def uninstall_game(name):
    local_env_ = local_env()
    games_dir = local_env_ + "games/"
    game_dir = games_dir + name + "/"
    subprocess.run(["rm", "-r", game_dir])
def update_game(name, description, version, author, github_url):
    uninstall_game(name)
    install_game(name, description, version, author, github_url)

@click.group()
def cli():
    pass

@cli.command(help="Classic test lol.")
def ping():
    click.echo("pong")


@cli.command(help="This command plays a game.")
@click.argument("game", nargs=-1)
def install(game):
    game = " ".join(game)
    games = get_games()
    installed = get_installed()

    if game in installed:
        click.echo(f"Game {game} is already installed")
        return

    try:
        g = games[game]
    except KeyError:
        click.echo(f"Game {game} not found")
        return

    install_game(g["name"], g["description"], g["version"], g["author"], g["source"])
    click.echo(f"Installed {g['name']} {g['version']}")
    return

@cli.command(help="This command uninstalls a game.")
@click.argument("game", nargs=-1)
def uninstall(game):
    game = " ".join(game)
    local_env_ = local_env()
    installed_file = local_env_ + "installed.json"
    installed = get_installed()
    
    try:
        g = installed[game]
    except KeyError:
        click.echo(f"Game {game} not found")
        return
    
    uninstall_game(game)
    del installed[game]
    with open(installed_file, "w") as f:
        json.dump(installed, f)
    f.close()
    click.echo(f"Uninstalled {g['name']} {g['version']}")

@cli.command(help="This command lists the installed games.")
def list():
    click.echo("Installed games:")
    installed = get_installed()

    for gkey, game in installed.items():
        click.echo(f"{game['name']} {str(game['version'])} - {game['description']}")
    click.echo("-" * 20)
    click.echo("Run 'void info <game>' to get more information about a game")
    click.echo("Run 'void play <game>' to play a game")
    click.echo("Run 'void updates' & 'void update <game>' to update installed games")

@cli.command(help="This command gives information about an installed game.")
@click.argument("game", nargs=-1)
def info(game):
    game = " ".join(game)
    installed = get_installed()

    try:
        g = installed[game]
    except KeyError:
        click.echo(f"Game {game} not found")
        return

    click.echo('')
    click.echo(f"Name: {g['name']}")
    click.echo(f"Description: {g['description']}")
    click.echo(f"Version: {g['version']}")
    click.echo(f"Author: {g['author']}")
    click.echo(f"Source: {g['source']}")
    click.echo('')
    return

@cli.command(help="This command plays a game.")
@click.argument("game", nargs=-1)
def play(game):
    game = " ".join(game)
    local_env_ = local_env()
    games_dir = local_env_ + "games/"
    game_dir = games_dir + game + "/"
    if not os.path.exists(game_dir):
        click.echo(f"Game {game} not found")
        return
    click.echo(f"Running {game}...")
    click.echo('')

    os.chdir(game_dir)
    config = get_config()
    subprocess.run([config['PYTHON_RUNNER'], game_dir + "main.py"])

@cli.command(help="This command lists the updates for installed games.")
def updates():
    click.echo("Updates:")
    games = get_games()
    installed = get_installed()

    empty = True
    for gkey, game in installed.items():
        if (g := games[game["name"]]) and (g["version"] != game["version"]):
            click.echo(f"{game['name']} ({game['version']} -> {g['version']})")
            empty = False

    if empty:
        click.echo("No updates available")

    click.echo("-" * 20)
    click.echo("Run 'void update <game>' to update a game")

@cli.command(help="This command updates an installed game.")
@click.argument("game", nargs=-1)
def update(game):
    game = " ".join(game)
    games = get_games()
    installed = get_installed()

    try:
        g = installed[game]
    except KeyError:
        click.echo(f"Game {game} not found")
        return
    
    if (g_ := games[g["name"]]):
        if g_["version"] != g["version"]:
            update_game(g["name"], g_["description"], g_["version"], g_["author"], g_["source"])
            click.echo(f"Updated {g['name']} {g['version']} -> {g_['version']}")
        else:
            click.echo(f"No updates available for {g['name']}")
    else:
        click.echo(f"Game {game} not found")

@cli.command(help="This command lists the available games.")
def games():
    click.echo("Available games:")
    games = get_games()

    first = True
    for gkey, game in games.items():
        if not first:
            click.echo('')
        click.echo(f"{game['name']} by {game['author']} - {game['description']}")
        first = False

    click.echo("-" * 20)
    click.echo("Run 'void install <game>' to install a game")
import aiohttp
import json
import typing
import discord
import utils

async def get_player_data(base_url: str, players_endpoint: str) -> typing.Tuple[list, int, typing.Optional[str]]:
    # The base URL for requesting player data
    # Usually for FiveM: e.g. http://server_ip:30120/players.json

    # We'll fetch the player list
    player_data_url = f"{base_url}/{players_endpoint}"
    players = []
    status_ok = False
    error_reason = None

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(player_data_url, timeout=5) as resp:
                if resp.status == 200:
                    players = json.loads(await resp.text(encoding="utf-8"))
                    status_ok = True
                else:
                    error_reason = f"HTTP {resp.status}"
    except Exception as e:
        error_reason = str(e)

    return players, status_ok, error_reason

async def get_server_info(base_url: str, info_endpoint: str) -> typing.Tuple[str, int, typing.Optional[str]]:
    info = {}
    status_ok = False
    error_reason = None

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{base_url}/{info_endpoint}", timeout=5) as resp:
                if resp.status == 200:
                    info = json.loads(await resp.text(encoding="utf-8"))
                    status_ok = True
                else:
                    error_reason = f"HTTP {resp.status}"
    except Exception as e:
        error_reason = str(e)

    return info, status_ok, error_reason

def fivem_replace_variables(text: str, fivem_data: list, member: discord.Member = None, guild: discord.Guild = None) -> str | None:
    """
    [server_name, server_ip, players, max_players]
    """
    if text is None:
        return None

    text = text.replace("{{fivem_server_name}}", fivem_data[0])
    text = text.replace("{{server_ip}}", fivem_data[1])
    text = text.replace("{{players_length}}", str(len(fivem_data[2])))
    text = text.replace("{{max_players}}", str(fivem_data[3]))

    return utils.replace_variables(text, member, guild)

from rcon.source import rcon
import discord


def init(tree: discord.app_commands.CommandTree, bot: discord.Client, config: dict, lang: dict):
    """
    sets up the on_message callback for '/rcon'.
    """

    @tree.command(name="rcon", description=lang["command_description"])
    async def player_list_command(interaction: discord.Interaction, command: str):
        fivem_config = config
        rcon_password = fivem_config.get("rcon_password", "")
        rcon_ip = fivem_config.get("server_ip", "127.0.0.1")
        try:
            rcon_ip, rcon_port = rcon_ip.split(":")
        except ValueError:
            rcon_port = 30120
        rcon_port = int(rcon_port)
        commands_args = command.split(" ")
        new_args = []
        temp_index = -1
        for i in range(len(commands_args)):
            if commands_args[i].startswith('"'):
                temp_index = i
                temp_str = commands_args[i]
                break
            if commands_args[i].endswith('"') and temp_index != -1:
                new_args.append(" ".join(commands_args[temp_index:i+1]))
                temp_index = -1
            if temp_index == -1:
                new_args.append(commands_args[i])
        if temp_index != -1:
            return await interaction.response.send_message(lang["double_quotes_err"], ephemeral=True)
        response = "```\n" + await rcon(new_args[0], *new_args[1:], host=rcon_ip, port=rcon_port, passwd=rcon_password)
        if len(response) > 2000:
            response = response[:1990] + "\n..." + "\n```"
        await interaction.response.send_message(response, ephemeral=True)

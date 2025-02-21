import socket
import struct
import discord

class RCONClient:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.socket = None

    def connect(self):
        # UDP (weirdly enough, FiveM RCON uses UDP)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(3)  #NOTE: more than 3 seconds might resolve in "interaction failed" on the slash command

    def send_command(self, command):
        """
        Sends a command to the FiveM server.
        Fivem packets are in the format: \xFF\xFF\xFF\xFFrcon <password> <command>
        :param command:
        :return:
        """
        try:
            packet = f"\xFF\xFF\xFF\xFFrcon {self.password} {command}".encode("latin1")
            self.socket.sendto(packet, (self.host, self.port))
            try: #try to receive the response
                response, _ = self.socket.recvfrom(4096)
                response = response.decode("latin1", errors="ignore").strip()

                if response.startswith("\xFF\xFF\xFF\xFF"): # Remove unexpected leading bytes (just in case)
                    response = response[4:]
                return response
            except socket.timeout:
                return "Timeout (No response from server)"
        except Exception as e:
            return f"Error: {e}"

    def close(self):
        """Closes the UDP socket."""
        if self.socket:
            self.socket.close()
            self.socket = None

def init(tree: discord.app_commands.CommandTree, bot: discord.Client, config: dict, lang: dict):
    """
    sets up the on_message callback for '/rcon'.
    """

    @tree.command(name="rcon", description=lang["command_description"])
    async def player_list_command(interaction: discord.Interaction, command: str):

        allowed_role = int(config.get("allowed_role_id", 0))
        if allowed_role:
            allowed_role = interaction.guild.get_role(allowed_role)
            if allowed_role not in interaction.user.roles:
                return await interaction.response.send_message(lang["no_permission"], ephemeral=True)
        else:
            return await interaction.response.send_message(lang["no_permission"], ephemeral=True)
        rcon_password = config.get("rcon_password", "")
        rcon_ip = config.get("server_ip", "127.0.0.1")
        try:
            rcon_ip, rcon_port = rcon_ip.split(":")
        except ValueError:
            rcon_port = 30120
        rcon_port = int(rcon_port)
        rcon = RCONClient(rcon_ip, rcon_port, rcon_password)
        try:
            rcon.connect()
            response = rcon.send_command(command)
        except Exception as e:
            response = "Error: " + str(e)
        if len(response) > 2000:
            response = response[:1990] + "\n..." + "\n```"
        await interaction.response.send_message(response, ephemeral=True)

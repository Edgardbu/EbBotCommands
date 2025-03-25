import discord
import utils
import sqlite3

def init(tree: discord.app_commands.CommandTree, bot: discord.Client, lang: dict, db: sqlite3.Connection):
    def has_permission():
        async def predicate(interaction: discord.Interaction):
            if interaction.user.guild_permissions.administrator:
                return True
            await interaction.response.send_message(lang["no perms"], ephemeral=True)
            return False
        return discord.app_commands.check(predicate)

    auto_commands = discord.app_commands.Group(name="embed_auto", description=lang["auto_commands_description"])

    @auto_commands.command(name="add", description=lang["auto_commands_description_add"])
    @has_permission()
    async def auto_add(interaction: discord.Interaction, embed_title: str, embed_description_before_message: str = None, embed_description_after_message: str = None, channel: discord.TextChannel = None):
        """
        Add an auto embed to the channel
        :param interaction: discord.Interaction the interaction
        :param channel: discord.TextChannel the channel to add the auto embed to
        :param text: str the text of the auto embed
        :return: None
        """
        if channel is None:
            channel = interaction.channel
        db.execute("INSERT OR REPLACE INTO autoEmbeds VALUES (?, ?, ?, ?)", (channel.id, embed_title, embed_description_before_message, embed_description_after_message))
        db.commit()
        await interaction.response.send_message(lang["auto_embed_added"], ephemeral=True)

    @auto_commands.command(name="remove", description=lang["auto_commands_description_remove"])
    @has_permission()
    async def auto_remove(interaction: discord.Interaction, channel: discord.TextChannel = None):
        """
        Remove an auto embed from the channel
        :param interaction: discord.Interaction the interaction
        :param channel: discord.TextChannel the channel to remove the auto embed from
        :return: None
        """
        if channel is None:
            channel = interaction.channel
        db.execute("DELETE FROM autoEmbeds WHERE channel_id=?", (channel.id,))
        db.commit()
        await interaction.response.send_message(lang["auto_embed_removed"], ephemeral=True)

    tree.add_command(auto_commands)

    async def on_ready():
        db.execute("CREATE TABLE IF NOT EXISTS autoEmbeds (channel_id INTEGER PRIMARY KEY NOT NULL, embed_title TEXT NOT NULL, embed_description_before_message TEXT DEFAULT NULL, embed_description_after_message TEXT DEFAULT NULL)")
        db.commit()

    async def on_message(message: discord.Message):
        if message.author.bot:
            return
        if message.channel.type != discord.ChannelType.text:
            return
        auto_embed = db.execute("SELECT * FROM autoEmbeds WHERE channel_id=?", (message.channel.id,)).fetchone()
        if auto_embed is None:
            return
        message_content = message.content
        embed = discord.Embed(title=auto_embed[1], timestamp=message.created_at)
        if auto_embed[2] is not None: # Before
            embed.description = auto_embed[2] + "\n" + f"```{message_content}```"
        embed.description = message.content
        if auto_embed[3] is not None: # After
            embed.description = f"```{message_content}```" + "\n" + auto_embed[3]
        if auto_embed[2] is not None and auto_embed[3] is not None:
            embed.description = auto_embed[2] + "\n" + f"```{message_content}```" + "\n" + auto_embed[3]
        if auto_embed[2] is None and auto_embed[3] is None:
            embed.description = f"```{message_content}```"
        embed.set_author(name=message.author.name, icon_url=message.author.avatar.url)
        embed.set_thumbnail(url=message.guild.icon.url)
        embed.set_footer(text=message.guild.name, icon_url=message.guild.icon.url)
        await message.delete()
        await message.channel.send(embed=embed)

    if not hasattr(bot, "on_message_callbacks"):
        bot.on_message_callbacks = []
    bot.on_message_callbacks.append(on_message)

    if not hasattr(bot, "on_ready_callbacks"):
        bot.on_ready_callbacks = []
    bot.on_ready_callbacks.append(on_ready)

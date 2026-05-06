import discord
from discord import app_commands
import os

print("TOKEN =", os.getenv("TOKEN"))

TOKEN = os.getenv("TOKEN")

LOG_CHANNEL_ID = 1501476498706796554  # remplace par l'ID de ton salon logs
ALLOWED_ROLE_ID = 1501235658604413120  # remplace par l'ID du rôle "chaters"

class MyBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

bot = MyBot()

@bot.tree.command(name="shift", description="Enregistrer un shift")
@app_commands.describe(
    hours="Nombre d'heures",
    tips="Tips (€)",
    payout="Payout (€)"
)
async def shift(interaction: discord.Interaction, hours: float, tips: float, payout: float):

    # Vérification rôle
    if not any(role.id == ALLOWED_ROLE_ID for role in interaction.user.roles):
        await interaction.response.send_message("❌ Pas autorisé", ephemeral=True)
        return

    log_channel = interaction.client.get_channel(LOG_CHANNEL_ID)

    embed = discord.Embed(title="📊 Nouveau shift", color=0x00ff00)
    embed.add_field(name="👤 Membre", value=interaction.user.mention, inline=False)
    embed.add_field(name="🆔 ID", value=str(interaction.user.id), inline=False)
    embed.add_field(name="⏱ Heures", value=f"{hours}h")
    embed.add_field(name="💸 Tips", value=f"{tips}€")
    embed.add_field(name="💰 Payout", value=f"{payout}€")

    await log_channel.send(embed=embed)

    await interaction.response.send_message("✅ Shift envoyé", ephemeral=True)

bot.run(TOKEN)

import discord


class VoiceSetupView(discord.ui.Modal, title="Voice Setup"):
    name = discord.ui.TextInput(label="Ton nom", placeholder="Enter your name")

    async def on_submit(self, interaction):
        await interaction.response.send_message(f"Hello {self.name.value}")
    
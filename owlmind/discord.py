import re
import discord
from .botengine import BotMessage, BotBrain
from .genai import ask_genai  # <-- Import GenAI handler

class DiscordBot(discord.Client):
    """
    DiscordBot connects the Discord Runner with OwlMind's BotMind,
    forming a multi-layered context in BotMessage by collecting elements of the Discord conversation.
    """

    def __init__(self, token, brain: BotBrain, promiscous: bool = False, debug: bool = False):
        self.token = token
        self.promiscous = promiscous
        self.debug = debug
        self.brain = brain
        if self.brain:
            self.brain.debug = debug

        intents = discord.Intents.default()
        intents.messages = True
        intents.reactions = True
        intents.message_content = True

        super().__init__(intents=intents)
        return

    async def on_ready(self):
        print(f'Bot is running as: {self.user.name}.')
        if self.debug:
            print(f'Debug is on!')

    async def on_message(self, message):
        # CUT-SHORT conditions
        if message.author == self.user or \
           (not self.promiscous and not (self.user in message.mentions or isinstance(message.channel, discord.DMChannel))):
            if self.debug:
                print(f'IGNORING: orig={message.author.name}, dest={self.user}')
            return

        # Remove bot mention if any
        text = re.sub(r"<@\d+>", "", message.content).strip()

        # Collect attachments, reactions and others.
        attachments = None
        reactions = None

        # Handle special commands
        if text.lower().startswith("/summarize"):
            content_to_summarize = text[len("/summarize"):].strip()
            if content_to_summarize:
                prompt = f"Summarize the following text:\n{content_to_summarize}"
                summary = ask_genai(prompt)
                await message.channel.send(summary)
            else:
                await message.channel.send("❗ Please provide text to summarize after the /summarize command.")
            return

        if text.lower().startswith("/debug"):
            code_to_debug = text[len("/debug"):].strip()
            if code_to_debug:
                prompt = f"Find bugs and suggest improvements for the following code:\n{code_to_debug}"
                debug_suggestion = ask_genai(prompt)
                await message.channel.send(debug_suggestion)
            else:
                await message.channel.send("❗ Please provide code to debug after the /debug command.")
            return

        # Create context normally
        context = BotMessage(
            layer1=message.guild.id if message.guild else 0,
            layer2=message.channel.id if hasattr(message.channel, 'id') else 0,
            layer3=message.channel.id if isinstance(message.channel, discord.Thread) else 0,
            layer4=message.author.id,
            server_name=message.guild.name if message.guild else '#dm',
            channel_name=message.channel.name if hasattr(message.channel, 'name') else '#dm',
            thread_name=message.channel.name if isinstance(message.channel, discord.Thread) else '',
            author_name=message.author.name,
            author_fullname=message.author.global_name,
            message=text,
            attachments=attachments,
            reactions=reactions)

        if self.debug:
            print(f'PROCESSING: ctx={context}')

        # Process through Brain (SimpleBrain)
        if self.brain:
            self.brain.process(context)

            # Fallback logic if rule engine says "I have no idea how to respond!"
            if context.response and (
                context.response.strip().lower() == "i have no idea how to respond!"
                or context.response.strip().lower().startswith("(default)")
            ):

                if self.debug:
                    print("[DiscordBot] Fallback triggered — sending to GenAI with Tutor prompt...")
                prompt = (
                    "You are a professional tutor who explains technical concepts very clearly and thoroughly.\n"
                    "First, define the concept in simple words.\n"
                    "Then, give a real-world example.\n"
                    "Then, explain how it works step-by-step.\n"
                    "Imagine you are teaching a complete beginner.\n"
                    "Keep your explanation friendly and detailed, and do not exceed 20 lines.\n\n"
                    f"Concept: {context.get('message', '')}"
                )

                context.response = ask_genai(prompt)

        # Send response
        if context.response:
            # Limit response length to avoid Discord's 2000 character limit error
            if len(context.response) > 1900:
                context.response = context.response[:1900] + "..."
            await message.channel.send(context.response)
        return


    def run(self):
        super().run(self.token)

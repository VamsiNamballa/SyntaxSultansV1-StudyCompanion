from dotenv import dotenv_values
from owlmind.discord import DiscordBot
from owlmind.simplebrain import SimpleBrain

if __name__ == '__main__':

    # Load token from .env
    config = dotenv_values(".env")
    TOKEN = config['TOKEN']
    ## Alternative: Hard-code your TOKEN here and remove the comment:
    # TOKEN={My Token} 

    # Load SimpleBot Brain loading rules from a CSV
    brain = SimpleBrain(id='bot-1')
    brain.load('rules/bot-rules-2.csv')

    # Debugging Brain Load
    if brain.debug:
        print(f"SimpleBrain loaded {len(brain.plans)} rules.")
    
    # Start the Bot Runner process
    bot = DiscordBot(token=TOKEN, brain=brain, debug=True)
    
    # Run the bot
    bot.run()

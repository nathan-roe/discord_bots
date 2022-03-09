import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')
GUESS_LENGTH = 5
MAX_GUESSES = 5

class CustomClient(discord.Client):
    def __init__(self) -> None:
        super().__init__()
        abc = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'
        self.game = {
            'letters_left': abc,
            'all_letters': abc,
            'active': False,
            'answer': 'phone',
            'guess_count': 0,
            'play_again_observer': False
        }
        self.accuracy_arr = []

    async def on_message(self, message):
        if message.author == client.user:
            return

        if self.game['play_again_observer']:
            if message.content.lower() in ['y', 'yes']:
                await self.start_game(message)
                self.game['play_again_observer'] = False
            elif message.content.lower() in ['n', 'no']:
                self.game['play_again_observer'] = False
            else:
                await message.channel.send(f'Please enter y or n to continue...')
            return

        if message.content.lower() == "join nordle":
            await self.start_game(message)
        elif self.game['active']:
            if len(txt := message.content.lower()) == GUESS_LENGTH:
                if txt == self.game['answer'].lower():
                    five_green_squares = []
                    for _ in range(GUESS_LENGTH):
                        five_green_squares.append(':green_square:')
                    await message.channel.send(' '.join(five_green_squares) + '\nYOU WIN!!!!')
                    await self.end_game(message, True)
                else:
                    # remove characters in guess from letters left
                    idx = 0
                    for char in list(txt):
                        # return accuracy of guess
                        print(char, self.game['answer'][idx])
                        if char == self.game['answer'][idx]:
                            self.accuracy_arr.append(':green_square:')
                            self.game['letters_left'] = self.game['letters_left'].replace(char, char.upper())
                        elif char in self.game['answer']:
                            self.accuracy_arr.append(':yellow_square:')
                            self.game['letters_left'] = self.game['letters_left'].replace(char, char.upper())
                        else:
                            self.game['letters_left'] = self.game['letters_left'].replace(char, "_")
                            self.accuracy_arr.append(':white_large_square:')
                        idx = idx + 1
                    self.game['guess_count'] = self.game['guess_count'] + 1
                    if self.game['guess_count'] == MAX_GUESSES:
                        await self.end_game(message)
                        return
                    await message.channel.send(' '.join(self.accuracy_arr) + '\n' + self.game['letters_left'])
                    self.accuracy_arr = []
            else:
                await message.channel.send(f'Please enter a word that is {GUESS_LENGTH} characters long or enter exit\
                    to quit the game')
        return

    async def start_game(self, message):
        await message.channel.send(
            f'Welcome to Nordle, {message.author}!\n'
            +'Please make your first guess :)'
        )
        self.game['active'] = True

    async def end_game(self, message, success = False):
        if not success:
            await message.channel.send(
                f'{" ".join(self.accuracy_arr)}\n'
                + f'Sorry, the answer was {self.game["answer"]} :/ Want to play again? y/n'
            )
        self.game = {
            **self.game,
            'active': False,
            'letters_left': self.game['all_letters'],
            'answer': 'phone',
            'guess_count': 0,
            'play_again_observer': True
        }
        self.accuracy_arr = []

client = CustomClient()
client.run(TOKEN)
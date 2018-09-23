import functions
from functions.penalty_kick import User, Game, Leaderboard

# f = open('./functions/leaderboard.txt', 'rt')
# lines = f.readlines()
# f.close()
# for line in lines:
#     print(line)

def turn_on():
    print('== Welcome to the arcade ==')
    Leaderboard.read_score
    user = User(input('Please enter your name : '))
    score = Leaderboard(user.name, user.game.points)
    score.read_score()
    while True:
        try:
            select = int(input('''
            what would you like to do?\n
             1: earn token \n
             2: play game\n
             0:exit \n
             Input : '''))
            if select == 1:
                pass
            elif select == 2:
                print("Good idea! let's play a game")
                user.game.how_to()
                user.play()
                score.add_score()
            elif select == 0:
                print('Come again!')
                print('exiting game...')
                break
        except ValueError:
            print('must choose from 1, 2, or 0')

turn_on()

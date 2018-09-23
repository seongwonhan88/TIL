import random, datetime

class User():
    """
    """
    def __init__(self, name):
        """
        Takes name and gives 5 lives to start. Game class is called upon initation"""

        self.name = name
        self.life = 5
        self.game = Game(name, 'Impossible Penalty Kick')

    def play(self):
        """
        User gets to play while life lasts.
        Once life reaches 0, the loop is broken and shows the score"""

        print(f'you get {self.life} chaces to score. Good luck!')
        while self.life > 0:
            self.life -= 1
            self.game.kick()
            print(f'{self.life} left.')
        else:
            print('Game Over')
            print(f'Your total points are : {self.game.points}')

class Game():
    """
    Game is called from User class.
    Takes game user and title, points start at 0 when initiated"""
    def __init__(self,user, title):
        self.user = user
        self.title = title
        self.points = 0

    def how_to(self):
        print(f'{self.user}, you\'re playing {self.title}')
        print('''

            here is the goal

        :::::::::::::::::::::::::::
        :[ 1 ][ 2 ][ 3 ][ 4 ][ 5 ]:
        :[ 6 ][ 7 ][ 8 ][ 9 ][ 10]:
        :[ 11][ 12][ 13][ 14][ 15]:
        :          \o/            :
        ----------- @ <------------ World's best goal keeper
                   / \\


                    O <--- your ball

                    o <--- you
                   <|>
                   / \\

            enter the number you want to shoot at:
        ''')

    def kick(self):
        """
        This is the actual gaming method.
        It takes a number from terminal and compares with the list of random numbers.
        If the given number is not in the random numbered list, user gets 10 points(accumulative)"""
        try: #if not integer, it'll spit out
            self.shoot = int(input('enter the number you want to shoot at: '))
            if self.shoot in random.sample(list(range(1,16)), k=10):
                print('goal keeper stopped the ball')
            elif self.shoot not in random.sample(list(range(1,16)), k=10):
                print('goal went over the bar')
            else:
                print('you made it!')
                self.points += 10
        except ValueError:
            print('come on, you can\'t do that! must put integer between 1 to 15')


class Leaderboard():
    """
    Purely stands for score-keeping.
    The class takes name and the score from instances"""
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def read_score(self):
        f = open('./functions/leaderboard.txt', 'rt')
        lines = f.readlines()
        f.close()
        for line in lines:
            print(line)

    def add_score(self):
        f = open('./functions/leaderboard.txt', 'at')
        newline = f'{datetime.date.today()} : {self.name}, total {self.score} points \n'
        f.write(newline)
        f.close()

from random import randint

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def error_message( message ):
    print(f"{bcolors.FAIL}{message}{bcolors.ENDC}")

def red_message( message ):
    print(f"{bcolors.FAIL}{message}{bcolors.ENDC}")

def success_message( message ):
    print(f"{bcolors.OKGREEN}{message}{bcolors.ENDC}")

def information_message( message ):
    print(f"{bcolors.OKCYAN}{message}{bcolors.ENDC}")

class Avatar():
    damage_range = ""
    damage = 0
    life = 0
    hp_regeneration = 0

    def __init__( self, name ):
        self.name = name

    def receive_damage( self, damage ):
        self.life = self.life - damage
        message = "Name: {n}, Damage received: {d}, Actual life: {l}, Hp regeneration: {hp}".format( n = self.name, d = damage, l = self.life, hp = self.hp_regeneration) 
        if ( self.life <= 0 ):
            red_message( f"{self.name} dies" )
        else:
            red_message("-" * ( len(message) + 4 ))
            red_message("| " + message + " |")
            red_message("-" * ( len(message) + 4 ))

    def attack( self, enemy ):
        enemy.receive_damage( self.damage )

    def regeneration( self ):
        information_message(f'HP regeneration: {self.hp_regeneration}')
        quantity = 0
        while True:
            try:
                quantity = int(input("Insert the amount of regeneration: "))
                if quantity > self.hp_regeneration:
                    raise ArithmeticError
                break;
            except ArithmeticError:
                error_message("Insufficiente regeneration")
            except ValueError:
                error_message("Enter a valid quantity")

        self.hp_regeneration -= quantity
        self.life += quantity
        message = "Name: {n}, Actual life: {l}, Hp regeneration: {hp}".format( n = self.name, l = self.life, hp = self.hp_regeneration) 
        success_message("-" * ( len(message) + 4 ))
        success_message("| " + message + " |")
        success_message("-" * ( len(message) + 4 ) )

    @classmethod
    def information( cls ):
        return f"Damage: {cls.damage_range}, life: {cls.life}, hp regeneration: {cls.hp_regeneration}"

    @classmethod
    def select_avatar( cls ):
        player_name = input("Enter your name: ")
        option_avatar = ""
        while True:
            try:
                option_avatar = int(input(f"""{bcolors.OKCYAN}Choose your avatar: 
_____________________________________________________________________
| 1) Warrior - {Warrior.information()} |
| 2) Wizard - {Wizard.information()}   |
| 3) Dwafr - {Dwafr.information()}    |
¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
Enter 1, 2 or 3: {bcolors.ENDC}"""))
                if option_avatar <= 0 or option_avatar > 3:
                    raise ValueError
                break
            except ValueError:
                print(f"{bcolors.FAIL}Choose a valid option (1 - 2 - 3){bcolors.ENDC}")
                
        if( option_avatar == 1 ):
            return Warrior( player_name )
        elif( option_avatar == 2 ):
            return Wizard( player_name )
        elif( option_avatar == 3 ):
            return Dwafr( player_name )

    def __str__( self ):
        return """
Name: {n}
Life: {l}
Hp_regeneration: {hp}
""".format( n = self.name, l = self.life, hp = self.hp_regeneration )

class Warrior( Avatar ):
    damage_range = "(180 - 210)"
    damage = randint( 180, 210 )
    life = 1000
    hp_regeneration = 600

class Wizard( Avatar ):
    damage_range = "(170 - 190)"
    damage = randint( 170, 190 )
    life = 800
    hp_regeneration = 800

class Dwafr( Avatar ):
    damage_range = "(180 - 190)"
    damage = randint( 180, 190 )
    life = 900
    hp_regeneration = 700

def verify_players_0_hp( players ):
    for player in players:
        if player.life < 0:
            players.remove( player )

def print_players( players ):
    players_str = ""
    for idx, player in enumerate(players):
        players_str += "| {i} - {n} |".format( i = idx, n = player.name )
    print( players_str )

# Game
def game():
    print(f"""{bcolors.OKGREEN}
-'----------------------------'-
 | Welcome to World of Python |
-,----------------------------,-
{bcolors.ENDC}""")

    players = []
    number_players = 0

    while True:
        try:
            number_players = int(input("Enter the number of players: "))
            if number_players < 2:
                raise ArithmeticError
            break
        except ValueError:
            print(f"{bcolors.FAIL}Insert a valid number{bcolors.ENDC}")
        except ArithmeticError:
            print(f"{bcolors.FAIL}The number of players have to be more than 1{bcolors.ENDC}")

    for i in range(number_players):
        print(f"\n----- Player {i} ------")
        players.append(Avatar.select_avatar())

    while True:
        for idx, player in enumerate(players):
            # If only one player remains, he wins
            if( len( players ) == 1 ):
                print( f"{bcolors.OKGREEN}{players[0].name} wins{bcolors.ENDC}")
                return

            option = ""
            while True:                    
                try:
                    option = int(input(f"""{bcolors.OKCYAN}
{player.name}'s turn
_________________
| Options:       |
| 1) Attack      |
| 2) Regenerate  |
| 3) Information |
¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
Select 1, 2 or 3: {bcolors.ENDC}"""))
                    if option <= 0 or option > 3:
                        raise ArithmeticError
                    break
                except ArithmeticError:
                    error_message("Select an option between 1 - 3")
                except ValueError:
                    error_message("Insert a valid option")
            # Atack
            if option == 1:
                enemy = None
                if( len(players) == 2 ):
                    # Don't choose the enemy, because are only 2 players
                    enemy = players[1] if idx == 0 else players[0]
                else:
                    # Print all players and choose the enemy 
                    print_players( players )
                    while True:
                        try:
                            enemy_idx = int(input("Enter number of the enemy you want to attack: "))
                            # validation if the selected enemy index was the same player or index outside of the array
                            if enemy_idx == idx or  0 > enemy_idx or enemy_idx >= len(players):
                                raise ArithmeticError

                            enemy = players[ enemy_idx ]
                            break
                        except ArithmeticError:
                            print(f"{bcolors.FAIL}Error: You choosed yourself or a player outside of the list of players {bcolors.ENDC}")
                        except ValueError:
                            print(f"{bcolors.FAIL}Error: Insert a valid value{bcolors.ENDC}")
                player.attack( enemy )

            elif option == 2:
                # Regenerate hp
                player.regeneration()
            elif option == 3:
                # See the information of player
                print ( player )
                position = idx + 1 if idx < len( players ) - 1 else 0
                # The following is because this option doesn't take a turn for the player
                # Remove the player from the players array
                players.remove( player )
                # Then, insert the same player but in the next position of his current position to have the turn again
                players.insert( position, player )

            verify_players_0_hp( players )
game()
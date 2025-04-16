# def main():
#     print("hello, world!")

# if __name__ == "__main__":
#     main()

import random

MAXIMUM_LINES = 3
MAXIMUM_BET = 1000   
MINIMUM_BET = 1

ROWS = 3
COLUMNS = 3
#Dictionary of symblos and how many times the symbols can appear 
symbol_count = {  
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}
#values of each symbol while calculating the winning amounts for bet 
symbol_value = {   
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

def check_the_winnings(columns, lines, bet, values):
    """This function checks if the player won on any of the lines"""
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values [symbol] * bet
            winning_lines.append(line + 1)
    return winnings, winning_lines

def get_slot_machine_spin(rows, cols, symbols):
    """This function generate a random sloth machine spin and returns 2D list representing coloums filled with randomly chosen symbols"""
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)
    
    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns 

def print_slot_machine(columns):
    """This function prints the slot machine rows horizontally from the column-based data."""
    for row in range (len(columns[0])):
        for i, column in enumerate(columns):
            if i!= len(columns) - 1:
                print(column[row], end = " | ") #prevents new line and adds seperator
            else:
                print(column[row], end = "")   
            
        print()


def deposit_amount():
    """This function ask the user how much they wanto to deposit and returns the deposit amount"""
    while True:
        amount = input("How much do you want to deposit? $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print ("The amount must be greater than 0.")
        else:
                print ("Please enter a number.")

    return amount

def get_number_of_lines():
    """This function ask the user how many line they want to bet on and return the number of lines"""
    while True:
        lines = input(
            "Enter the number of lines to bet on (1-" + str(MAXIMUM_LINES) + ")? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAXIMUM_LINES:
                break
            else:
                print ("Please enter a valid number of lines.")
        else:
                print ("Please enter a number.")

    return lines
     

def get_bet():
    """This function ask the user hoew much they want to bet per line and returns bet amount per line"""
    while True:
        amount = input("How much do you want to bet on each line? $")
        if amount.isdigit():
            amount = int(amount)
            if MINIMUM_BET <= amount <= MAXIMUM_BET:
                break
            else:
                print (f"Amount must be between ${MINIMUM_BET} - ${MAXIMUM_BET}.")
        else:
                print ("Please enter a number.")

    return amount

def spin(balance):
    """This function executes a single spin round of the slot machine and returns net amount after winning and bet deduction"""
    lines = get_number_of_lines()
    while True: 
        bet = get_bet()
        total_bet = bet * lines
        if total_bet > balance:
            print(f"You do not have enough to bet that amount, your current balance is: ${balance}")
        else:
            break

    print(f"You are betting ${bet} on {lines} lines. Total bet is equal to: ${total_bet}")

    slots = get_slot_machine_spin(ROWS, COLUMNS, symbol_count)
    print_slot_machine(slots)

    winnings, winning_lines = check_the_winnings(slots, lines, bet, symbol_value)
    print(f"YOU WON ${winnings}.")
    print(f"You Won on lines:", *winning_lines)
    return winnings - total_bet

def main():
    """It is the main entry point of the slot machine game and handles game loop and balance updates"""
    balance = deposit_amount()
    while True: 
        print (f"Current balance is ${balance}")
        result = input("Press enter to spin (q to quit).")
        if result == "q":
            break
        balance += spin(balance)
    if __name__ == "__main__":
        print(f"You left with ${balance}")
main()






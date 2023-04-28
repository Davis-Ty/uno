#@Creator Tyon Davis

from multiprocessing import  Queue
import random
import threading
import time
from tkinter import *
import tkinter as tk


class Deck:
    def __init__(self):
        #creating list for deck of cards
        self.cards = []
        #calling funcion for our list
        self.create_deck()

    #(function) creates cards and adds to the list .cards
    def create_deck(self):
        for suit in ["Red", "Blue", "Green", "Yellow"]:
            for value in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "+2 (draw 2)", "+4 (draw 4)", "reverse"]:
                self.cards.append((value + " " + suit))
        for i in range(0, 2):
            self.cards.append("+1 shot to random player")     
        for i in range(0, 3):
            self.cards.append("Color Change")
            self.cards.append("designated driver")
        #calling function
        self.shuffle_deck()
       
    #(function) puts cards in random order
    def shuffle_deck(self):
        random.shuffle(self.cards)


    #(function) checks if it cand pull card from the deck if so it give the next card in the deck 
    def deal_card(self):
        if self.is_empty():
            self.create_deck()
            card = self.deal_card()
            return self.cards.pop() 
        else:
            #.pop() returns last card
            return self.cards.pop()
    #(function)- checks if deck is empty
    def is_empty(self):
        return len(self.cards) == 0

class Player:

    def __init__(self):
        #creating list for each player
        self.hand = []


    #(function) gives player a card 
    def draw_card(self, deck):
        #setting var to function
        card = deck.deal_card()
        #check if it can give a player another card
        if card is not None:
            self.hand.append(card)
        else:
            #if we can not get another card the game reloads the deck and continues to pass out cards
            deck.create_deck()# calling function
            card = deck.deal_card()
            self.hand.append(card)#adding card to player
            print("cards added")
            
    # start add comments
    #(function) checks if we have a winner
    def have_card(self, card):
        if card in self.hand:
            return True
        else:
            return False
    #(function) playes the card and removes from user hand
    def play_card(self, card):
        if card in self.hand:
            self.hand.remove(card)
            return True
        else:
            return False
    # end add comments
    #(Function) returns card value
    def get_hand(self):
        return self.hand

class Game:
    #(function)creating play deck starting the game
    def prep_hands(self, num_users, num_cards,queue):
        deck = Deck() #setting a var to deck class
        #(_)- is a placeholder... way of telling python dont worry about this 
        players = [Player() for _ in range(num_users)]# var is a list containing the class player for the num of people playing
        #looping for the amount of cards the user wants each player to have
        for i in range(num_cards):
            # loop for the amount players in the game
            for j in range(num_users):
                #getting our "key" (place of element that represents a player) and then calling our function draw_card in the class player after is called deck
                #deck calls the Deck class 1st
                players[j].draw_card(deck)
        # Print out each players hand on turn
        for i in range(num_users):
            #prints the number player using .format for looks
            print(f"Player {i+1}:")     
            #pring out the cards by calling function for each player
            for card in players[i].get_hand():
                print(card)
            print()
        # setting our var to the class so we can use the functions  of the class
        game=Game()
        deck=Deck()
        #starting the game
        game.play_game(players,deck,queue)

    #(Functon) to check if the card matches the playing card color or number returns true or false
    def card_checker(self,card1, card2):
        card1 = set(card1.split())
        card2 = set(card2.split())
        common_words = card1.intersection(card2)
        return len(common_words) > 0
    
    #(Function)- checks who turn it is and returns the the player element number back
    def next_player(self,players,first_turn, Clockwise):
        
        #checking if the rotation is going to the right or left.
        if Clockwise==True:
            if first_turn == len(players) - 1:
                first_turn = 0
                return first_turn
            else:
                first_turn = first_turn + 1
                return first_turn
        else:
            if first_turn == 0:
                first_turn = len(players) - 1
                return first_turn
            else:
                first_turn = first_turn - 1
                return first_turn
            
    def get_computer_card(self,players, played_cards, first_turn):
        player = players[first_turn]
        for card in player.get_hand():
            if player.have_card(card) and self.card_checker(card, played_cards[-1]):
                player.play_card(card)
                return card
            elif player.have_card(card) and card =="Color Change" or card =="designated driver" or  card=="+1 shot to random player":
                return card
        # If no valid card found, draw a card from the deck
        return "pull"
    
    def get_computer_color(self, players, played_cards, first_turn):
        player = players[first_turn]
        hand = player.get_hand()
        color_counts = {
            "Red": 0,
            "Blue": 0,
            "Green": 0,
            "Yellow": 0
        }
        for card in hand:
            for this_color in  color_counts:
                if player.have_card(card) and self.card_checker(card,this_color ):      
                    color_counts[this_color] += 1
        try:   
            # Get the color with the highest count
            max_color = max(color_counts, key=color_counts.get)
            return max_color
        except:
            color = random.choice(["Red", "Blue", "Green", "Yellow"])
            return color
        

    #(function)- actual game      
    def play_game(self, players, deck,queue):
        root = tk.Tk()
        game=Game()
        #keep tracke of played cards
        played_cards = []
        #setting first card faced up so user can have a card to start the game off with
        played_cards.append(deck.deal_card())
        #rotation starts off by going to the right first
        Clockwise=True
        #starting off with no winner
        winner=False
        

        i=0
        print(f"First card flipped \n {played_cards[i]} \n ")
        #getting random player to start off the game
        first_turn = random.randint(0, len(players) - 1)
        
        #start loop until we have a winner
        while not winner==True:
            
            first_turn=first_turn
            
            # get current time
            # start of turn
            start_time = time.time()
            
            
            # check if 15 seconds have passed
            while not time.time() - start_time >= 15 and not winner ==True:
                
                #checking if facecard is a special card and changes it 
                while(played_cards[i]=="+1 shot to random player" or played_cards[i]=="Color Change" or played_cards[i]=="designated driver"):
                    played_cards.append(deck.deal_card())
                    i=i+1 
                    print(f"\nCurrent card: {str(played_cards[i])} \n")
                print(f"Player {first_turn+1}:")
                #prints out cards in players hand
                for card in players[first_turn].get_hand():
                    print(card)

                #prompts player to play a card

                #hit_card_down = input(f"Play a card, Player {first_turn+1}: ")
                hit_card_down = self.get_computer_card(players, played_cards, first_turn)
                    
                #checks if player has the card
                if players[first_turn].have_card(hit_card_down) and hit_card_down=="+1 shot to random player" or hit_card_down=="Color Change" or hit_card_down=="designated driver" or game.card_checker(str(hit_card_down), str(played_cards[i])):
                    #remves card from player hand
                    players[first_turn].play_card(hit_card_down)
                    #checks if we have a winner 
                    if len(players[first_turn].get_hand()) == 0:
                        #add drink
                        
                        print(f"Player {str(first_turn+1)} is the winner \n drink formula \n")
                        queue.put(f"Player {first_turn+1}")
                        winner=True
                    else:
                        #checks if card was special 
                        if (hit_card_down=="Color Change"):
                            #ask user to input a color 
                            #color=(input("Enter a color: "))
                            color=self.get_computer_color(players, played_cards, first_turn)
                            while color not in ["Red", "Blue", "Green", "Yellow"]:
                                print("\nthat color is not available")
                                #color=(input("Enter a color: "))
                                color=self.get_computer_color(players, played_cards, first_turn)

                            played_cards.append(color)
                        elif(hit_card_down=="designated driver" or hit_card_down=="+1 shot to random player"):
                            #lets user skip a shot a face card gets pull from deck
                            played_cards.append(deck.deal_card())
                        else:
                            #gives next play +2 cards and skips them
                            if game.card_checker (("+2"), str(hit_card_down)):
                                try:
                                    players[first_turn+1].hand.append(deck.deal_card())
                                    players[first_turn+1].hand.append(deck.deal_card())
                                    first_turn=game.next_player(players,first_turn,Clockwise)
                                    
                                except:
                                    players[0].hand.append(deck.deal_card())
                                    players[0].hand.append(deck.deal_card())
                                    first_turn=game.next_player(players,first_turn,Clockwise)
                                    
                            elif game.card_checker (("reverse"), str(hit_card_down)):
                                #changes rotation of the game
                                if Clockwise==True:
                                    Clockwise=False
                                    
                                else:
                                    Clockwise=True
                                    
                            elif game.card_checker (("+4"), str(hit_card_down)):
                                #gives next play +4 cards and skips them adds card as face card
                                try:
                                    players[first_turn+1].hand.append(deck.deal_card())
                                    players[first_turn+1].hand.append(deck.deal_card())
                                    players[first_turn+1].hand.append(deck.deal_card())
                                    players[first_turn+1].hand.append(deck.deal_card())
                                    first_turn=game.next_player(players,first_turn,Clockwise)
                                    
                                except:
                                    players[0].hand.append(deck.deal_card())
                                    players[0].hand.append(deck.deal_card())
                                    players[0].hand.append(deck.deal_card())
                                    players[0].hand.append(deck.deal_card())
                                    first_turn=game.next_player(players,first_turn,Clockwise)
                                    
                            played_cards.append(hit_card_down)
                        i=i+1
                        print(f"\n Card that was just played \n {played_cards[i]} \n")
                        first_turn=game.next_player(players,first_turn,Clockwise)
            
                else:
                    #lets player pull card from the deck and change turn
                    if  hit_card_down=="pull":
                            players[first_turn].hand.append(deck.deal_card())
                            print(f"card added \n \n {played_cards[i]}\n")
                            first_turn=game.next_player(players,first_turn,Clockwise)
                    else:
                        #makes user repick a card
                        print(f"Invalid card. Try again.\n \n Last Played card \n {played_cards[i]} \n")
            #time is up
            else: 
                if (winner):
                    continue
                else:
                    # must fix it to skip player on auto
                    hit_card_down ="pull"
                    print("Time's up! Drawing a card from the deck...")
                    first_turn=game.next_player(players,first_turn,Clockwise)
                        

    def get_game_settings(self):
        root = tk.Tk()

       
        # create a canvas with a green background
        canvas = tk.Canvas(root,  bg="green")
        canvas.pack()

        # create a label for the first question
        question1_label = tk.Label(root, text="Enter the number of players:",bg="Yellow")
        question1_label.place(x=10, y=10)

        # create the first text box with number validation
        vcmd = root.register(self.validate_numeric_entry)
        text_box1 = tk.Entry(root, validate="key", validatecommand=(vcmd, '%S'))
        text_box1.place(x=10, y=30)

        # create a label for the second question
        question2_label = tk.Label(root, text="Enter the number of cards for each player:",bg="Yellow")
        question2_label.place(x=10, y=60)

        # create the second text box with number validation
        text_box2 = tk.Entry(root, validate="key", validatecommand=(vcmd, '%S'))
        text_box2.place(x=10, y=80)

        # create a button to submit the values
        submit_button = tk.Button(root, text="Start game", command=root.quit)
        submit_button.place(x=10, y=120)

        #canvas.lower(canvas) # to move the image behind textboxes

        root.mainloop()

        num_users = int(text_box1.get())
        num_cards = int(text_box2.get())

        # Close the GUI window
        root.destroy()

        return num_users, num_cards

    def validate_numeric_entry(self, text):   
        #Validation function for text boxes that only allows numeric input
        
        if text.isdigit() or text == "":
            return True
        else:
            return False
        
    def start_game_thread(self):
        
        winners = []  # create a list to hold all the winners
        group_winners = []
        lock = threading.Lock()
        while True:
            # get game settings from user
            num_users, num_cards = self.get_game_settings()
            if num_users > 8:
                # divide players into 2 groups of 8 or less
                num_groups = (num_users + 7) // 8
                group_size = (num_users + num_groups - 1) // num_groups
                groups = [range(i * group_size, min((i+1) * group_size, num_users)) for i in range(num_groups)]

                # play each group's game separately
                
                for group in groups:
                    # create queue for storing winners
                    winners_queue = Queue()

                    # start game thread
                    game_process = threading.Thread(target=self.prep_hands, args=(len(group), num_cards, winners_queue))
                    game_process.start()

                    # wait for game to finish
                    game_process.join()

                    # get winner from queue
                    winner = winners_queue.get()
                    lock.acquire()
                    group_winners.append(winner)
                    lock.release()

                # start final game with group winners
                winners_queue = Queue()
                lock = threading.Lock()
                game_process = threading.Thread(target=self.prep_hands, args=(len(group_winners), num_cards, winners_queue))
                game_process.start()

                # wait for game to finish
                game_process.join()

                # get final winner from queue
                winner = winners_queue.get()
                lock.acquire()
                winners.append(winner)
                lock.release()
            else:
                # create queue for storing winners
                winners_queue = Queue()
                # start game thread
                game_process = threading.Thread(target=self.prep_hands, args=(num_users, num_cards, winners_queue))
                game_process.start()

                # wait for game to finish
                game_process.join()

                # get winner from queue
                winner = winners_queue.get()
                lock.acquire()
                winners.append(winner)
                lock.release()

            # ask user if they want to play again
            play_again = input(f"The winner is {winner}. Play again? (y/n) ")

            if play_again.lower() == "n": 
                print("Total number of wins:")
                winners_dict = {}
                for player in winners and group_winners:
                    if player in winners_dict:
                        winners_dict[player] += 1
                    else:
                        winners_dict[player] = 1

                for player, wins in winners_dict.items():
                    print(f"{player} won {wins} times.")
                print("displays for large groups.")
                break

if __name__=='__main__':
    
    #setting class to var
    dRuNk_UnO= Game()
    #creating our thread calling
    game_thread = threading.Thread(target= dRuNk_UnO.start_game_thread, args=())
    game_thread.start()
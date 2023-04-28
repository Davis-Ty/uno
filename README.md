Author: 
Tyon Davis 
?
HOW
• The game is played with a deck of cards that contains the following cards: 1-10 in four colors (red, blue, green, and yellow), "Skip" in four colors, "Reverse" in four colors, "+2" in four colors, "+4", "Color Change", "Designated Driver", and "+1 shot to random player".
• The objective of the game is to be the first player to get rid of all their cards. Each player takes turns playing cards that match the color or number of the top card on the discard pile. If a player cannot play a card, they must draw a card from the deck. Special cards have different effects.
• "Reverse": The direction of play is reversed.
• "+2": The next player must draw two cards and skip their turn.
• "+4": The next player must draw four cards and skip their turn. The player who plays this card also gets to choose the color that play continues with.
• "Color Change": The player who plays this card gets to choose the color that play continues with.
• "Designated Driver": The player who plays this card must choose another player to not drink until the end of the game.
• "+1 shot to random player": The player who plays this card chooses another player to take a shot of alcohol.
































Explain Diagram
	Player has the following methods:
• __init__(): creates an empty list of cards in the player's hand.
• draw_card(deck): takes a deck object and draws a card from it, adding it to the player's hand. If the deck is empty, it calls create_deck() and tries to draw a card again.
• have_card(card): checks if a specified card is in the player's hand and returns True or False.
• play_card(card): removes a specified card from the player's hand if it is there and returns True, otherwise returns False.
• get_hand(): returns a list of the cards currently in the player's hand.

Deck has the following methods:
• __init__(): creates an empty list of cards and calls create_deck() to populate the list and shuffle the cards.
• create_deck(): creates a standard deck of cards, including numeric cards, action cards (+2, +4, reverse), and special cards (designated driver, color change), and shuffles them.
• shuffle_deck(): shuffles the deck of cards.
• deal_card(): checks if there are any cards left in the deck and deals the next card, or creates a new deck and deals the next card if the deck is empty.
• is_empty(): checks if the deck is empty.


The main class is called Game, which has four methods:
• prep_hands(): This method creates the deck, shuffles the cards, deals a certain number of cards to each player, and starts the game.
• card_checker(): This method checks if a card matches the playing card in either color or number.
• next_player(): This method checks whose turn it is and returns the player number of the next player.
• play_game(): This method is the actual game, where each player takes turns playing cards until someone wins.
It also has two methods that are called from within the play_game() method:
• get_computer_card(): This method returns the computer's card choice.
• get_computer_color(): This method returns the computer's color choice.
There is also a commented-out line that prompts the user to input their card choice.


• cl “Uno Rules - the Original Uno Card Game Rules.” Www.unorules.com, www.unorules.com/. “UNO | Mattel Games.” Mattelgames.com, 2020, www.mattelgames.com/enus/cards/uno.
• Accessed 19 Mar. 2023. “Log in with Twitter.” Developer.twitter.com, developer.twitter.com/en/docs/authentication/guides/log-in-with-twitter. (test trail)
• https://opengameart.org/content/10-seamless-grass-textures-that-are-2048-x-2048-grass-2png (GUI test trail)
• DrUInk UnO: Lucidchart
• JavaLocks - Adv Topics in Par Dist Comp Section 01 Spring Semester 2023 CO (usg.edu)
       
Spring 2023 CSCI 4308 Term Project Progress
yOu KnOw DrUnK?


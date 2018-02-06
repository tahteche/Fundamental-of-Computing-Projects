# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.cards = []

    def __str__(self):
        # return a string representation of a hand
        ans = ""
        for card in self.cards:
            ans += " " + str(card)        
        return "Hand contains" + ans        

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)
        return self.cards

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        
        value = 0
        aces = 0
        for card in self.cards:
            value += VALUES[card.get_rank()]
            if( VALUES[card.get_rank()] == 'A'):
                aces += 1
        
        if (value <= 11 and aces == 1):
            value += 10        
        return value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        x_axis = pos[0]
        y_axis = pos[1]
        for card in self.cards:
            card.draw(canvas, (x_axis, y_axis))
            x_axis += CARD_SIZE[0] +10
 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.cards)
       
    def deal_card(self):
        # deal a card object from the deck
        return self.cards.pop()
    
    def __str__(self):
        # return a string representing the deck
        ans = ""
        for card in self.cards:
            ans += " " + str(card)        
        return "Deck contains" + ans  


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, score
    if(in_play):
        outcome = "You forfeited!"
        score -= 1
        
    outcome = ""
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    dealer_hand = Hand()
    
    i = 1
    while i <= 2:
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        i += 1    
    in_play = True

def hit():
    # replace with your code below
 
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
    global in_play, score, outcome
    
    if (player_hand.get_value() <= 21 and dealer_hand.get_value() <= 21):    
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())

        if( player_hand.get_value() > 21):
            outcome = "You have busted!"
            in_play = False
            score -= 1
            
        if( dealer_hand.get_value() > 21):
            outcome = "Dealer has busted!"
            in_play = False
            score += 1
        
def stand():
    # replace with your code below
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score
    
    global in_play, score, outcome

    if( player_hand.get_value() > 21):
        outcome = "You have busted!"
        score -= 1
    else:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        if(dealer_hand.get_value() > 21):
            outcome = "Dealer has busted!"
            in_play = False
            score += 1
            
        elif(dealer_hand.get_value() < player_hand.get_value()):            
            outcome = "Player Wins!"
            in_play = False
            score += 1
            
        else:
            outcome =  "Dealer Wins"
            in_play = False
            score -= 1
            
# Helper functions
def draw_card_back(canvas, pos):        
    canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

# draw handler    
def draw(canvas):
    global in_play, score, outcome 
    # test to make sure that card.draw works, replace with your code below
    
    canvas.draw_text("Blackjack", (10, 35), 32, "blue")
    canvas.draw_text("Score: " + str(score), (400, 40), 28, "black")
    
    canvas.draw_text("Dealer", (10, 100), 24, "black")
    canvas.draw_text(outcome, (400, 100), 20, "black")
    dealer_hand.draw(canvas, (10, 120))
    
    canvas.draw_text("Player", (10, 270), 24, "black")
    player_hand.draw(canvas, (10, 290))
    
    if(in_play):
        canvas.draw_text("Hit or stand?", (400, 270), 20, "black")
        draw_card_back(canvas, (10, 120))
    else:
        canvas.draw_text("New Deal?", (400, 270), 20, "black")

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric

# implementation of card game - Memory

import simplegui
import random

CARD_DIMENSION = (50, 100)

def card_angles(card_number):
    
    ''' Returns a list with 4 points which are the angles of the card'''
    top_left = (CARD_DIMENSION[0] * card_number, 0)
    top_right = (CARD_DIMENSION[0] + CARD_DIMENSION[0] * card_number, 0)
    bottom_right = (CARD_DIMENSION[0] + CARD_DIMENSION[0] * card_number, CARD_DIMENSION[1])
    bottom_left = (CARD_DIMENSION[0] * card_number, CARD_DIMENSION[1])
    return [top_left, top_right, bottom_right, bottom_left]

def clicked_card(pos):
    '''Takes a click point and returns the index of the 
        card on which the point us found'''
    for card in range(16):
        card_right_side = CARD_DIMENSION[0] + CARD_DIMENSION[0] * card
        card_left_side = CARD_DIMENSION[0] * card
        if( (pos[0] > card_left_side) and (pos[0] < card_right_side) ):
            return card

# helper function to initialize globals
def new_game():
    global flipped_card1, flipped_card2, state, turns, cards, exposed
    flipped_card1 = None
    flipped_card2 = None
    state = 0
    turns = 0
    
    exposed = range(0, 16)
    for card in exposed:
        exposed[card] = False
        
    cards = range(0, 8)
    cards.extend(range(0, 8))
    
    random.shuffle(cards)
     
# define event handlers
def mouseclick(pos):
    global flipped_card1, flipped_card2, state, turns, cards, exposed
    if state == 0:
        state = 1
        exposed[clicked_card(pos)] = True
        flipped_card1 = clicked_card(pos)
    elif state == 1:
        state = 2
        exposed[clicked_card(pos)] = True
        flipped_card2 = clicked_card(pos)
        turns += 1
        label.set_text("Turns = " + str(turns))
    else:
        state = 1
        if( cards[flipped_card1] != cards[flipped_card2] ):
            exposed[flipped_card1] = False
            exposed[flipped_card2] = False
        exposed[clicked_card(pos)] = True
        flipped_card1 = clicked_card(pos)
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):    
    card_pos_x = 20
    for card in cards:
        canvas.draw_text(str(card), (card_pos_x,50), 30, 'white')
        card_pos_x += 50
    
    for card in range(len(exposed)):
        if( not exposed[card]):
            canvas.draw_polygon(card_angles(card), 1, 'white', 'green')


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric

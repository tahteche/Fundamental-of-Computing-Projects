"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_permutations(outcomes, length):
    '''
    Iterative function that list all permutations of outcomes of 
    given length.
    '''
    indexes = [()]
    for dummy_idx in range(length):
        temp = []
        for seq in indexes:
            for idx in range(len(outcomes)):
                new_seq = list(seq)
                if idx in new_seq:
                    continue
                new_seq.append(idx)
                temp.append(new_seq)
                
        indexes = temp
    
    permutations = []
    for seq in indexes:
        new_seq = []
        for idx in seq:
            new_seq.append(outcomes[idx])
        new_seq = tuple(new_seq)
        permutations.append(new_seq)
    return permutations


def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    scores = dict()
    hand_set = set(hand)
    
    for item in hand_set:
        die_score = item * hand.count(item)
        scores[item] = die_score
        
    max_score = -1
    for val in scores.values():
        if val > max_score:
            max_score = val
            
    return max_score


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcomes = []
    free_dice_outcomes = gen_all_sequences(range(1, num_die_sides + 1), num_free_dice)
       
    for free_dice_outcome in free_dice_outcomes: 
        outcomes.append(held_dice + free_dice_outcome)
    
    scores = []
    for outcome in outcomes:
        scores.append(score(outcome))
        
    ans = float(sum(scores)) / len(scores)
    
    return ans


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    all_holds = set([])
    for length in range(len(hand)+1):
        sequences = gen_permutations(hand, length)
        sorted_sequences = [tuple(sorted(sequence)) for sequence in sequences]
        all_holds.update(sorted_sequences)
    
    return all_holds

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_holds = list(gen_all_holds(hand))
    exp_values = []
    for hold in all_holds:
        exp_val = expected_value(hold, num_die_sides, len(hand) - len(hold))
        exp_values.append(exp_val)
    
    max_exp_val = max(exp_values)
    best_hold_idx = exp_values.index(max_exp_val)
    best_hold = all_holds[best_hold_idx]
    
    return (max_exp_val, best_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
run_example()

#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    




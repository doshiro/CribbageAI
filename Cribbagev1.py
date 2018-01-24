###############################################################################
#
#  Python program to play Cribbage, maybe
#  May or may not work correctly. Let's find out!
#
###############################################################################

#import libraries
import random
from Player import Player
from Hand import Hand


# Define constants
DECK_SIZE = 52


#Define arrays for cards
CARDS = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
SUITS = [" of Clubs", " of Diamonds", " of Hearts", " of Spades"]

#Define arrays for deck
deck = [0] * 52
cutCard = -1

# make new players
player1 = Player( "Player 1" )
player2 = Player( "Player 2" )

# make refs for dealer and other player
dealer = player1
second = player2

#make a crib
crib = Hand()

#make a discard pile
discard = []

def displayBreak():

    print( )
    print( "----------------------" )
    print( )

def throwParse( throw, butNot ):

    #try to parse to int
    try:
        #make sure they give us a valid index
        if( int(throw) >= 0 and int(throw) < 6 and int(throw) != butNot ):
            return int(throw)
        else:
            print("Please give a number 0-5")
            return -1
    except:
        print("Please give a number 0-5")
        return -1

#stuff for checking the score 
def checkScore( score, discard, player ):

    #make 5ddsure the pile is nonempty
    if len( discard ) == 0:

        # exit prematurely
        return 0
 

    #check if we are at 15
    if score == 15:

        # denote and move player 2
        print( "15 for 2!" )
        player.move( 2 )

    elif score == 31:

        # denote and move player 2
        print( "31 for 2!" )
        player.move( 2 )

    
    #make variable for last index
    depth = len( discard ) - 1

    #booleans for keeping track of 4, 3 of a kind
    fourFound = False
    threeFound = False

    #booleans for keeping track of runs
    run = False

    for x in range( 6, 1, -1 ):

        # check for runs of x
        if depth >= x:

            # make a copy of the last x cards in the discard pile for checking runs
            discardCopy = []
            for y in range( depth, depth - x - 1, -1 ):
                discardCopy.append( discard[y] )

            # sort the copied array
            discardCopy.sort()

            #get the greatest card
            top = discardCopy[ len(discardCopy) - 1 ]

            # assume we have a run
            run = True

            # check the cards for a run of x + 1
            for z in range( 1, x + 1 ):
                if top - z != discardCopy[ x - z ]:
                    run = False

        if run:

            length = str( x + 1 )
            print( "Run of " + length + " for " + length + "!" )
            player.move( x + 1 )
            break

    
    #check for 4 of a kind
    top = discard[ depth ]

    if depth >= 3:
        #check for 4 of a kind
        if top == discard[depth-1] and top == discard[depth-2] and top == discard[depth-3]:

            # denote we have a 4 of a kind and move
            print( "4 of a kind for 12!")
            player.move( 12 )
            fourFound = True

    #check for a 3 of a kind
    if not fourFound:

        # make sure there are three cards in the pile
        if depth >= 2:

            if top == discard[depth-1] and top == discard[depth-2]:

                # denote we have a 3 of a kind and move
                print( "3 of a kind for 6!" )
                player.move( 6 )
                threeFound = True            

        if depth >= 1 and not threeFound:

            # check for pair
            if top == discard[depth-1]:

                # denote we have a pair and move
                print( "Pair for 2!" )
                player.move( 2 )

    # show the score
    displayBreak()
    print( "The score is " + str( score ) + "\n" ) 

# 
def peg( player, discard, points ):

    #player plays card if they can
    move = player.play( points, discard, None, False )


    # if they player made a legit move
    if move > 0:

        # add that to the score
        if move > 10:
            points += 10
        else:
            points += move

        # check the score
        checkScore( points, discard, player )

    #let us know what the score is
    return points

# picks random, non-dealt card
def cut():

    #Denote we begin to cut the deck
    print( "\nCutting the deck!" )

    #Store the number of the cut in card
    cutCard = random.randint( 13, 51 )

    #print the card that was cut
    print( "The cut was " + Hand.cardString(cutCard) )

    #check if card is a jack
    if Hand.cardValue( cutCard )[0] == 10:
        print( "Jack was cut! 2 points to the dealer!" )
        dealer.move( 2 )

    return cutCard

#Populate deck with numbers 0 - 51 at each index
for x in range(1, 51):
    deck[x] = x

#play until someone wins
while( True ):

    #Shuffle the deck to get a random order
    random.shuffle(deck)


    #loop to populate hands
    for x in range(0, 12):
        # send even cards to player 1
        if x % 2 == 0:
            # give the card to player 1
            second.hand.addCard( deck[x] )

        #Send odd cards to player 2
        else:
            # give the card to player 2
            dealer.hand.addCard( deck[x] )

    # print out cards
    print("Second")
    second.hand.showCards( 6 )
    print("Dealer")
    dealer.hand.showCards( 6 )

    in1 = -1
    in2 = -1
    in3 = -1
    in4 = -1

    print("\nSecond")

    #Print out cards to throw and prompt
    while in1 == -1:
        #get user input
        throw1 = input("Please choose the index of the first card to throw: ")
        
        #parse said input
        in1 = throwParse( throw1, -1 )

    while in2 == -1:
        #get user input
        throw2 = input("Please choose the index of the second card to throw: ")

        #parse said input
        in2 = throwParse( throw2, in1 )

    displayBreak()

    print("\nDealer")
    while in3 == -1:

        #get user input
        throw3 = input("Please choose the index of the first card to throw: ")

        #parse input
        in3 = throwParse( throw3, -1 )

    while in4 == -1:
        #get user input
        throw4 = input("Please choose the index of the second card to throw: ")
        in4 = throwParse( throw4, in3 )

    #store the new hands
    second.hand.throw( in1, in2, crib )
    dealer.hand.throw( in3, in4, crib )

    #update playable cards
    second.update()
    dealer.update()
    
    #print cards in new hands
    print("Throwing complete! \n")

    #print hand 1
    print("Second")
    second.hand.showCards( 4 )

    #print hand 2
    print()
    print("Dealer")
    dealer.hand.showCards( 4 )

    #print crib
    print()
    print("Crib")
    crib.showCards( 4 )

    #print the cut
    cutCard = cut()


    #create pointers for turns
    last = second
    other = dealer

    # set score to 0
    score = 0

    # make storing references
    lastStore = last
    otherStore = other

    # while a player can peg
    while second.playing or dealer.playing:

        # make sure one person is able to play
        if not second.ableToPeg and not dealer.ableToPeg:
                
            #swap
            last = lastStore
            other = otherStore

            last.ableToPeg = True
            other.ableToPeg = True
    
            # make sure we're not at 31
            if score != 31:

                #give 1 point to whoever played last
                print( "1 for last card!" )
                other.move( 1 )

            # reset score and empty discard
            score = 0
            discard = []


        if last.ableToPeg:
            # second person takes turn
            score = peg( last, discard, score )

            if not other.ableToPeg:
                lastStore = other
                otherStore = last


        if other.ableToPeg:
            # dealer takes turn
            score = peg( other, discard, score )

    if score != 31:

        #give 1 point to whoever played last
        print( "1 for last card!" )
        otherStore.move( 1 )



    #count hands!
    print( "\nCounting hands!" )
    print("Second")
    second.move( second.hand.score(cutCard, False) )


    print("\nDealer")
    dealer.move( dealer.hand.score(cutCard, False) )

    print("\nCrib")
    dealer.move( crib.score(cutCard, True) )


    #clear all hands
    player1.hand.clear()
    player2.hand.clear()
    crib.clear()

    #swap second and dealer
    tmp = dealer
    dealer = second
    second = tmp

    #determine if we want to continue
    if input( "Continue? (y/n) = " ) == "n":
        print( "Exiting..." )
        exit()

    else:
        print( "Continuing!")

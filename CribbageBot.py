###############################################################################
#
#  Python program to play Cribbage, maybe
#  May or may not work correctly. Let's find out!
#
###############################################################################

#import libraries
import random
from PlayerBot import Player
from Hand import Hand
from DumbAI import DumbAI

# Define constants
DECK_SIZE = 52


#Define arrays for cards
CARDS = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
SUITS = [" of Clubs", " of Diamonds", " of Hearts", " of Spades"]

#Define arrays for deck
deck = [0] * 52
cutCard = -1

# make new players
player1 = Player( "Human" )
player2 = Player( "DumbAI" )

# make refs for dealer and other player
dealer = player1
second = player2

#make a crib
crib = Hand()

#make a discard pile
discard = []

# make a dumb ai
dumb = DumbAI()

#keep track of when the human is the dealer
humanDealer = True

#keep track of who threw the last card
lastPlayer = player1

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
            top = discardCopy[ len( discardCopy ) - 1 ]

            # assume we have a run
            run = True

            # check the cards for a run of 7
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
    print( "Discard pile: " )
    print( discard )
    

# 
def peg( player, discard, points, isAi ):

    # player moves if they can
    move = player.play( points, discard, dumb, isAi )

    # if they player made a legit move
    if move > 0:

        # add that to the score
        if move > 10:
            points += 10
        else:
            points += move

        #check the score
        checkScore( points, discard, player )

    #let us know what the score is
    return points


# picks random, non-dealt card
def cut():

    #Denote we begin to cut the deck
    print( "\nCutting the deck!" )

    #Store the number of the cut in card
    cutCard = deck[random.randint( 12, 51 )]

    #print the card that was cut
    print( "The cut was " + Hand.cardString( cutCard ) )

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

    # check when the ai plays this turn
    aiLast = humanDealer

    # denote who is dealing
    print( dealer.name + " is dealing!\n\n" )

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

    # print out the human's
    if not humanDealer:
        print( second.name )
        second.hand.showCards( 6 )
    else: 
        print( dealer.name )
        dealer.hand.showCards( 6 )

    # stuff for keeping track of the input / output
    in3 = -1
    in4 = -1
    displayBreak()


    # print name of human player hand
    print( "Human" )

    while in3 == -1:

        #get user input
        throw3 = input("Please choose the index of the first card to throw: ")

        #parse input
        in3 = throwParse( throw3, -1 )

    while in4 == -1:
        #get user input
        throw4 = input("Please choose the index of the second card to throw: ")
        in4 = throwParse( throw4, in3 )
    
    # determine the AI's throw and throw
    if aiLast:
        aiThrow = dumb.determineThrow( second.hand )
        second.hand.throw( aiThrow[0], aiThrow[1], crib )
        dealer.hand.throw( in3, in4, crib )

    else: 
        aiThrow = dumb.determineThrow( dealer.hand )
        second.hand.throw( in3, in4, crib )
        dealer.hand.throw( aiThrow[0], aiThrow[1], crib )

    #update playable cards
    second.update()
    dealer.update()
    
    #print cards in new hands
    print("Throwing complete! \n")

    # show the human's hand
    if not humanDealer:
        print( second.name )
        second.hand.showCards( 4 )
    else:
        print( dealer.name )
        dealer.hand.showCards( 4 )

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

    # denote that everyone is again able to play
    second.playing = True
    dealer.playing = True
    second.ableToPeg = True
    dealer.ableToPeg = True

    # while a player can peg
    while second.playing or dealer.playing:

        # make sure one person is able to play
        if not second.ableToPeg and not dealer.ableToPeg:

            # verify we swap
            if not lastStore == last:
                #swap ai's position
                aiLast = not aiLast

            #swap
            last = lastStore
            other = otherStore

            # denote we are again able to peg
            if last.playing:
                last.ableToPeg = True

            if other.playing:
                other.ableToPeg = True
    
            # make sure we're not at 31
            if score != 31:

                #give 1 point to whoever played last
                print( "1 for last card!" )
                lastPlayer.move( 1 )
            
            # reset score and empty discard
            score = 0
            discard = []


        if last.ableToPeg:

            # keep track of score before move
            score1 = score

            # if the ai is the last
            if aiLast:
                # second person takes turn
                score = peg( last, discard, score, True )

            # if the human is the last
            else:
                score = peg( last, discard, score, False )

            # check if the score has changed
            if not score1 == score:

                #update the last player
                lastPlayer = last


            # switch players if we're last and able to play after
            if not other.ableToPeg and last.playing and other.playing:
                lastStore = other
                otherStore = last


        if other.ableToPeg:
            
            #keep track of the score before move
            score1 = score

            # if ai is the other
            if not aiLast:
                score = peg( other, discard, score, True )

            # otherwise human takes this turn
            else:
                score = peg( other, discard, score, False )

            if not last.playing:
                otherStore = other

            # check if the move was legit
            if not score1 == score:

                #update last player
                lastPlayer = other


    if score != 31:

        #give 1 point to whoever played last
        print( "1 for last card!" )
        lastPlayer.move( 1 )



    #count hands!
    print( "\nCounting hands!" )
    print( "The cut was: " + Hand.cardString( cutCard ) + "\n" )

    print()
    print( second.name )
    second.move( second.hand.score(cutCard, False) )

    print()
    print( dealer.name )
    dealer.move( dealer.hand.score(cutCard, False) )

    print("\n" + dealer.name + "'s Crib")
    dealer.move( crib.score(cutCard, True) )


    #clear all hands
    dealer.hand.clear()
    second.hand.clear()
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

        #print game information
        print( "Continuing!\n")
        print( second.name + " is at " + str( second.position ) )
        print( dealer.name + " is at " + str( dealer.position ) )

        humanDealer = not humanDealer

        #reset score and discard
        score = 0
        discard = []

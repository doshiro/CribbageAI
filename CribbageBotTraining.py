###############################################################################
#
#  Python program to play Cribbage, maybe
#  May or may not work correctly. Let's find out!
#
###############################################################################

#import libraries
import random
from PlayerBotOnly import Player
from HandSilent import Hand
from DumbAI import DumbAI
from DumbestAI import DumbestAI



# Define constants
DECK_SIZE = 52

#Define arrays for cards
CARDS = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
SUITS = [" of Clubs", " of Diamonds", " of Hearts", " of Spades"]

#Define arrays for deck
deck = [0] * 52
cutCard = -1

# make new players
player1 = Player( "RandomAI" )
player2 = Player( "DumbAI" )


# set opponents
player1.setOpp( player2 )
player2.setOpp( player1 )

# make refs for dealer and other player
dealer = player1
second = player2

#make a crib
crib = Hand()

#make a discard pile
discard = []

# make bots
dumb = DumbAI()
dumbest = DumbestAI()

#keep track of when the human is the dealer
humanDealer = True

#keep track of who threw the last card
lastPlayer = player1

# keep track of stats
totalTurn = 0
randomTurn = 0
deltap1 = 0
deltap2 = 0
sameTurn = 0
margin = []

#stuff for checking the score 
def checkScore( score, discard, player ):

    #make 5ddsure the pile is nonempty
    if len( discard ) == 0:

        # exit prematurely
        return 0
 

    #check if we are at 15
    if score == 15:

        # denote and move player 2
        player.move( 2 )

    elif score == 31:

        # denote and move player 2
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
            player.move( x + 1 )
            break

    
    #check for 4 of a kind
    top = discard[ depth ]

    if depth >= 3:
        #check for 4 of a kind
        if top == discard[depth-1] and top == discard[depth-2] and top == discard[depth-3]:

            # denote we have a 4 of a kind and move
            player.move( 12 )
            fourFound = True

    #check for a 3 of a kind
    if not fourFound:

        # make sure there are three cards in the pile
        if depth >= 2:

            if top == discard[depth-1] and top == discard[depth-2]:

                # denote we have a 3 of a kind and move
                player.move( 6 )
                threeFound = True            

        if depth >= 1 and not threeFound:

            # check for pair
            if top == discard[depth-1]:

                # denote we have a pair and move
                player.move( 2 )


# 
def peg( player, discard, points, isDumb ):

    # player moves if they can
    move = player.play( points, discard, dumb, dumbest, isDumb )

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

    #Store the number of the cut in card
    cutCard = deck[random.randint( 12, 51 )]

    #print the card that was cut
    
    #check if card is a jack
    if Hand.cardValue( cutCard )[0] == 10:
        dealer.move( 2 )

    return cutCard

# function for breaking out of loop
def reset():

    # denote end of game
    raise gameWon

#Populate deck with numbers 0 - 51 at each index
for x in range(1, 51):
    deck[x] = x

#play until someone wins
while( player1.wins + player2.wins) < 100:

    try:
        while( True ):
            # denote we have taken a turn
            totalTurn += 1

            # check when the ai plays this turn
            aiLast = humanDealer

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

            
            # determine the AI's throw and throw

            randThrow = dumbest.determineThrow( second.hand )

            if aiLast:
                aiThrow = dumb.determineThrow( second.hand )
                second.hand.throw( aiThrow[0], aiThrow[1], crib )
                dealer.hand.throw( randThrow[0], randThrow[1], crib )

            else: 
                aiThrow = dumb.determineThrow( dealer.hand )
                second.hand.throw( randThrow[0], randThrow[1], crib )
                dealer.hand.throw( aiThrow[0], aiThrow[1], crib )

            #update playable cards
            second.update()
            dealer.update()
            
            #print cards in new hands

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
                lastPlayer.move( 1 )



            second.move( second.hand.score(cutCard, False) )

            dealer.move( dealer.hand.score(cutCard, False) )

            dealer.move( crib.score(cutCard, True) )


            #clear all hands
            dealer.hand.clear()
            second.hand.clear()
            crib.clear()

            #swap second and dealer
            tmp = dealer
            dealer = second
            second = tmp

            #print game information
            humanDealer = not humanDealer

            #reset score and discard
            score = 0
            discard = []

            # if 2 turns have passed ( both players have had a crib )
            if( humanDealer ):
                deltap1 = player1.position - deltap1
                deltap2 = player2.position - deltap2

                # check if the random is ahead
                if deltap1 > deltap2:
                    randomTurn += 1

                elif deltap1 == deltap2:
                    sameTurn += 1
          
                margin.append( deltap2 - deltap1 )


    except ValueError:
        score = 0
        discard = []
        humanDealer = True
        crib = Hand()
        dealer = player1
        second = player2

        deltap1 = 0
        deltap2 = 0

#calculate statistics
winRate = player1.wins / (player1.wins + player2.wins) * 100.0
turnPairs = randomTurn / totalTurn * 100.0
print( "Statistics:" )

print(" \nGames" )
print( "DumbAI won: " + str( 100 - winRate ) + "% of the time" )
print( "(" + str( player2.wins ) + ")" )
print( "RandomAI won: " + str( winRate ) + "% of the time" )
print( "(" + str( player1.wins ) + ")" )

print("\nTurn Pairs" )
print( "DumbAI won: " + str( 100 - turnPairs - sameTurn/totalTurn*100.0 ) + "% of pairs of turns!" )
print( "(" + str( totalTurn - randomTurn ) + ")" )
print( "RandomAI won: " + str( turnPairs ) + "% of pairs of turns!" ) 
print( "(" + str( randomTurn ) + ")" )
print( "Tied: " + str( sameTurn / totalTurn * 100.0 ) + "% of the time!" )


print( "Average margin" )
print( sum( margin ) / len( margin ) )

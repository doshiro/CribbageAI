import random
import itertools
from Hand import Hand
from Player import Player


class DumbestAI:

    def __init__( self ):

        #hand to be stored by the AI
        self.hand = Hand()


    # throw the first two cards
    def determineThrow( self, hand ):

        a = random.randint( 0, 5 )
        b = a

        # more random
        while( b == a ):
            b = random.randint( 0, 5 )

        return [a, b]


    # function for playing in pegging
    def determinePeg( self, score, discard, playable ):

        # make variable to store played card
        played = -1

        # check if we can play any cards
        if len( playable ) == 0:

            print( "len(playable) = 0. Abort!")
            return -1

        # make boolean for keeping track of if we can play any cards
        canPlay = [False] * len( playable )
        playPossible = False

        # check if we have any playable cards
        for x in range( 0, len( playable ) ):

            #check if we have any playable face cards
            if playable[x] > 10:
                if score + 10 <= 31:
                        
                    # denote we can play a card
                    canPlay[x] = True
                    playPossible = True

            # check if we have any playable cards
            else:
                
                #check if we can play the card
                if score + playable[x] <= 31:

                    # denote we can play a card
                    canPlay[x] = True
                    playPossible = True

        # make sure we can play something
        if not playPossible:

            print( "No play possible! Abort!" )
            return -1

        # make array to choose from
        choose = []

        # detemine optimal throw
        for x in range( 0, len( playable ) ):

            # make sure this card is playable
            if canPlay[x]:
                choose.append( x )

        # return random playable card
        return choose[ random.randint( 0, len( choose ) - 1 ) ]

###############################################################################
#
# Player object for game of Cribbage
#
#
###############################################################################

#import libraries
import random
from HandSilent import Hand

# Player class has a hand of cards and a position
class Player:

    def __init__( self, name ):

        #keep track of player name
        self.name = name

        # keep track of where the player is
        self.position = 0

        # keep track of player's hand
        self.hand = Hand()

        # keep track of played cards
        self.playable = Hand()
        self.playableVals = []

        #keep track of if we can play
        self.ableToPeg = True
        self.playing = True

        # keep track of wins
        self.wins = 0

        # keep track of opponent and game
        self.opponent = None

    # set the opponent
    def setOpp( self, player ):

        self.opponent = player

    # method to move the player forward in position by a number of points
    def move( self, points ):

        #move the position forward by the number of points
        self.position += points

        #check if we have won
        if self.position > 120:

            self.wins += 1

            self.position = 0
            self.opponent.position = 0
    
            raise ValueError



    # function for updating the hand
    def update( self ):
    
        # add vals to playable and playableVals
        for x in range( 0, 4 ):

                # add the cards to the hands
                self.playableVals.append( self.hand.cardVals[x][0] + 1 )
                self.playable.addCard( self.hand.cardNums[x] )

        # denote we have a new hand and therefore can play
        self.ableToPlay = True
        self.playing = True


    def parse( self, card ):

        try:

            toThrow = int( card )
            return toThrow

        except:

            print( card + " is not a valid integer!" )
            return -1

    # function for playing in pegging
    def play( self, score, discard, ai, dumbest, isAi ):


        # make variable to store played card
        played = -1

        # check if we can play any cards
        if len( self.playableVals ) == 0:

            self.playing = False
            self.ableToPeg = False
            return -1

        # make boolean for keeping track of if we can play any cards
        canPlay = [False] * len( self.playableVals )
        playPossible = False

        # check if we have any playable cards
        for x in range( 0, len( self.playableVals ) ):

            #check if we have any playable face cards
            if self.playableVals[x] > 10:
                if score + 10 <= 31:
                        
                    # denote we can play a card
                    canPlay[x] = True
                    playPossible = True

            # check if we have any playable cards
            else:
                
                #check if we can play the card
                if score + self.playableVals[x] <= 31:

                    # denote we can play a card
                    canPlay[x] = True
                    playPossible = True

        # make sure we can play something
        if not playPossible:

            # denote we are skipping
            self.ableToPeg = False
            return 0


        while played == -1:


            # make a copy of the discard pile
            dCopy = list( discard )

            if isAi:
                toThrow = ai.determinePeg( score, dCopy, self.playableVals )

            else:
                toThrow = dumbest.determinePeg( score, dCopy, self.playableVals )

            if toThrow < 0: 

                print( "Something is wrong; your AI sucks!" )
                return -1


            # make sure card is in a valid index
            if( toThrow >= 0 and toThrow < len(self.playableVals) ):


                #make sure card is playable
                if( canPlay[toThrow] ):

                    #store the played value
                    played = self.playableVals[toThrow]

                    #add played value to discard
                    discard.append( played )

                    #remove the card from the playable and playableVals
                    del self.playableVals[ toThrow ]
                    self.playable.removeCard( toThrow )

                #if the card is not playable
                else:

                    #denote this card cannot be thrown
                    print( "Cannot play " + Hand.cardString( self.playable.cardNums[ toThrow ] ) + ". Try again." )

            else:

                #tell the user to try again
                print( "Please give a number between 0 and " + str( len( self.playableVals ) - 1 ) )

        
        return played

# TODO HEADER

#import libraries
import random
import itertools

#holds information for a hand object
class Hand:
    
    #Define arrays for cards
    CARDS = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
    SUITS = [" of Clubs", " of Diamonds", " of Hearts", " of Spades"]


    #method for getting the string representation of a card
    @staticmethod
    def cardString( num ):
        return( Hand.CARDS[ num % 13 ] + Hand.SUITS[ num // 13 ] )


    #method for getting the value of a card
    @staticmethod
    def cardValue( num ):
        return [ num % 13, num // 13 ]


    #default ctor makes an array of 6 things
    def __init__( self ):

        #make instance arrays for card holding
        self.cardNums = []
        self.cardVals = []

        #make instance variables for holding cards thrown
        cardThrown = -1


    #adds a card to a hand
    def addCard( self, card ):

        #add card to both cardNums and cardVals
        self.cardNums.append( card )
        self.cardVals.append( self.cardValue( card ) )


    def removeCard(self, card ):
    
        #remove card from both card arrays
        del self.cardNums[ card ]
        del self.cardVals[ card ]

    #sets the card at a given index
    def setCard(self, card, index ):

        #set the card num at the given index
        self.cardNums[index] = card

        #set the card value as well
        self.cardValues[index] = cardValue( card )


    #method to show cards
    def showCards( self, num ):

        return 0

    #method to throw cards
    def throw(self, card1, card2, crib ):

        #add thrown cards to crib
        crib.addCard( self.cardNums[card1] )
        crib.addCard( self.cardNums[card2] )

        #remove the thrown cards from the hand
        if card1 > card2:
            self.removeCard( card1 )
            self.removeCard( card2 )

        else:
            self.removeCard( card2 )
            self.removeCard( card1 )


    #clear the current hand
    def clear( self ):

        # make the arrays emptied or cleared
        self.cardNums = []
        self.cardVals = []

    #scores a hand
    def score(self, cut, checkCrib):

        # show the hand
        self.showCards( 4 )

        #create variable for keeping track of points
        points = 0

        #add in cut
        self.addCard( cut )

        #check for pairs
        for i in range( 0, 4 ):
            for j in range( i + 1, 5 ):

                #add two points to score and shout if pair found
                if( self.cardVals[i][0] == self.cardVals[j][0] ):
                    points += 2

        #check for 4 card flush
        if not checkCrib:

            #store suit of first card
            suit = self.cardVals[0][1]

            #check for all other cards to be in same suit
            if ( self.cardVals[1][1] == suit and self.cardVals[2][1] == suit and self.cardVals[3][1] == suit ):
                points += 4

                #check for 5 card flush
                if( self.cardVals[4][1] == suit ):
                    points += 1

        #if we are checking the crib
        else:

            #check all cards and the cut by default
            suit = self.cardVals[0][1]
            if( self.cardVals[1][1] == suit and self.cardVals[2][1] == suit and self.cardVals[3][1] == suit and self.cardVals[4][1] == suit ):
                points += 5

        # sort the ranges
        lst = []

        for x in range( 0, 5 ):
            lst.append( self.cardVals[x][0] )

        lst.sort()
        
        # make list of all combinations of 3 and 4
        runFour = [list(x) for x in itertools.combinations(lst, 4)]
        runThree = [list(x) for x in itertools.combinations(lst, 3)]

        #create boolean for finding run of 4
        runFound = False

        #check for run of 5
        if lst[0] + 1 == lst[1] and lst[0] + 2 == lst[2] and lst[0] + 3 == lst[3] and lst[0] + 4 == lst[4]:

            # denote we found a run of 5
            points += 5

        else:

            #check for runs of 4
            for x in range( 0, 5 ):

                # check for a run of 4
                if runFour[x][1] == runFour[x][0] + 1 and runFour[x][2] == runFour[x][0] + 2 and runFour[x][3] == runFour[x][0] + 3:

                    #denote we found a run of 4
                    points += 4

                    runFound = True


            #check for runs of 3
            if not runFound:

                #check for runs of 3
                for x in range( 0, 10 ):

                    if runThree[x][1] == runThree[x][0] + 1 and runThree[x][2] == runThree[x][0] + 2:

                        # denote we found a run of 3
                        points += 3


        #check for correct jack
        suit = cut // 13
        
        for x in range( 0, 4 ):
            if self.cardVals[x][0] == 10 and self.cardVals[x][1] == suit:
                points += 1

        #check for 15s

        #cast to 10s and add sum
        total = 0
        for x in range(0, 5):
            if self.cardVals[x][0] > 9:
                self.cardVals[x][0] = 9

            total += self.cardVals[x][0]

        #check if all cards together are 15
        if total == 14:
            points += 2

        lst = []

        #check for all other combinations
        for x in range(0, 5):
            lst.append( self.cardVals[x][0] + 1 )
        
        #make combs array to hold all combinations of elements
        for i in range(2, 5):
            els = [list(x) for x in itertools.combinations(lst, i)]

            for x in range( 0, len(els) ):
                if sum( els[x] ) == 15:
                    points += 2


        #denote how much was earned
        return points

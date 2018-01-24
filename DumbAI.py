import random
import itertools
from Hand import Hand
from Player import Player


class DumbAI:

    def __init__( self ):

        #hand to be stored by the AI
        self.hand = Hand()
        self.GUESSCUT = 9



    def evaluateProb( self, hand ):

        # make a deck
        deck = []
        for x in range( 1, 52 ):

            # assume card is not in your hand
            inHand = False

            for y in range( 0, 4 ):
                if x == hand.cardNums[y]:
                    #make note this card is already in your hand
                    inHand = True

            if not inHand:
                # populate deck
                deck.append( x )

    
        # created sorted hand
        lst = list( hand.cardNums )
        lst.sort()

        # initialize a best hand
        score = 0.0

        # evaluate each of throws and pick the best one
        for x in range( 0, len( deck ) ):

            #evaluate with the cut card
            score += self.evaluate( hand, deck[x] )

        # return total score
        return score




    def evaluate( self, newHand, cut ):

        # make a copy of the hand with the cut
        hand = Hand()
        for x in range( 0, 4 ):
            hand.addCard( newHand.cardNums[x] )
        hand.addCard( cut )

        #create variable for keeping track of points
        points = 0.0

        #check for pairs
        for i in range( 0, 4 ):
            for j in range( i + 1, 5 ):

                #add two points to score and shout if pair found
                if( hand.cardVals[i][0] == hand.cardVals[j][0] ):
                    points += 2


        #store suit of first card
        suit = hand.cardVals[0][1]

        #check for all other cards to be in same suit
        if ( hand.cardVals[1][1] == suit and hand.cardVals[2][1] == suit and hand.cardVals[3][1] == suit ):
            points += 4

            # check the cut
            if( hand.cardVals[4][1] == suit ):
                points += 1

        # sort the ranges
        lst = []
        for x in range( 0, 5 ):
            lst.append( hand.cardVals[x][0] )
        lst.sort()
        
        # make list of all combinations of 3
        runFour = [list(x) for x in itertools.combinations( lst, 4 )]
        runThree = [list(x) for x in itertools.combinations(lst, 3)]

        # keep track of if we have found a run
        runFound = False
        runFive = False

        # check for a run of 5
        first = lst[0]
        if first == lst[1] - 1 and first == lst[2]-2 and first == lst[3]-3 and first == lst[4]-4:

            # denote we found a run
            runFive = True
            points += 5

        if not runFive:
            # check for a run of 4
            for x in range( 0, len(runFour) ):

                # sort the list
                runFour[x].sort()

                if runFour[x][1] == runFour[x][0] + 1 and runFour[x][2] == runFour[x][0] + 2 and runFour[x][3] == runFour[x][0] + 3:
                    #denote we found a run of 4
                    points += 4
                    runFound = True

        #check for runs of 3
        if not runFound:

            #check for runs of 3
            for x in range( 0, len( runThree ) ):

                if runThree[x][1] == runThree[x][0] + 1 and runThree[x][2] == runThree[x][0] + 2:
                    # denote we found a run of 3
                    points += 3


        # give preference to jacks
        for x in range( 0, 4 ):
            if lst[x] == 10:
                points += 0.25


        # make the correct 15 nums
        for x in range( 0, len( lst ) ):
            if lst[x] >= 9:
                lst[x] = 10
            else:
                lst[x] += 1


        #check for 15s
        for x in range( 1, 5 ):

            #make an array of combinations
            test = [list(y) for y in itertools.combinations( lst, x )]

            # check if the cards give a 15
            for cards in test:

                # add points if we have a 15
                if sum(cards) == 15:
                    points += 2

            return points


    # find out what to throw by scoring all possible throws
    def determineThrow( self, hand ):

        #make variables to throw
        a = -1
        b = -1

        #make new hands with combinations of 4 cards
        fourCardHands = [list(x) for x in itertools.combinations( hand.cardNums, 4 )]


        # populate the hand with the first combination
        for x in range( 0, 4 ):
            self.hand.addCard( fourCardHands[0][x] )
 

        # make a score to beat
        scoreToBeat = self.evaluateProb( self.hand )
        

        # create a hand from the array
        for x in range( 1, len( fourCardHands ) ):
            
            # make a hand pointer
            testHand = Hand()
            testHand.clear()

            for y in range( 0, 4 ):

                # make new hand 
                testHand.addCard( fourCardHands[x][y] )


            score = self.evaluateProb( testHand )

            # check the score of the test hand
            if score > scoreToBeat:

                # update the hand pointer
                self.hand = testHand
                score = scoreToBeat

        # find the indices we threw
        for x in range ( 0, 6 ):

            # assume we threw this card
            thrown = True

            # check if we didn't throw it
            for y in range( 0, 4 ):

                # compare the original hand's value at that index to our new hand
                if hand.cardNums[x] == self.hand.cardNums[y]:

                    # denote the number is in the array
                    thrown = False

            # if we threw it
            if thrown:

                # denote what this index is
                # make sure we reassigned a already
                if a == -1:
                    a = x

                # reassign b
                else:
                    b = x

        return [a, b]


    #stuff for checking the score 
    def scorePeg( self, card, score, discardReal ):

        # keep track of points earned for this throw
        points = 0

        score += card

        # copy the passed in array
        discard = list( discardReal )

        # add the proposed throw to the array
        discard.append( card )

        #make 5ddsure the pile is nonempty
        if len( discard ) == 0:

            # exit prematurely
            return 0
     

        #check if we are at 15
        if score == 15:

            # denote and move player 2
            points += 2

        elif score == 31:

            # denote and move player 2
            points += 2
        
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

                # keep track of the points found for a run
                if run:

                    points += x + 1
                    break

        
        #check for 4 of a kind
        top = discard[ depth ]

        if depth >= 3:
            #check for 4 of a kind
            if top == discard[depth-1] and top == discard[depth-2] and top == discard[depth-3]:

                # denote we have a 4 of a kind and move
                points += 12
                fourFound = True

        #check for a 3 of a kind
        if not fourFound:

            # make sure there are three cards in the pile
            if depth >= 2:

                if top == discard[depth-1] and top == discard[depth-2]:

                    # denote we have a 3 of a kind and move
                    points += 6
                    threeFound = True         

            if depth >= 1 and not threeFound:

                # check for pair
                if top == discard[depth-1]:

                    points += 2
        
        return points


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


        # initialize scoreToBeat
        scoreToBeat = 0

        # initialize toThrow variable
        for x in range( 0, len( playable ) ):

            # make sure we can throw this card
            if canPlay[x]:

                # make this the card to throw and exit
                toThrow = x
                break

        # detemine optimal throw
        for x in range( toThrow, len( playable ) ):

            # make sure this card is playable
            if canPlay[x]:

                # determine how many points throwing this card gives us
                score = self.scorePeg( playable[x], score, discard )

                #determine if this card is better scorewise
                if score > scoreToBeat:

                    # make this the new card to throw and update score to beat
                    toThrow = x
                    scoreToBeat = score

                # determine if this card is better because it's a higher number
                elif score == scoreToBeat and playable[x] > playable[toThrow]:

                    #make this the new card
                    toThrow = x


        #if the card is not playable
        if not canPlay[ toThrow ]:

            #denote this card cannot be thrown
            print( "Cannot throw " + Hand.cardString( self.playable.cardNums[ toThrow ] ) + ". Try again." )
            return -1


        # otherwise return the optimal index thrown
        else:

            #print( "Throwing " + str( playable[toThrow] ) )
            return toThrow

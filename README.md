# CribbageAI
A basic, python-based cribbage text game and AI

# Inspiration and General Information
This was a project I started to teach myself Python.

If you need the rules of cribbage, look here: 
http://www.bicyclecards.com/how-to-play/cribbage/

To play against the bot, use the "Cribbagev1.py" file.

The CribbageAI I have developed uses algorithms to determine what card to throw. For example, once dealt 6 cards, it will calculate the points for all combinations of 4 cards weighted against all possible cuts and throw whatever keeps it the most points in its hand. While pegging, it will throw cards that are obviously pairs, runs (in any order), 15s or 31s.

# Testing
The CribbageAI bot has been tested against a bot that throws and pegs 100% randomly, and my AI wins around 75% of the time! Against a human player, namely my brother, my mom, and myself who tested this thing, it wins only 30-40% of the time, but that is to be expected! More on this in the discussion section.

# Discussion of Error
While the human trials are less than promising, the 30-40% figure comes from the fact that the bot does not have a very good understanding of dynamics of throwing or late-game play.

In throwing, one does not always throw for the optimal number of points in their hand. Often, if your opponent has the crib, you shouldn't throw them a pair or a 15, even if doesn't fit in with the rest of your hand. The bot often throws free points to their opponent in the crib. Further, the bot does not throw itself good cards when it has the crib. Also, when throwing for a hand that has 0-2 points, it fails to consider what cards would be good to keep for pegging.

Speaking of pegging, in late-game, the game revolves more around pegging than around keeping cards in your hand, as often you don't get to count your hand / crib if one player pegs out. The bot fails to take this into account, and it will always throw to keep the most points in its hard, even if its goal should be to peg out. 

# Further Work
The original intent for this project was to learn machine learning through Python. However, after finishing the algorithmic AI and researching Q-learning, I realized that the decision-space for this game is massive, and that the project I had begun was a bit too ambitious. I plan to do a smaller machine learning project and build my way up to a more effective cribbage bot using machine learning.

At this point, I may try to write a UI for this and publish my first mobile phone app. We'll see what's to come!

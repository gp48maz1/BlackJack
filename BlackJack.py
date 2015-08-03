from Player import Player
from Deck import Deck
import copy

class BlackJack:
	
	def __init__(self, deckNumbers=6): 	# TODO constructors with list of players and deck as parameter
		self.deck = Deck(deckNumbers)
		self.players = [Player("Player 1", 200), Player("Player 2", 200)]
	
	def setDeck(self, newDeck):
		self.deck = newDeck
	
	def sumCards(self, listCards, ace1=False, ace11=False):
		""" returns sum of the cards, counted following the blackjack rules """
		returnSum = 0
		
		for i in range(len(listCards)):
			cardNumber = self.deck.cardNumber(listCards[i])
			if(cardNumber >= 1 and cardNumber <= 9):
				returnSum += cardNumber+1
			elif(cardNumber >= 10 and cardNumber <= 12):
				returnSum += 10
			elif(cardNumber == 0): # Ace counting
				if(ace1):
					returnSum += 1
				elif(ace11):
					returnSum += 11
				else:
					if(BlackJack.isBetterSum(self, BlackJack.sumCards(self, listCards, True, False), BlackJack.sumCards(self, listCards, False, True))):
						returnSum +=1
					else:
						returnSum += 11
			else:
				print "Unknown card"
				return 0
		
		return returnSum
		
	def isBetterSum(self, s1, s2):
		""" Returns true if s1 beats or ties s2, false if s2 strictly beats s1 """
		if(s2 > 21):
			return True
		else:
			if(s1 > 21):
				return False
			else:
				if(s2 > s1):
					return False
				else:
					return True
		
		return True
		
	def displayPlayerCards(self, playerCards, n=-1):
		returnString = ""
		if(n >= len(self.players) or n < 0):
			for i in range(len(self.players)):
				returnString += self.players[i].getName() + " Cards (Total points {}) :".format(BlackJack.sumCards(self, playerCards[i]))
				returnString += "\n" + self.deck.displayCard(playerCards[i])
		else:
			returnString += self.players[n].getName() + " Cards (Total points {}) :\n".format(BlackJack.sumCards(self, playerCards[n]))
			returnString += self.deck.displayCard(playerCards[n])
			
		return returnString
		
	def displayDealerCards(self, dealerCards, show=False):
		returnString = ""
		returnString += "\nDealer Cards :"
		returnString += "\n" + self.deck.displayCard(dealerCards[0])
		if(show):
			for i in range(1,len(dealerCards)):
				returnString += "\n" + self.deck.displayCard(dealerCards[i])
			returnString += "\n------ Total points : {} \n".format(BlackJack.sumCards(self, dealerCards))
		else:
			returnString += "\n********** \n"
			
		return returnString
		
	def cardsNeeded(self):
		""" Number of cards needed for one round """
		return 3*(len(self.players)+1)
	
	def enoughCardsLeft(self):
		""" True if there are more than cardsNeeded(self) cards left in deck """
		if(len(self.deck.deck) >= BlackJack.cardsNeeded(self)):
			return True
		else:
			return False
		
	def hasBlackJack(self, listCards):
		if(len(listCards) == 2 and BlackJack.sumCards(self, listCards) == 21):
			return True
		else:
			return False
		return False

	def doubleIsValid(self, playerCards):
		""" Returns True if double is valid, false if it is not """
		# TODO : modify to comply to different casino rules

		if(len(playerCards) == 2):
			return True
		else:
			return False
			
	def splitIsValid(self, playerCards):
		
		if (len(playerCards) == 2 ):
			if(self.deck.cardNumber(playerCards[0]) == self.deck.cardNumber(playerCards[1])):
				return True
		
		return False
 
	def results(self, dealerCards, playerCards, bets):
		print "########## Round results ############"
		dealerBlackJack = BlackJack.hasBlackJack(self, dealerCards)
		dealerPoints = BlackJack.sumCards(self, dealerCards)
		playersPoints = []
		# Players points and players blackjacks
		for i in range(len(self.players)):
			playersPoints.append(BlackJack.sumCards(self, playerCards[i]))
		playersBlackJack = []
		for i in range(len(self.players)):
			playersBlackJack.append(BlackJack.hasBlackJack(self, playerCards[i]))
		
		## addMoney and print results
		print "Dealer, total points : {}".format(dealerPoints)
		if(dealerBlackJack):
			print "Black Jack !"
			
		for i in range(len(self.players)):
			print self.players[i].getName() + " , total points : {}".format(playersPoints[i])
			if(playersBlackJack[i]):
				print "Black Jack !"
				
			# Who wins + money earned
			win = 0
			if(playersPoints[i] > 21):
				print "Busted."
				win = -bets[i]
			else:
				if(dealerPoints > 21):
					print "Dealer is busted."
					win = bets[i]
					if(playersBlackJack[i]):
						print "Black Jack pays 3:2"
						win = 1.5*bets[i]
				else:
					if(playersPoints[i] > dealerPoints):
						print "Dealer pays."
						if(not playersBlackJack[i]):
							win = bets[i]
						else:
							print "Black Jack pays 3:2"
							win = 1.5*bets[i]
					elif(playersPoints[i] < dealerPoints):
						print "Dealer wins."
						win = -bets[i]
					else:
						if(not playersBlackJack[i] and not dealerBlackJack):
							print "Tie."
							win = 0
						else:
							if(dealerBlackJack and playersBlackJack[i]):
								print "Tie."
								win = 0
								# TODO : in this case, dealers pays player's BlackJack ?
							elif(dealerBlackJack and not playersBlackJack[i]):
								print "Dealer has Black Jack. Dealer wins."
								win = -bets[i]
							elif(playersBlackJack[i] and not dealerBlackJack):
								print "Player has Black Jack. Dealer pays 3:2."
								win = 1.5*bets[i]
							else:
								print "Tie."
								win = 0
			
			if (win >= 0):
				print "Wins : {}".format(win)
			else:
				print "Loses : {}".format(-win)
				
			self.players[i].addMoney(win)

	####### Play BlackJack ! ######
	def playBlackjack(self):
		
		defaultBet = 10
		
		""" Main function for the black jack game with inputs from human players """
		
		keepPlaying = True
		while (keepPlaying):
			print "--- New Round ----"
			
			playersSplit = [False]*len(self.players)
			
			### Display Players (and eject those who haven't enough money left) :
			playersToEject = []
			for i in range(len(self.players)):
				if(self.players[i].getMoney() > 0):
					print self.players[i]
				else:
					print self.players[i].getName() + " has no money left."
					print self.players[i].getName() + " is out of the game !"
					playersToEject.append(i)
			
			if(len(playersToEject) > 0):
				for i in range(len(playersToEject)):
					self.players.pop(playersToEject[i])
					
			if(len(self.players) < 1):
				print "No more players."
				return 0
			### Ask for bets
			bets = []
			for i in range(len(self.players)):
				keepAsking = True
				while (keepAsking):
					inputBet = raw_input(self.players[i].getName() + ", what is your bet (10) ? ")
					
					## Default bet
					if inputBet == "":
						inputBet = defaultBet
					
					try:
						currentBet = int(inputBet)
						if (currentBet <= self.players[i].getMoney()):
							keepAsking = False
							bets.append(currentBet)
						else:
							print "You dont have enough money to place this bet !"
					except ValueError:
					   print "Not a valid bet !"
			
			### Give cards to players + to dealer
			dealerCards = self.deck.drawCard(2)
			print BlackJack.displayDealerCards(self, dealerCards)
			
			playerCards = []
			for i in range(len(self.players)):
				cards = self.deck.drawCard(2)
				playerCards.append(cards)
				
			print BlackJack.displayPlayerCards(self, playerCards)
			
			### Ask for players' actions
			i = 0
			cont = True
			playersBackup = self.players
			#~ for i in range(len(self.players)):
			while cont:
				
				keepAsking = True
				while (keepAsking):
					if (BlackJack.sumCards(self, playerCards[i]) >= 21):
							print "You cannot ask for a card anymore" # TODO : better text here
							keepAsking = False
					else:
						# TODO : add split possibility
						
						splitString = ""
						
						print BlackJack.displayPlayerCards(self, playerCards, i)
						
						## TODO : cannot split if already split
						if(self.splitIsValid(playerCards[i])):
							splitString = "to split (P),"
						
						## TODO : cannot double if split
						if(BlackJack.doubleIsValid(self, playerCards[i])):
							stringInput = ", do you want "+splitString+" to hit (H), to stay (S) or to double (D) ? "
						else:
							stringInput = ", do you want "+splitString+" to hit (H) or to stay (S) ? "

						playerAction = raw_input(self.players[i].getName() + stringInput)
						
						if(playerAction == "H"):
							if (BlackJack.sumCards(self, playerCards[i]) >= 21):
								print "You cannot ask for a card anymore" # TODO : better text here
								keepAsking = False
							else:
								playerCards[i].append(self.deck.drawCard())
								print BlackJack.displayPlayerCards(self, playerCards, i)
						elif(playerAction == "D"):
							if(BlackJack.doubleIsValid(self, playerCards[i])):
								print "Your bet has been doubled."
								bets[i] = 2*bets[i]
								playerCards[i].append(self.deck.drawCard())
								print BlackJack.displayPlayerCards(self, playerCards, i)
								print "You've chose to Double, you cannot ask for a card anymore"
								keepAsking = False
							else:
								print "You can't double in this situation."
						elif(playerAction == "S"):
							keepAsking = False
						elif(playerAction == "P"):
							## TODO : cannot split if already split
							if(self.splitIsValid(playerCards[i])):
								
								playersSplit[i] = True
								
								## Backups
								playersBackup = copy.deepcopy(self.players)
								
								self.players.insert(i+1,copy.copy(self.players[i]))
								self.players[i].name = self.players[i].name + " - hand #1"
								self.players[i+1].name = self.players[i+1].name + " - hand #2"
								
								splittedCard = playerCards[i][1]
								playerCards[i] = [playerCards[i][0], self.deck.drawCard()]
								
								playerCards.insert(i+1, [splittedCard, self.deck.drawCard()])
								
								bets.insert(i+1, bets[i])
								
								#~ print self.players
								#~ print playerCards
								#~ print bets
								#~ print BlackJack.displayPlayerCards(self, playerCards, i)
								
								pass
							else:
								"Cannot split here."
						else:
							print "Not a valid choice."
							
				i = i+1
				
				if (i >= len(self.players)):
					cont = False
					
			### Make dealer draw or stay
			keepDrawing = True
			while (keepDrawing):
				print BlackJack.displayDealerCards(self, dealerCards, True) # Show Dealer cards
				if(BlackJack.sumCards(self, dealerCards) <= 16):
					print "Dealer draws"
					dealerCards.append(self.deck.drawCard())
				else:
					print "Dealer stands"
					keepDrawing = False
			
			### Display win or lose and addMoney
			BlackJack.results(self, dealerCards, playerCards, bets)
			
			## TODO : correct amount of money for players who splitted
			#~ print playersSplit
			k = 0
			for i in range(len(playersBackup)):
				if playersSplit[i]:
					moneyWithSplitResult = self.players[k].money + self.players[k+1].money - playersBackup[i].money
					#~ print "with split result : ", moneyWithSplitResult
					playersBackup[i].money = moneyWithSplitResult
					k = k+1
				else:
					playersBackup[i].money = self.players[k].money
					
				k = k+1

			
			self.players = playersBackup
			
			### If there are enough cards left in deck, continue, else stop
			if(not BlackJack.enoughCardsLeft(self)):
				print "No more cards left in deck. Cards will be shuffled."
				keepPlaying = False
				BlackJack.setDeck(self, Deck())
				BlackJack.playBlackjack(self)
#Hearthstone Battlegrounds Simulator#
import random
class Card:
    def __init__(self, name: str, attack: int, health: int, divine: bool, taunt: bool, poison: bool, windfury: int):
        self.name = name
        self.attack = attack
        self.health = health
        self.divine = divine
        self.taunt = taunt
        self.poison = poison
        self.windfury = windfury
        
    def battle(self, othercard):
        if self.divine == False and othercard.divine == False:
            if self.poison == True and self.attack > 0:
                othercard.health = 0
            else:
                othercard.health = othercard.health - self.attack
            if othercard.poison == True and othercard.attack > 0:
                self.health = 0
            else:
                self.health = self.health - othercard.attack
        elif self.divine == True and othercard.divine == True:
            if self.attack > 0:
                othercard.divine = False
            if othercard.attack > 0:
                self.divine = False
        elif self.divine == True:
            if self.poison == True and self.attack > 0:
                othercard.health = 0
            else:
                othercard.health = othercard.health - self.attack
            if othercard.attack > 0:
                self.divine = False
        elif othercard.divine == True:
            if othercard.poison == True and othercard.attack > 0:
                self.health = 0
            else:
                self.health = self.health - othercard.attack
            if self.attack > 0:
                othercard.divine = False
        
    def __str__(self):
        return str(self.name) + " " + str(self.attack) + " " + str(self.health)

class Board:
    def __init__(self):
        self.cardlist = []
        self.index = -1
        self.tauntlist = []
        
    def addCard(self, card: Card):
        self.cardlist.append(card)
        if card.taunt == True:
            self.tauntlist.append(card)
        
    def updateStatus(self):
        self.removeDead()

    def removeDead(self):
        i = 0
        while i < len(self.cardlist):
            if self.cardlist[i].health <= 0:
                if self.cardlist[i].taunt == True:
                    self.tauntlist.remove(self.cardlist[i])
                if i <= self.index:
                    self.index = self.index - 1
                del self.cardlist[i]
                i = i - 1
            i = i + 1
            
    def printBothBoardState(self, board2):
        print("your board:")
        self.printBoardState()
        print("opponents board:")
        board2.printBoardState()
        print()

    def printAttack(self, board2, i, j, tauntcheck):
        if tauntcheck == False:
            print(str(self.cardlist[i]) + " attacks " + str(board2.cardlist[j]))
        else:
            print(str(self.cardlist[i]) + " attacks " + str(board2.tauntlist[j]))
        print()
    
    def battle(self, otherBoard):   
        while len(self.cardlist) > 0 and len(otherBoard.cardlist) > 0:
            self.printBothBoardState(otherBoard)
            self.index = (self.index + 1) % len(self.cardlist)
            self.cardattack(self.index,otherBoard)
            self.updateStatus()
            otherBoard.updateStatus()
            self.printBothBoardState(otherBoard)
            if len(self.cardlist) == 0 or len(otherBoard.cardlist) == 0:
                break
            otherBoard.index = (otherBoard.index + 1) % len(otherBoard.cardlist)
            otherBoard.cardattack(otherBoard.index,self)
            self.updateStatus()
            otherBoard.updateStatus()
            if len(self.cardlist) == 0 or len(otherBoard.cardlist) == 0:
                break
        self.printBothBoardState(otherBoard)
        return self.endGame(otherBoard)

    def cardattack(self,i,otherBoard):
        card = self.cardlist[i]
        wi = 0
        while card in self.cardlist and wi <= self.cardlist[i].windfury:
            if len(otherBoard.tauntlist) == 0:
                j = random.randint(0, len(otherBoard.cardlist) - 1)
                #to print indeces of cards attacking each other:
                print(i, j)
                self.printAttack(otherBoard, i, j, False)
                self.cardlist[i].battle(otherBoard.cardlist[j])
                self.updateStatus()
                otherBoard.updateStatus()
            else:
                j = random.randint(0, len(otherBoard.tauntlist) - 1)
                #to print indeces of cards attacking each other:
                print(i, j)
                self.printAttack(otherBoard, i, j, True)
                self.cardlist[i].battle(otherBoard.tauntlist[j])
                self.updateStatus()
                otherBoard.updateStatus()
            wi = wi + 1
            

    def endGame(self, otherBoard):
        if len(self.cardlist) == 0 and len(otherBoard.cardlist) == 0:
            return "draw"
        elif len(self.cardlist) == 0:
            return "loss"
        elif len(otherBoard.cardlist) == 0:
            return "win"
        else:
            raise ValueError("Game shouldn't end yet")
    
    def printBoardState(self):
        for i in range(len(self.cardlist)):
            print(self.cardlist[i])
            if self.cardlist[i].divine == True:
                print("divine")

    

card1 = Card("a",1,1, True, False, False, 0)
card2 = Card("b",1,1, True, True, False, 0)
card3 = Card("c",4,4, True, False, False, 0)
card4 = Card("d",3,3, True, False, False, 0)
card5 = Card("e",5,5, True, False, False, 0)
card6 = Card("f",1,1, True, True, False, 0)
card7 = Card("g",9,9, True, False, False, 0)
card8 = Card("h",10,10, True, True, False, 4)
board1 = Board()
board1.addCard(card8)
board1.addCard(card1)
board1.addCard(card3)
board1.addCard(card2)
board2 = Board()
board2.addCard(card6)
board2.addCard(card4)
board2.addCard(card7)
board1.battle(board2)


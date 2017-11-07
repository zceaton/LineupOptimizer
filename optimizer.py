import xlrd

class Player:
    def __init__(self, name, positions, price, projection):
        self.name = name
        self.price = price
        if(projection == ''):
            self.projection = 0.0
        else:
            self.projection = projection
     
        self.positions = ["UTIL"]
        _positions = positions.split('/')
        if "PG" in _positions:
            self.positions.append("PG")
            self.positions.append("G")
        if "SG" in _positions:
            self.positions.append("SG")
            if "G" not in self.positions:
                self.positions.append("G")
        if "SF" in _positions:
            self.positions.append("SF")
            self.positions.append("F")
        if "PF" in _positions:
            self.positions.append("PF")
            if "F" not in self.positions:
                self.positions.append("F")
        if "C" in _positions:
            self.positions.append("C")

    def __str__(self):
        returnString = "{" + self.name + ": " + str(self.positions) + " | " + str(self.price) + " | " + str(self.projection) + "}"
        return returnString

    def __repr__(self):
        returnString = "{ " + self.name + ": " + str(self.positions) + " | " + str(self.price) + " | " + str(self.projection) + "}"
        return returnString

if __name__ == "__main__":
    workbook = xlrd.open_workbook('Josh Engleman\'s NBA DFS Projections.xlsx')
    worksheet = workbook.sheet_by_name('Projections')
    players = []
    highLineup = {"PG": "", "SG": "", "SF": "", "PF": "", "C": "", "G": "", "F": "", "UTIL": ""}

    for x in range(1,332):
        name = worksheet.cell(x,0).value
        projection = worksheet.cell(x,7).value
        positions = worksheet.cell(x,8).value
        price = worksheet.cell(x,9).value
        players.append(Player(name, positions, price, projection))

    highestProjection = 0
    tempPlayers = []

    for x in range(0,331):
        if players[x].projection != 0.0:
            tempPlayers.append(players[x])

    players = tempPlayers

    for PG in players:
        print(PG)
        for SG in players:
            if("PG" not in PG.positions or SG is PG):
                break
            for SF in players:
                if("SG" not in SG.positions or SF is PG or SF is SG):
                    break
                for PF in players:
                    pfPrice = PG.price + SG.price + SF.price + PF.price
                    if("SF" not in SF.positions or PF is PG or PF is SG or PF is SF or pfPrice > 50000):
                        break
                    for C in players:
                        cPrice = PG.price + SG.price + SF.price + PF.price + C.price
                        if("PF" not in PF.positions or C is PG or C is SG or C is SF or C is PF or cPrice > 50000):
                            break
                        for G in players:
                            gPrice = PG.price + SG.price + SF.price + PF.price + C.price + G.price
                            if("C" not in C.positions or G is PG or G is SG or G is SF or G is PF or G is C or gPrice > 50000):
                                break
                            for F in players:
                                fPrice = PG.price + SG.price + SF.price + PF.price + C.price + G.price + F.price
                                if("G" not in G.positions or F is PG or F is SG or F is SF or F is PF or F is C or F is G or fPrice > 50000):
                                    break
                                for UTIL in players:
                                    price = PG.price + SG.price + SF.price + PF.price + C.price + G.price + F.price + UTIL.price
                                    if("F" not in F.positions or UTIL is PG or UTIL is SG or UTIL is SF or UTIL is PF or UTIL is C or UTIL is G or UTIL is F or price > 50000):
                                        break

                                    proj = PG.projection + SG.projection + SF.projection + PF.projection + C.projection + G.projection + F.projection + UTIL.projection
                                    newLineup = {"PG": PG.name, "SG": SG.name, "SF": SF.name, "PF": PF.name, "C": C.name, "G": G.name, "F": F.name, "UTIL": UTIL.name}
                                    #print(newLineup)
                                    if(proj > highestProjection):
                                        highestProjection = proj
                                        highLineup = newLineup

    print(highLineup)
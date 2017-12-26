import xlrd, xlwt, csv, distance

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

    def __lt__(self, other):
        return self.projection / self.price > other.projection / other.price

    def __repr__(self):
        returnString = "{ " + self.name + ": " + str(self.positions) + " | " + str(self.price) + " | " + str(self.projection) + "}"
        return returnString

def getIDs(name, players, ids):
    best = 100000
    bestIndex = -1
    for player in players:
        if distance.levenshtein(name, player) < best:
            best = distance.levenshtein(name, player)
            bestIndex = players.index(player)

    if best > 5:
        print(name)
        print(ids[bestIndex])

    return ids[bestIndex]


if __name__ == "__main__":
    workbook = xlrd.open_workbook('DraftKings.xlsx')
    worksheet = workbook.sheet_by_name('Sheet1')
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Sheet1', True)
    players = []
    allProjections = []
    xlLineups = []
    highLineup = {"PG": "", "SG": "", "SF": "", "PF": "", "C": "", "G": "", "F": "", "UTIL": ""}
    xlPlayers = []
    xlPlayersID = []

    for x in range(1,101):
        name = worksheet.cell(x,1).value
        projection = worksheet.cell(x,9).value
        positions = worksheet.cell(x,0).value
        price = worksheet.cell(x,2).value
        if(price != ''):
            players.append(Player(name, positions, price, projection))

    x = 0
    with open('DKSalaries.csv', 'rt') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            if(x >= 8):
                xlPlayersID.append(row[10])
                xlPlayers.append(row[11])
            else:
                x += 1

    highestProjection = 0
    tempPlayers = []

    for x in range(0,len(players)):
        if players[x].price / 1000 * 5.3 < players[x].projection or (players[x].price >= 9000 and players[x].projection != 0.0):
            tempPlayers.append(players[x])

    players = tempPlayers
    print("Original players: ", len(players))

    PGs = []
    SGs = []
    SFs = []
    PFs = []
    Cs = []
    Gs = []
    Fs = []

    for player in players:
        if 'PG' in player.positions:
            PGs.append(player)
        if 'SG' in player.positions:
            SGs.append(player)
        if 'SF' in player.positions:
            SFs.append(player)   
        if 'PF' in player.positions:
            PFs.append(player)
        if 'C' in player.positions:
            Cs.append(player)
        if 'G' in player.positions:
            Gs.append(player)
        if 'F' in player.positions:
            Fs.append(player)

    for PG1 in PGs:
        for PG2 in PGs:
            if PG1.price > PG2.price and PG1.projection < PG2.projection:
                PGs.remove(PG1)
                break

    for SG1 in SGs:
        for SG2 in SGs:
            if SG1.price > SG2.price and SG1.projection < SG2.projection:
                SGs.remove(SG1)
                break

    for SF1 in SFs:
        for SF2 in SFs:
            if SF1.price > SF2.price and SF1.projection < SF2.projection:
                SFs.remove(SF1)
                break

    for PF1 in PFs:
        for PF2 in PFs:
            if PF1.price > PF2.price and PF1.projection < PF2.projection:
                PFs.remove(PF1)
                break

    for C1 in Cs:
        for C2 in Cs:
            if C1.price > C2.price and C1.projection < C2.projection:
                Cs.remove(C1)
                break

    for G1 in Gs:
        for G2 in Gs:
            if G1.price > G2.price and G1.projection < G2.projection:
                Gs.remove(G1)
                break

    for F1 in Fs:
        for F2 in Fs:
            if F1.price > F2.price and F1.projection < F2.projection:
                Fs.remove(F1)
                break

    for player1 in players:
        for player2 in players:
            if player1.price > player2.price and player1.projection < player2.projection:
                players.remove(player1)
                break

    print("PGs: ", len(PGs))
    print("SGs: ", len(SGs))
    print("SFs: ", len(SFs))
    print("PFs: ", len(PFs))
    print("Cs: ", len(Cs))
    print("Gs: ", len(Gs))
    print("Fs: ", len(Fs))
    print("players: ", len(players))

    PGs.sort()
    SGs.sort()
    SFs.sort()
    PFs.sort()
    Cs.sort()
    Gs.sort()
    Fs.sort()
    players.sort()

    for PG in PGs:
        print("-PG", PGs.index(PG) + 1,  "/", len(PGs), ": ", PG)
        for SG in SGs:
            print("SG", SGs.index(SG)  + 1, "/", len(SGs), ": ", SG)
            if(SG is PG):
                continue
            for SF in SFs:
                if(SF is PG or SF is SG):
                    continue
                for PF in PFs:
                    pfPrice = PG.price + SG.price + SF.price + PF.price
                    if(PF is PG or PF is SG or PF is SF or pfPrice > 50000):
                        continue
                    for C in Cs:
                        cPrice = PG.price + SG.price + SF.price + PF.price + C.price
                        if(C is PG or C is SG or C is SF or C is PF or cPrice > 50000):
                            continue
                        for G in Gs:
                            gPrice = PG.price + SG.price + SF.price + PF.price + C.price + G.price
                            if(G is PG or G is SG or G is SF or G is PF or G is C or gPrice > 50000):
                                continue
                            for F in Fs:
                                fPrice = PG.price + SG.price + SF.price + PF.price + C.price + G.price + F.price
                                if(F is PG or F is SG or F is SF or F is PF or F is C or F is G or fPrice > 50000):
                                    continue
                                for UTIL in players:
                                    price = PG.price + SG.price + SF.price + PF.price + C.price + G.price + F.price + UTIL.price
                                    if(UTIL is PG or UTIL is SG or UTIL is SF or UTIL is PF or UTIL is C or UTIL is G or UTIL is F or price > 50000):
                                        continue

                                    proj = PG.projection + SG.projection + SF.projection + PF.projection + C.projection + G.projection + F.projection + UTIL.projection
                                    nameList = [PG.name, SG.name, SF.name, PF.name, C.name, G.name, F.name, UTIL.name]
                                    nameList.sort()
                                    same = False

                                    projLen = 20
                                    if(len(allProjections) < projLen):
                                        for x in range (0, len(allProjections)):
                                            if nameList == allProjections[x][1]:
                                                same = True
                                                break
                                        if not same:     
                                            allProjections.append([proj, nameList, {"PG": PG.name, "SG": SG.name, "SF": SF.name, "PF": PF.name, "C": C.name, "G": G.name, "F": F.name, "UTIL": UTIL.name}])
                                            allProjections.sort(key=lambda tup: tup[0])

                                    else:
                                        same = False
                                        for x in range(0,projLen):
                                            if nameList == allProjections[x][1]:
                                                same = True
                                                break
                                        for x in range (0,projLen):
                                            if not same and proj > allProjections[x][0]:
                                                allProjections.insert(x, [proj, nameList, {"PG": PG.name, "SG": SG.name, "SF": SF.name, "PF": PF.name, "C": C.name, "G": G.name, "F": F.name, "UTIL": UTIL.name}])
                                                allProjections.pop(projLen)
                                                break
                                    if(proj > highestProjection):
                                        highestProjection = proj
                                        highLineup = {"PG": PG.name, "SG": SG.name, "SF": SF.name, "PF": PF.name, "C": C.name, "G": G.name, "F": F.name, "UTIL": UTIL.name}
                                        #print(highLineup)
                                        #print(highestProjection)
        
        for x in range(0,projLen):
            ws.write(x, 0, getIDs(allProjections[x][2].get('PG'), xlPlayers, xlPlayersID))
            ws.write(x, 1, getIDs(allProjections[x][2].get('SG'), xlPlayers, xlPlayersID))
            ws.write(x, 2, getIDs(allProjections[x][2].get('SF'), xlPlayers, xlPlayersID))
            ws.write(x, 3, getIDs(allProjections[x][2].get('PF'), xlPlayers, xlPlayersID))
            ws.write(x, 4, getIDs(allProjections[x][2].get('C'), xlPlayers, xlPlayersID))
            ws.write(x, 5, getIDs(allProjections[x][2].get('G'), xlPlayers, xlPlayersID))
            ws.write(x, 6, getIDs(allProjections[x][2].get('F'), xlPlayers, xlPlayersID))
            ws.write(x, 7, getIDs(allProjections[x][2].get('UTIL'), xlPlayers, xlPlayersID))
            print(round(allProjections[x][0],1), ' - ', allProjections[x][2])
        wb.save('lineups.xls')

    #print(highLineup)
    #print(highestProjection)
    wb.save('lineups.xls')
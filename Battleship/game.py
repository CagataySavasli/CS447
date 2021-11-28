import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

HOST = input("Get host's IP : ")
PORT = int(input("PORT : "))
BUFFERSIZE = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)



myBoard = [["x ","A","B","C","D","E","F","G","H","I","J"],["1 " ,"X","X","X","X","X","X","X","X","X","X"],["2 ","X","X","X","X","X","X","X","X","X","X"],["3 ","X","X","X","X","X","X","X","X","X","X"],["4 ","X","X","X","X","X","X","X","X","X","X"],["5 ","X","X","X","X","X","X","X","X","X","X"],["6 ","X","X","X","X","X","X","X","X","X","X"],["7 ","X","X","X","X","X","X","X","X","X","X"],["8 ","X","X","X","X","X","X","X","X","X","X"],["9 ","X","X","X","X","X","X","X","X","X","X"],["10","X","X","X","X","X","X","X","X","X","X"]]
opponentBoard = [["x ","A","B","C","D","E","F","G","H","I","J"],["1 " ,"X","X","X","X","X","X","X","X","X","X"],["2 ","X","X","X","X","X","X","X","X","X","X"],["3 ","X","X","X","X","X","X","X","X","X","X"],["4 ","X","X","X","X","X","X","X","X","X","X"],["5 ","X","X","X","X","X","X","X","X","X","X"],["6 ","X","X","X","X","X","X","X","X","X","X"],["7 ","X","X","X","X","X","X","X","X","X","X"],["8 ","X","X","X","X","X","X","X","X","X","X"],["9 ","X","X","X","X","X","X","X","X","X","X"],["10","X","X","X","X","X","X","X","X","X","X"]]

needed = [False,0]

dictOfShips = {
    "Carrier" : [5,"C"],
    "Battleship" : [4,"B"],
    "Submarine" : [3,"S"],
    "Destroyer" : [2,"D"],
}


dictOfX = {
    "A" : 1,
    "B" : 2,
    "C" : 3,
    "D" : 4,
    "E" : 5,
    "F" : 6,
    "G" : 7,
    "H" : 8,
    "I" : 9,
    "J" : 10,
}

# CLIENT PART :

def send_msg(msg):
    msg = msg + " "
    client_socket.send(bytes(msg,"utf8"))

def recv_msg():
    while True:
        try:
            msg = client_socket.recv(BUFFERSIZE).decode("utf8")
            checkMsgType(msg)
        except:
            break
    

client_thread = Thread(target=recv_msg)
client_thread.start()


# GAME PART : 

# Print the game boards on the terminal.
def display():

    print("\nOppenent Board : ")    
    for i in range(len(opponentBoard)):
        print(opponentBoard[i])

    print("________________________________________________________")

    print("My Board : ")
    for i in range(len(myBoard)):
        print(myBoard[i])

    print("*********************************************Score : ",needed[1])
    

# get infos needed to put the ships on the game board and check them whether there is a problem.
def getInfoPutShips():

    c = " Carrier - length : 5 - denoted : C "
    b = "Battleship - length : 4 - denoted : B "
    s = "Submarine - length : 3 - denoted : S "
    d = "Destroyer - length : 2 - denoted : D "
    

    listOfShips = ["Carrier", "Battleship", "Submarine", "Destroyer"]

    while True:
        if not listOfShips:
            break

        print(c,"\n",b,"\n",s,"\n",d)

        ship = input("Choose the ship : ")
        if ship not in listOfShips:
            print("Please select one of the given ships and only once ...")
            time.sleep(2)
            continue

        y = input("Choose the X coordinate : ")
        if y not in ["A","B","C","D","E","F","G","H","I","J"]:
            print("Undefined input ...")
            time.sleep(2)
            continue
            
        x = int(input("Choose the Y coordinate : "))
        if x not in range(1,11):
            print("Undefined input ...")
            time.sleep(2)
            continue


        direc = input("Chose the direction (v for vertical, h for horizontal) of ship : ")
        if not ((direc == "v") or (direc == "h")):
            print("Undefined input. Please selact one of 'v' or 'h'.")
            time.sleep(2)
            continue
        else:

            if (direc == "v" and x+dictOfShips[ship][0] > 10) or (direc == "h" and dictOfX[y]+dictOfShips[ship][0] > 10) :
                print("Out of range ...")
                time.sleep(2)
                continue
        if checkBoard(x,dictOfX[y],ship,direc) :
            putShipOnBoard(x,dictOfX[y],ship,direc)
            listOfShips.remove(ship)
        else :
            print("Collesion with an old ship ... ")
            time.sleep(2)
        


#make the needed changes on the list to put the ship on the game boards
def putShipOnBoard(x,y,ship,direc):
    if direc == "v" :
        for i in range(x,x+dictOfShips[ship][0]):
            myBoard[i][y] = dictOfShips[ship][1]
    elif direc == "h" :
        for i in range(y,y+dictOfShips[ship][0]):
            myBoard[x][i] = dictOfShips[ship][1]
    print("The ship has been successfully placed on the game board ...")
    time.sleep(2)
    display()


#check collection while put ships on game board
def checkBoard(x,y,ship,direc):
    if direc == "v" :
        for i in range(x,x+dictOfShips[ship][0]):
            if not myBoard[i][y] == "X" :
                return False
    elif direc == "h" :
        for i in range(y,y+dictOfShips[ship][0]):
            if not myBoard[x][i] == "X" :
                return False
    return True     


def getOpponentHitInfo(msg):
    
    if "OK" in msg:
        needed[1] = needed[1] + 1
    if needed[1] >= 14:
        send_msg(name + " Winner")
    
    

def checkMsgType(msg):
    if "Winner" in msg:
        print(msg)
    
    elif "first" in msg:
        needed[0] = True

    if(name not in msg):
        if "HIT" in msg:
            if "10" in msg:
                checkHitSeccesful(msg[len(msg)-5:])
            else:
                checkHitSeccesful(msg[len(msg)-4:])
        
        else:
            getOpponentHitInfo(msg)
    

def checkHitSeccesful(msg):
    x = int(msg[2:4])
    y = dictOfX[msg[0]]

    shotted = "O"

    if myBoard[x][y] != "X":
        send_msg(name+"OK")
        myBoard[x][y] = shotted
    else:
        send_msg(name+"NOT")
        myBoard[x][y] = shotted
    needed[0] = True
    

    


    print(x,y)

def sendHitCordination():
    display()
    print("Give the cordination of hitting...")
    y = input("Choose the X coordinate : ")
    if y not in ["A","B","C","D","E","F","G","H","I","J"]:
        print("Undefined input ...")
        time.sleep(2)
        sendHitCordination()
        
    x = int(input("Choose the Y coordinate : "))
    if x not in range(1,11):
        print("Undefined input ...")
        time.sleep(2)
        sendHitCordination()
    opponentBoard[x][dictOfX[y]] = "O"
    msg = name + "HIT" + str(y) + "/" + str(x)
    needed[0] = False
    send_msg(msg)



def firstMethod():

    global name 
    name = input("Give Your Name : ")
    send_msg(name)
    
    

    display()

    getInfoPutShips()

    while True:
        if needed[0]:   
            sendHitCordination()




firstMethod()

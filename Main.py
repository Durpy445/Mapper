import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin

Nodes = {
    
}


Visited = [None] * 10000

def StrToInt(Value):
    Returned = 0
    for Letter in Value:
        Returned +=ord(Letter)
    
    return Returned

def HashFunction(Value,Array):
    Size = len(Array)
    if type(Value) == str:
        Value = StrToInt(Value) 
    return Value % Size

def InBounds(Value,Array):
    if Value < 0 or Value >= len(Array):
        return False
    else:
        return True

def Probe(Value,Array):
    Location = HashFunction(Value,Array)
    
    Up = True
    Down = True

    Positive = 1
    Negative = -1
    while Up or Down:
        if Up:
            CurrentLocation = Location + Positive   
            Data = Array[CurrentLocation]
            if InBounds(CurrentLocation,Array):
                if Data == None or Data == Value:
                    return CurrentLocation
            else:
                Up = False
            Positive += 1

        if Down:
            CurrentLocation = Location + Negative
            Data = Array[CurrentLocation]
            if InBounds(CurrentLocation,Array):
                if Data == None or Data == Value:
                    return CurrentLocation
            else:
                Down = False
            Negative -= 1

            


    return None

def CheckHash(Value,Array):
    print(Value)
    Location = HashFunction(Value,Array)
    if Array[Location] == Value:
        return Location
    else:
        ProbeLocation = Probe(Value,Array)
        return ProbeLocation

def StoreInHash(Value,Array):
    Location = HashFunction(Value,Array)
    if Array[Location] == None:
        Array[Location] = Value
        return True
    elif Array[Location] == Value:
        return True
    else:
        ProbeLocation = Probe(Value,Array)
        if ProbeLocation != None:
            Array[ProbeLocation] = Value
            return True
    return False


def GetLinks(Link):
    Returns = []
   
    
    try:
         response = requests.get(Link)
    except:
        print("Cant Get Response")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all("a") 
    
    for link in links:
        Thing = link.get("href")
      
        if Thing != None and len(Thing) > 0:
            if (Thing[0] == "/" or Thing[0] == "h"):
                try:
                    Thing = urljoin(Link, Thing) 
                    Returns.append(Thing)
                except:
                    print("Can't Join Url")
        
               
        
    return Returns


def CheckIfInList(Value,List): 
    Location = CheckHash(Value,List)
    if List[Location] == Value:
        return True
    else:
        return False


def CheckIfInMap(Value,Map):
    if Value in Map:
        return True
    else:
        return False

def Check(Link,Depth,MaxDepth,Map,Visited):
    print(Link)
    StoreInHash(Link,Visited)
    
    if CheckIfInMap(Link,Map) == False:
        Links = GetLinks(Link)
        if Links:
            Map[Link] = GetLinks(Link)
        else:
            return None
        

    if Depth > MaxDepth :
        return None
   
    Depth += 1
    for I in range(len(Map[Link])):
        if CheckIfInList(Map[Link][I],Visited) == False:
            Check(Map[Link][I],Depth,MaxDepth,Map,Visited)
       

StartTime = time.time
Check("https://www.youtube.com/watch?v=iCh7KuXBO78",0,1,Nodes,Visited)
TotalTime = time.time - StartTime

File = open("Output.txt","w")
File.write("Took " + str(StartTime) + " Seconds to complete \n\n")
for Node in Nodes:
    File.write(Node + "\n")
    for Item in Nodes[Node]:
        File.write("       "+Item)
    File.write("\n\n\n")

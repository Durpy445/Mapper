import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin

Nodes = {
    
}
Visited = []

def GetLinks(Link):
    Returns = []
    response = requests.get(Link)
    soup = BeautifulSoup(response.content, 'html.parser')

    links = soup.find_all("a") 
    for link in links:
        Thing = link.get("href")
      
        if Thing != None:
            Thing = urljoin(Link, Thing)    
            print(Thing)
            Returns.append(Thing)
        
        
    return Returns


def CheckIfInList(Value,List):
    for i in range(len(List)):
        if List[i] == Value:
            return True
    return False

def CheckIfInMap(Value,Map):
    if Value in Map:
        return True
    else:
        return False

def Check(Link,Depth,MaxDepth,Map):
   
    if Depth > MaxDepth or CheckIfInList(Link,Visited):
        return None
    Visited.append(Link)
    if CheckIfInMap(Link,Map) == False:
        Map[Link] = GetLinks(Link)
    Depth += 1
    for I in range(len(Map[Link])):
        Check(Map[Link][I],Depth,MaxDepth,Map)


Check("https://www.google.com/search?client=firefox-b-d&q=import+soup+python",0,1,Nodes)
print(Visited)

for Node in Nodes:
    print("\n\n\n",Node)
    print(Nodes[Node],"\n")
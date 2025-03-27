import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
import threading
import asyncio
from asyncio import TaskGroup

MaxThreads = 5


Nodes = {}

Visited = []
ToVisit = []


def GetLinks(Link,Nodes,ToVisit,Visited,Depth,MaxDepth):
    if Depth >= MaxDepth:
        print("more")
        return None
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
        try:
            Thing = urljoin(Link, Thing) 
            Returns.append(Thing)
            if not(Thing in ToVisit or Thing in Visited):
                ToVisit.append([Thing,Depth + 1])
        except:
            print("Can't Join Url")
    print("Returning")
    Nodes[Link] = Returns


async def UseLink(Link,Nodes,ToVisit,Visited,Depth,MaxDepth):
    GetLinks(Link,Nodes,ToVisit,Visited,Depth,MaxDepth)
   

async def UseLinks(Nodes,ToVisit,Visited,MaxDepth):
    async with TaskGroup() as group:
        for I in range(MaxThreads):
            if len(ToVisit) > 0:
                    print("A")
                    group.create_task(UseLink(ToVisit[0][0],Nodes,ToVisit,Visited,ToVisit[0][1],MaxDepth))
                    Visited.append(ToVisit[0][0])
                    ToVisit.pop(0)

   


def Start(StartingLink,Nodes,ToVisit,Visited,MaxDepth):
    GetLinks(StartingLink,Nodes,ToVisit,Visited,0,MaxDepth)
    while len(ToVisit) > 0:
       print(len(ToVisit))
       asyncio.run(UseLinks(Nodes,ToVisit,Visited,MaxDepth))
        


        
       
StartTime = time.time() 
Start("https://www.youtube.com/",Nodes,ToVisit,Visited,2)
TotalTime = time.time() 
TotalTime = (TotalTime - StartTime)


File = open("Output.txt","w")
File.write("Took " + str(TotalTime) + " Seconds to complete \n\n")
for Node in Nodes:
    File.write(Node + "\n")
    for Item in Nodes[Node]:
        File.write("       "+Item)
    File.write("\n\n\n")    

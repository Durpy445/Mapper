import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
import threading
MaxThreads = 4


Nodes = {}

Visited = []
ToVisit = []

def GetLinks(Link,Nodes,ToVisit,Visited):
    if not (Link in Visited):
        Visited.append(Link)
   
    if Link in ToVisit:
        ToVisit.remove(Link)
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
                ToVisit.append(Thing)
        except:
            print("Can't Join Url")
    Nodes[Link] = Returns

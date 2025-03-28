import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

MaxThreads = 10

Nodes = {}
Visited = set()
ToVisit = []
DepthArray = []

async def GetLinks(session, Link, Nodes, ToVisit, Visited, Depth, MaxDepth, DepthArray):
    if Depth >= MaxDepth:
        return
    
    Returns = []
    try:
        async with session.get(Link) as response:
            html = await response.text()
    except:
        print(f"Can't get response from {Link}")
        return

    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all("a")

    for link in links:
        Thing = link.get("href")
        if Thing:
            Thing = urljoin(Link, Thing)
            if Thing not in Returns:
                Returns.append(Thing)
            if Thing not in ToVisit and Thing not in Visited:
                if Depth + 1 <= MaxDepth:
                    ToVisit.append(Thing)
                    DepthArray.append(Depth + 1)
    
    Nodes[Link] = Returns


async def UseLink(session, Link, Nodes, ToVisit, Visited, Depth, MaxDepth, DepthArray, Num):
    await GetLinks(session, Link, Nodes, ToVisit, Visited, Depth, MaxDepth, DepthArray)


async def UseLinks(Nodes, ToVisit, Visited, MaxDepth, DepthArray):
    async with aiohttp.ClientSession() as session:
        while ToVisit:
            tasks = []
            for _ in range(min(MaxThreads, len(ToVisit))):
                link = ToVisit.pop(0)
                depth = DepthArray.pop(0)
                Visited.add(link)
                tasks.append(UseLink(session, link, Nodes, ToVisit, Visited, depth, MaxDepth, DepthArray, len(Visited)))

            await asyncio.gather(*tasks)


def Start(StartingLink, Nodes, ToVisit, Visited, MaxDepth, DepthArray):
    ToVisit.append(StartingLink)
    DepthArray.append(0)
    if hasattr(asyncio, 'WindowsSelectorEventLoopPolicy'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(UseLinks(Nodes, ToVisit, Visited, MaxDepth, DepthArray))


StartTime = time.time()
Start("https://www.youtube.com/", Nodes, ToVisit, Visited, 3, DepthArray)
TotalTime = time.time() - StartTime

with open("Output.txt", "w") as File:
    File.write(f"Took {TotalTime:.2f} Seconds to complete\n\n")
    for Node in Nodes:
        File.write(Node + "\n")
        for Item in Nodes[Node]:
            File.write("       " + Item + "\n")
        File.write("\n\n\n")

print(f"Crawling completed in {TotalTime:.2f} seconds.")

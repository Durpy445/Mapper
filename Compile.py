Output = open("Output.txt","r")
i = 0
CurrentSite = ""
Websites = {}
for Line in Output:
    if i%2 == 0:
        if Line in Websites:
            Websites[Line] += 1
        else:
            Websites[Line] = 1
        CurrentSite = Line
        
        print(Line)
    else:
        Strings = Line.split(",")
        for Website in Strings:
            if Website != "":
                if Website in Websites:
                    Websites[Website] += 1
                else:
                    Websites[Website] = 1
        print(Strings)
        pass


    i += 1
print(Websites)
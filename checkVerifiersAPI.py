import requests, json, sys


BASE_URL = "https://www.speedrun.com/api/v1/"
ITTGameID = "kdkm3re1"

def getUsername(userID):
    url = BASE_URL + "users/" + userID
    info = requests.get(url)
    info = info.json()
    name = info["data"]["names"]["international"]
    return name

def getExaminerUsername(info):
    return getUsername(info["status"]["examiner"])

def getJsonOnPage(url):
    info = requests.get(url)
    info = info.json()
    return info

def nextPage(info):
    offset = info["pagination"]["offset"]
    if(offset == 0):
        return getJsonOnPage(info["pagination"]["links"][0]["uri"])
    else:
        try:
            return getJsonOnPage(info["pagination"]["links"][1]["uri"])
        except IndexError:
            return {}

def getGameIDFromName(gameName):
    url = BASE_URL + "games?name=" + gameName
    info = requests.get(url)
    info = info.json()
    gameID = info["data"][0]["id"]
    return gameID

def getPlayerIDFromUsername(username):
    url = BASE_URL + "users?name=" + username
    info = requests.get(url)
    info = info.json()
    playerID = info["data"][0]["id"]
    return playerID

def getAllVerifierIDsInJson(gameID):
    url = BASE_URL + "games/" + gameID
    verifiers = getJsonOnPage(url)
    verifiers = verifiers["data"]["moderators"]
    IDs = {}
    for i in verifiers:
        IDs[i] = 0
    return IDs

def dictionaryOfIDsToUsernames(dictionaryOfIDs):
    #Have to make list to force it to make a copy, otherwise error while itterating over dictionary because it changes size
    for i in list(dictionaryOfIDs):
        username = getUsername(i)
        dictionaryOfIDs[username] = dictionaryOfIDs[i]
        del dictionaryOfIDs[i]
    return dictionaryOfIDs
    
def listOfIDsThatVerifiedRuns(gameID):
    url = BASE_URL + "runs?game=" + gameID + "&status=verified"
    info = getJsonOnPage(url)
    verifiers = {}
    while True:
        for run in info["data"]:
            #if its already in the database, then it adds 1
            try:
                verifiers[run["status"]["examiner"]] += 1
            #if its not in the database already, runs this code
            except KeyError:
                verifiers[run["status"]["examiner"]] = 1
        info = nextPage(info)
        if info == {}:
            break
    return verifiers


def getAllVerifiersVerified(gameName):
    gameID = getGameIDFromName(gameName)
    verifiers = listOfIDsThatVerifiedRuns(gameID)
    verifiers = dictionaryOfIDsToUsernames(verifiers)
    return verifiers



    



def getVerifiedFromUsername(username, gameName):
    playerID = getPlayerIDFromUsername(username)
    numberOfRunsVerified = 0
    gameID = getGameIDFromName(gameName)
    url = BASE_URL + "runs?game=" + gameID + "&status=verified"
    info = getJsonOnPage(url)
    while True:
        for run in info["data"]:
            if run["status"]["examiner"] == playerID:
                numberOfRunsVerified += 1
        info = nextPage(info)
        if info == {}:
            break
    return numberOfRunsVerified
    

    


#print(getUsername("xko62e28"))

#print (nextPage(getJsonOnPage("https://www.speedrun.com/api/v1/runs?game=kdkm3re1&status=verified&offset=180")))
#name = "LucklyUnknown"
#print (name + " : " + str(getVerifiedFromUsername(name, "It Takes Two")))
#print ("TheSmallNut" + " : " + str(getVerifiedFromUsername("TheSmallNut", "It Takes Two")))
#print ("Falsepog" + " : " + str(getVerifiedFromUsername("Falsepog", "It Takes Two")))
print(getAllVerifiersVerified("It Takes Two"))
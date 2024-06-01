file = open("./out/jokes_11115/Transcript.txt", "r")
transcript = ""
for line in file:
  transcript = "%s\n%s"%(transcript, line)

file = open("./out/jokes_11115/script.txt", "r")
script = ""
for line in file:
  script = "%s\n%s"%(script, line)

transcriptList = transcript.split(' ')
scriptList = script.split(' ')

import difflib
import re

def getFirstCommonElement(startingPositionFirst, startingPositionSecond):
    print(f"The first no match with {scriptList[startingPositionFirst]} and {transcriptList[startingPositionSecond]} ")
    bestDifference = [len(scriptList), startingPositionSecond] # plan is to minimize how much we are going down the script list
    if startingPositionSecond == 174:
      print("got here")
    for i, scriptWord in enumerate(scriptList[startingPositionFirst:]):
      print(i)
      for j, transcriptWord in enumerate(transcriptList[startingPositionSecond:]):
        # the addition of the two differences to be the smallest
        if difflib.SequenceMatcher(None, scriptWord.lower(), transcriptWord.lower()).ratio() >= 0.8 and bestDifference[0]+bestDifference[1] > i+j:
          print(transcriptWord)
          bestDifference[0] = i
          bestDifference[1] = j
    # grab the new script that is the addition of all elements in each list
    stringListFirst = ""
    for i in range(bestDifference[0]+1):
      if i+startingPositionFirst>=len(scriptList)-1:
        stringListFirst += f" {scriptList[i+startingPositionFirst]}"
        break
      else:
        stringListFirst += f" {scriptList[i+startingPositionFirst]}"
      print(scriptList[i+startingPositionFirst])

    print(bestDifference[1])
    print(len(transcriptList))
    for i in range(bestDifference[1]+1): # get starting and ending times...
      if startingPositionSecond==len(transcriptList)-1:
        break
      print(f"removing: {transcriptList[startingPositionSecond]}")
      del transcriptList[startingPositionSecond]

    # make a new timestamp
    print(f"inserting: {stringListFirst}")
    for i in range(len(transcriptList)):
      print(transcriptList[i])
    transcriptList.insert(startingPositionSecond, stringListFirst)
    print("inserted")

    for i in range(len(transcriptList)):
      print(transcriptList[i])
    print()
    # return the new positions from both iters
    return bestDifference[0]+1+startingPositionFirst

def recursiveSolutionCompare(scriptIter, transcriptIter):
  if scriptIter >= len(scriptList) or transcriptIter >= len(transcriptList):
    return True

  ratio = difflib.SequenceMatcher(None, scriptList[scriptIter].lower(), transcriptList[transcriptIter].lower()).ratio() # to lower case every letter!!!!!!!!!!!!
  # if it is just a one word change the ratio is 0.8888, if two then 0.8
  if ratio >= 0.8:
    print("good")
    transcriptList[transcriptIter] = scriptList[scriptIter]
    return recursiveSolutionCompare(scriptIter+1, transcriptIter+1)
  else:
    # find the next good match
    # make all the ones in between into one that is the same
    #recursive...
    newPosition = getFirstCommonElement(scriptIter, transcriptIter)
    return recursiveSolutionCompare(newPosition, transcriptIter+1)


check = recursiveSolutionCompare(0,0)
print(check)

newScript = ""
for i in range(len(transcriptList)):
  newScript+=f"{transcriptList[i]} "
newScript = re.sub(' +', ' ', newScript)
print(newScript)
f = open("./out/jokes_11115/BetterTranscript.txt", "a")
f.write(newScript)
f.close()

import difflib
import re
from projectManager import base_dir

def fixTranscript(transcript, script):
  # transcriptList = transcript # comes already as a list
  transcriptList = []
  scriptList = []
  for sentence in transcript:
    if len(sentence) == 1:
      continue
    for word in sentence['result']:
      transcriptList.append(word)

  scriptList = script.split(' ')

  def getFirstCommonElement(startingPositionFirst, startingPositionSecond):
      # print(f"The first no match with {scriptList[startingPositionFirst]} and {transcriptList[startingPositionSecond]['word']} ")
      bestDifference = [len(scriptList), startingPositionSecond] # plan is to minimize how much we are going down the script list
      for i, scriptWord in enumerate(scriptList[startingPositionFirst:startingPositionFirst+10]):
        for j, transcriptWord in enumerate(transcriptList[startingPositionSecond:]):
          # the addition of the two differences to be the smallest
          if difflib.SequenceMatcher(None, scriptWord.lower(), transcriptWord['word'].lower()).ratio() >= 0.8 and bestDifference[0]+bestDifference[1] > i+j:
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

      endTime = 0
      startTime = transcriptList[startingPositionSecond]['start']
      for i in range(bestDifference[1]+1): # get starting and ending times...
        if startingPositionSecond==len(transcriptList)-1:
          break
        endTime = transcriptList[startingPositionSecond]['end']
        del transcriptList[startingPositionSecond]

      # make a new timestamp
      newWord = {'conf': 1.0, 'end': endTime, 'start': startTime, 'word': stringListFirst}
      transcriptList.insert(startingPositionSecond, newWord)

      # return the new positions from both iters
      return bestDifference[0]+1+startingPositionFirst

  def recursiveSolutionCompare(scriptIter, transcriptIter):
    if scriptIter >= len(scriptList) or transcriptIter >= len(transcriptList):
      return True

    ratio = difflib.SequenceMatcher(None, scriptList[scriptIter].lower(), transcriptList[transcriptIter]['word'].lower()).ratio() # to lower case every letter!!!!!!!!!!!!
    # if it is just a one word change the ratio is 0.8888, if two then 0.8
    if ratio >= 0.8:
      transcriptList[transcriptIter]['word'] = scriptList[scriptIter]
      return recursiveSolutionCompare(scriptIter+1, transcriptIter+1)
    else:
      # find the next good match
      # make all the ones in between into one that is the same
      #recursive...
      newPosition = getFirstCommonElement(scriptIter, transcriptIter)
      return recursiveSolutionCompare(newPosition, transcriptIter+1)
    
  
  check = recursiveSolutionCompare(0,0)

  # newScript = ""
  # for i in range(len(transcriptList)):
  #   newScript+=f"{transcriptList[i]} "
  # newScript = re.sub(' +', ' ', newScript)
  return transcriptList
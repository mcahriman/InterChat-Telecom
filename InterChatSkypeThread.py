from InterChatSkypeListener import InterchatSkypeListener
import threading
import Skype4Py
import sys

class InterChatSkypeThread():
  def __init__(self, dispatcher):
    self.dispatcher = dispatcher
    self.skypeObj = Skype4Py.Skype(Events = InterchatSkypeListener(self.dispatcher))
  def start(self):
    self.skypeObj.Attach()
    return True
  def getDispatcher(self):
    return self.dispatcher
  def getSkypeObject(self):
    return self.skypeObj
  def writeToChannel(self, message, channel):
    print(channel)
    if(channel):
      try:
        chanTo = self.skypeObj.Chat(channel)
        chanTo.SendMessage(message)
        return True
      except:
        print "Message could not be sent:", sys.exc_info()[0]

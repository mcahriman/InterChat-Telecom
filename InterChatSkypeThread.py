from InterChatSkypeListener import InterchatSkypeListener
import threading
import Skype4Py

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
        chanTo = self.skypeObj.Chat(channel)
        chanTo.SendMessage(message)
        return True
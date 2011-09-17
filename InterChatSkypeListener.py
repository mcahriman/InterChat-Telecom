
class InterchatSkypeListener():
  def __init__(self, dispatcher):
    self.dispatcher = dispatcher
  def getDispatcher(self):
      return self.dispatcher
  def MessageStatus ( self, message, status ):
       print message.Chat.Name
       self.getDispatcher().dispatchMessage(message.Chat.Name, message.Sender.FullName, message.Body )
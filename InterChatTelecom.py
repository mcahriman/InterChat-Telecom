import time
from irc import IRCBot, IRCConnection
from InterChatDispatcher import InterChatDispatcher

class InterChatTelecom:
  def launchBot(self):
    dispatcher = InterChatDispatcher()
    dispatcher.launch()
    while 1:
      time.sleep( 5 )
      
InterChatTelecom().launchBot()
import time
from irc import IRCBot, IRCConnection
from InterChatDispatcher import InterChatDispatcher
import sys
reload ( sys )
sys.setdefaultencoding('utf8')

class InterChatTelecom:
  def launchBot(self):
    dispatcher = InterChatDispatcher()
    dispatcher.launch()
    while 1:
      time.sleep( 5 )
      
InterChatTelecom().launchBot()
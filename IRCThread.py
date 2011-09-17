from InterChatIRCListener import InterChatIRCListener
from irc import IRCBot, IRCConnection
import threading

class IRCThread(threading.Thread):
  def __init__(self, host, port, nick, channels, dispatcher):
    self.connexion = IRCConnection(host, port, nick)
    self.botInstance = InterChatIRCListener(self.connexion, dispatcher)
    self.connexion.connect()
    self.channels = channels
    threading.Thread.__init__(self)
  def getConnexion(self):
    return self.connexion
  def run(self):
    for channel in self.channels:
      self.connexion.join(channel) 
    self.connexion.enter_event_loop()
  def writeToChannel(self, message, channel):
    self.botInstance.respond(message,channel);
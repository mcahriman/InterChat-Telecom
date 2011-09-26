from ConfigProvider import ConfigProvider
from GatesProvider import GatesProvider
from ChatManager import ChatManager
from IRCThread import IRCThread
from InterChatSkypeThread import InterChatSkypeThread

class InterChatDispatcher():
  __state = {}
  def __init__(self):
    if(self.__state):
      self.__dict__ = self.__state
    else:
      self.configProvider = ConfigProvider()
      self.gatesProvider = GatesProvider()
      self.chatMgr = ChatManager()
  def launch(self):
    #launch irc
    irc_config = self.configProvider.getConfigSection('irc');
    self.irc_thread = IRCThread( irc_config['host'], irc_config['port'], irc_config['nick'], irc_config['channels'], self)
    self.connexion = self.irc_thread.getConnexion()
    self.irc_thread.start()
    self.skype_thread = InterChatSkypeThread(self)
    self.skype_thread.start()
  def dispatchIRCCommand(self, nick, message, channel):
    print "Message: "+message+" From " + channel
    return "oui"

  def dispatchMessageToChannel(self, channel, message):
    print channel
    channelTo = self.chatMgr.getChanelByAlias(channel)
    if(channelTo['type'] == 'irc'):          
      self.irc_thread.writeToChannel(message, channelTo['channel'])
    if(channelTo['type'] == 'skype'):
      self.skype_thread.writeToChannel(message, channelTo['channel'])

  def messageToChannel(self, channel, message, nick=""):
    parts = message.split(" ")
    if(len(parts) > 1 and self.chatMgr.getChanelByAlias(parts[1])):
        channelTo = self.chatMgr.getChanelByAlias(parts[1])
        body = message.replace("!tele "+parts[1],"")         
        rmessage = "tele from {0}@{1}: {2}".format(nick, channel, body)
        if(channelTo['type'] == 'irc'):          
          self.irc_thread.writeToChannel(rmessage, channelTo['channel'])
        elif(channelTo['type'] == 'skype'):
          self.skype_thread.writeToChannel(rmessage, channelTo['channel'])
  def helpToChannel(self, channel, message):
    with open('help.txt','r') as f:
      for i,l in enumerate(f):
        self.dispatchMessageToChannel(channel, l)
  def getChannelList(self):
    return self.chatMgr.getAliases()
  def dispatchMessage(self, chatname, sendername, body):
#    print body
    channel = self.chatMgr.getChanelById(chatname)
    if( sendername in ['pdobot', 'ictelecom'] ):
      return False;
    for channelTo in self.chatMgr.getAliases():
      channelToFull = self.chatMgr.getChanelByAlias(channelTo)
      if(self.chatMgr.isListening(channelTo, channel['alias'])):
        print "BINGO"
        if (channelToFull['type'] == 'irc'):
          message = "{0}{1}: {2}".format(sendername, channel['alias'], body)
          self.irc_thread.writeToChannel(message, channelTo)
    return False
  def listenChatOn(self, channel1, channel2):
      return self.chatMgr.turnListenOn(channel1, channel2)
  def listenChatOff(self, channel1, channel2):
      return self.chatMgr.turnListenOff(channel1, channel2)      

import yaml
import sys
import threading
import time
from irc import IRCBot, IRCConnection
import Skype4Py
reload ( sys )
sys.setdefaultencoding('utf8')


class ConfigProvider():
  configObject = {}
  def __init__(self):
    f = open('./config.yml','r')
    self.configObject = yaml.load(f)['config']
  def getConfigSection(self, configSection):
    return self.configObject[configSection]

class GatesProvider():
  def __init__(self):
    f = open('./gates.yml','r')
    self.gatesObj =  yaml.load(f)
  def flushgates(self):
    return false

class InterchatSkypeListener():
  def __init__(self, dispatcher):
    self.dispatcher = dispatcher
  def getDispatcher(self):
      return self.dispatcher
  def MessageStatus ( self, message, status ):
       print message.Chat.Name
       self.getDispatcher().dispatchMessage(message.Chat.Name, message.Sender.FullName, message.Body )

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

class InterChatIRCListener(IRCBot):
  def __init__(self, connexion, dispatcher):
      self.dispatcher = dispatcher;
      IRCBot.__init__(self,connexion)
  def getDispatcher(self):
    return dispatcher;
  def ssay(self, nick, message, channel):
      print 'ok'
      return 'WARN: Skype thread is not running'

  def command_patterns(self):
      return (
        ('!cmd', self.dispatch),
        ('!help', self.help),
        ('!tele', self.tele),
        ('!status', self.getstatus),
        ('!channels', self.getChannels),
        ('!listen', self.listen),
        ('!mute', self.mute),
        ('!crzslap', self.slap)
      )

  #command definitions:
  def listen(self,nick,message,channel):
      pts =  message.split(" ")      
      if( len(pts) == 2):
        return self.dispatcher.listenChatOn("#"+channel, pts[1])
  def mute(self,nick,message,channel):
      pts =  message.split(" ")      
      if( len(pts) == 2):
        return self.dispatcher.listenChatOff("#"+channel, pts[1])
  def slap(self,nick,message,channel):
      return "nothing happens"
  def tele(self,nick, message, channel):
      self.dispatcher.messageToChannel(channel, message, nick)
      return False
  def getstatus(self, nick, message, channel):
      return 'Status is ok, '+ nick
  def getChannels(self, nick, message, channel):
      return "Channels Available:" + ",".join(self.getDispatcher().getChannelList())
  def dispatch(self, nick, message,channel):
      return self.getDispatcher().dispatchIRCCommand(nick, message, channel)
  def help(self, nick, message, channel):
      return self.getDispatcher().helpToChannel("#"+channel, message)

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
        if(channelTo['type'] == 'skype'):
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

class ChatManager():
    idsDic = {}
    aliasDic = {}
    config = {}
    listeners = {}
    def __init__(self):
      if (self.idsDic == {}):
        self.configProvider = ConfigProvider()
        skypesection = self.configProvider.getConfigSection('skype')
        ircsection = self.configProvider.getConfigSection('irc')
        for channel in ircsection['channels']:
            self.idsDic[channel] = {'type':'irc', 'channel':channel, 'alias': '#'+channel}
            self.aliasDic[channel] = {'type':'irc', 'channel':channel, 'alias': '#'+channel}
        for channel in skypesection['channels']:
            channel['type'] = "skype"
            channel['alias'] = "&" + channel['name']
            self.idsDic[channel['channel']] = channel
            self.aliasDic['&'+channel['name']] = channel
    def getChanelByAlias(self, alias):
        return self.aliasDic.get(alias, None)
    def getChanelById(self, Id):
        return self.idsDic.get(Id, None)
    def getAliases(self):
        return self.aliasDic.keys()
    def getIds(self):
        return self.idsDic.keys()
    def isListening(self, channel1, channel2):
        if(self.listeners.keys().count(channel1) and self.listeners[channel1].count(channel2)):
            return True
    def turnListenOn(self, channel1, channel2):
        aliases = self.getAliases()
        if(self.getAliases().count(channel1) and self.getAliases().count(channel2) and channel1!=channel2):
            if(self.isListening(channel1,channel2) != True ):
              if self.listeners.get(channel1, False) == False:
                  self.listeners[channel1] = []
              self.listeners[channel1].append(channel2)
              return self.listeners
            elif(channel1 == channel2):
              return "nonono"
            else:
              return "already listening"
    def turnListenOff(self, channel1, channel2):
        if(self.isListening(channel1, channel2)):
          self.listeners[channel1].remove(channel2)
          return self.listeners
      
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

chatManager = ChatManager()
print chatManager.getAliases()
print chatManager.getIds()
dispatcher = InterChatDispatcher()
dispatcher.launch()

while 1:
  time.sleep( 5 )

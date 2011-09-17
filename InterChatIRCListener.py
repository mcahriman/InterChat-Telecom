from irc import IRCBot, IRCConnection

class InterChatIRCListener(IRCBot):
  def __init__(self, connexion, dispatcher):
      self.dispatcher = dispatcher;
      IRCBot.__init__(self,connexion)
  def getDispatcher(self):
    return dispatcher;

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
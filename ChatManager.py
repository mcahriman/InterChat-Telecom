from ConfigProvider import ConfigProvider

class ChatManager():
    idsDic = {}
    aliasDic = {}
    config = {}
    listeners = {}

    def addIRCChannelToDictionary(self, channel):
        self.idsDic[channel] = {'type':'irc', 'channel':channel, 'alias':'#' + channel}
        self.aliasDic[channel] = {'type':'irc', 'channel':channel, 'alias':'#' + channel}


    def addSkypeChannelToDictionary(self, channel):
        channel['type'] = "skype"
        channel['alias'] = "&" + channel['name']
        self.idsDic[channel['channel']] = channel
        self.aliasDic['&' + channel['name']] = channel

    def __init__(self):
      if (self.idsDic == {}):
        self.configProvider = ConfigProvider()
        skypesection = self.configProvider.getConfigSection('skype')
        ircsection = self.configProvider.getConfigSection('irc')
        for channel in ircsection['channels']:
            self.addIRCChannelToDictionary(channel)
        for channel in skypesection['channels']:
            self.addSkypeChannelToDictionary(channel)
            
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
      
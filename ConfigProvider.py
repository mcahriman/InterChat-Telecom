import yaml

class ConfigProvider():
  configObject = {}
  def __init__(self):
    f = open('./config/config.yml','r')
    self.configObject = yaml.load(f)['config']
  def getConfigSection(self, configSection):
    return self.configObject[configSection]
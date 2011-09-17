import yaml

class GatesProvider():
  def __init__(self):
    f = open('./config/gates.yml','r')
    self.gatesObj =  yaml.load(f)
  def flushgates(self):
    return false
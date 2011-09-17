import sys
reload ( sys )
sys.setdefaultencoding('utf8')

__all__ = ["ChatManager", "ConfigProvider", "GatesProvider", "InterChatDispatcher", 
           "InterChatIRCListener", "InterChatSkypeListener", "InterChatSkypeThread",
           "IRCThread"]
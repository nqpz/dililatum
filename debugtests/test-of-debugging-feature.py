def extra1():
    print 'AHA!'

def extra2(stm):
    print stm.debugargs

self.signalactions.add('systemstart', extra1)
self.signalactions.add('gamestart', extra2, self)

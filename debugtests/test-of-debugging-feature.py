def extra1(stm):
    print stm.debugargs

def extra2(stm):


def extra3(char, verb):
    print char.id + ' ' + verb + ' the name..'

action('beforesystemstart', extra1)
action('beforegamestart', extra2)
action('beforecharacteradd', extra3, 'is')

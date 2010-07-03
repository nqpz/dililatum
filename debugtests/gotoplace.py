def goto(event):
    game = event.args[0]
    sys = game.sys
    plcnum = int(sys.etc.arguments[0])
    game.world.set_place(plcnum)

def main():
    action('beforegamerun', goto)

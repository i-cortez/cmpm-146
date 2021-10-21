#!/usr/bin/env python
#

"""
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn


# You have to improve this tree or create an entire new one that is capable
# of winning against all the 5 opponent bots

def setup_behavior_tree():

    root = Selector(name='Custome strategy')

    smother = Sequence(name='Smother')
    canBlitz = Check(blitzable)
    blitzing = Action(blitz)
    smother.child_nodes = [canBlitz, blitzing]

    spread = Sequence(name='efficient spread')
    speadable = Check(spreadConditions)
    spreading = Action(efficientSpread)
    spread.child_nodes = [speadable, spreading]

    Reinforce = Sequence(name='reinforce')
    underAttack = Check(underAttackCheck)
    reinforceA = Action(reinforce)
    Reinforce.child_nodes = [underAttack, reinforceA]

    utilize = Sequence(name='stock')
    Advantage = Check(growing)
    util = Action(useStockpiles)
    utilize.child_nodes = [Advantage, util]


    defaultMove = Action(spread_to_weakest_neutral_planet)
    defaultAttack = Action(attack_weakest_enemy_planet)
    att = Action(attack)

    #root.child_nodes = [Reinforce, spread, att]
    root.child_nodes = [spread, att]

    logging.info('\n' + root.tree_to_string())
    return root

# You don't need to change this function
def do_turn(state):
    behavior_tree.execute(planet_wars)

if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")

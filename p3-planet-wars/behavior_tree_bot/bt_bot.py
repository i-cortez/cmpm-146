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

    utilize = Action(useStockpiles)

    defaultMove = Action(spread_to_weakest_neutral_planet)
    attack = Action(attack_weakest_enemy_planet)

    root.child_nodes = [spread]
    #root.child_nodes = [Reinforce, spread, smother, utilize, attack, defaultMove]
    #root.child_nodes = [Reinforce, spread, smother, utilize, attack, defaultMove]
    #root.child_nodes = [smother, spread, utilize, defaultMove]
    logging.info('\n' + root.tree_to_string())
    return root

    # Top-down construction of behavior tree
    #root = Selector(name='High Level Ordering of Strategies')

    #offensive_plan = Sequence(name='Offensive Strategy')
    #largest_fleet_check = Check(have_largest_fleet)
    #attack = Action(attack_weakest_enemy_planet)
    #offensive_plan.child_nodes = [largest_fleet_check, attack]

    #spread_sequence = Sequence(name='Spread Strategy')
    #neutral_planet_check = Check(if_neutral_planet_available)
    #spread_action = Action(spread_to_weakest_neutral_planet)
    #spread_sequence.child_nodes = [neutral_planet_check, spread_action]

    #root.child_nodes = [offensive_plan, spread_sequence, attack.copy()]

    #logging.info('\n' + root.tree_to_string())
    #return root

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

import sys
sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

def blitz(state):
    
    dest = None
    units = 0
    #growth = 0
    #turnsDiscrepancy = 0
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    travellers = state.enemy_fleets()

    for indiv in travellers:
        dest = indiv.destination_planet
        units = indiv.num_ships - dest.num_ships
        #distanceInTurns = indiv.total_trip_length / indiv.turns_remaining
        #turnsDiscrepancy = distanceInTurns*state.distance() - indiv.turns_remaining()
        #growth = indiv.destination_planet().growth_rate() *

    
    return issue_order(state, strongest_planet.ID, dest, units)

def efficientSpread(state):
    return False
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    targets = state.neutral_planets()
    tuning = [1, 1, 1]
    bestPlanet = None
    bestValue = None

    for target in targets:
        value = target.growth_rate*tuning[0] - target.num_ships*tuning[1] - state.distance(strongest_planet, target.ID)*tuning[2]
        if bestPlanet == None:
            bestPlanet = target
            bestValue = value
        elif value > bestValue:
            bestValue = value
            bestPlanet = target

    neededUnits = target.num_ships + 1
    if(strongest_planet.num_ships < neededUnits):
        return False

    return issue_order(state, strongest_planet.ID, bestPlanet.ID, neededUnits)
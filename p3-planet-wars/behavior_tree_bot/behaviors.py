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
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    for fleet in state.enemy_fleets():
        planetObj = None
        for planet in state.neutral_planets():
            if planet in state.my_planets():
                return False
            if fleet.destination_planet == planet.ID:
                planetObj = planet
        if planetObj == None:
            return False
        units = fleet.num_ships - planetObj.num_ships
        turnsDiscrepancy = state.distance(strongest_planet.ID, planetObj.ID) - fleet.turns_remaining
        if turnsDiscrepancy*planetObj.growth_rate >= 10:
            return False
        growth = planetObj.growth_rate * turnsDiscrepancy
        units = units + growth + 1
    
    return issue_order(state, strongest_planet.ID, fleet.destination_planet, units)

"""
def efficientSpread(state):
    # If there are no neutral planets end the function immediately
    targets = state.neutral_planets()
    if not targets: return False

    # If we have no strong planet, end
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    if not strongest_planet: return False
    #enemy_strongest_planet = max(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    # Flags to help with looping
    isTooManyShips = False
    isEnemyCloser = False
    isEnRoute = False

    # Variables
    tuning = [1, 0.2, 0.5]
    tuning = [1, 0.2, 0.8]
    bestPlanet = None
    bestValue = None

    # Sort the neutral planets in ascending order
    # based on the value of num_ships
    #def getValue(v): return v["num_ships"]
    #targets.sort(key=getValue)

    for target in targets:
        # Determine if we already have ships en route to the target
        for fleet in state.my_fleets():
            if fleet.destination_planet == target.ID:
                isEnRoute = True
                break
        if isEnRoute: return False

        # Determine if the enemy already sending ships
        for fleet in state.enemy_fleets():
            if fleet.destination_planet == target.ID:
                # Determine if the fleet source planet is closer than
                # our strongest planet
                myDistance = state.distance(strongest_planet.ID, target.ID)
                enemyDistance = state.distance(fleet.source_planet, target.ID)
                if enemyDistance < myDistance:
                    isEnemyCloser = True
                    break
                # If the enemy is already sending ships, how many?
                # Currently an arbitrary value, can be optimized
                # Example: can be modified based on how many turns
                # remain until arrival
                if fleet.num_ships > (target.num_ships + 10):
                    isTooManyShips = True
                    break
        if isTooManyShips or isEnemyCloser: return False

        value = (target.growth_rate*tuning[0]) - (target.num_ships*tuning[1]) - state.distance(strongest_planet.ID, target.ID)*tuning[2]
        if bestPlanet == None or value > bestValue:
            bestPlanet = target
            bestValue = value

    neededUnits = bestPlanet.num_ships + 1
    if strongest_planet.num_ships < neededUnits or not strongest_planet or not bestPlanet:
        return False
    return issue_order(state, strongest_planet.ID, bestPlanet.ID, neededUnits)
"""

def efficientSpread(state):
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    tuning = [1, 0.2, 0.8]
    myFleets = state.my_fleets()
    destination_assigned = False
    x = 0
    isEnRoute = False

    # Sort the list of obtained neutral planets
    # based on value in ascending order
    targets = state.neutral_planets()
    valueSorted = []
    for target in targets:
        value = (target.growth_rate*tuning[0]) - (target.num_ships*tuning[1]) - state.distance(strongest_planet.ID, target.ID)*tuning[2]
        valueSorted.append((value, target))
    valueSorted.sort(key=lambda y: y[0], reverse=True)

    # Now that the list is sorted, loop through the list of neutral planets
    # and determine if it is and determine if it is worth dispatching a fleet
    target = None
    for target in valueSorted:
        for fleet in myFleets:
            if fleet.destination_planet == target[1].ID:
                isEnRoute = True
                break
        if not isEnRoute:
            break
    
    neededUnits = target[1].num_ships + 1
    #if strongest_planet.num_ships < neededUnits or not strongest_planet or not target[1]:
        #return False
    return issue_order(state, strongest_planet.ID, target[1].ID, neededUnits)
    
    """
    while not destination_assigned:
        if len(myFleets) < 1:
            destination_assigned = True
        for fleet in myFleets:
            if fleet.destination_planet == valueSorted[x][1]:
                break
        if x == len(valueSorted) -1:
            destination_assigned = True
        else:
            x = x+1

    planet = valueSorted[0][1].ID
    #return False
    neededUnits = planet + 1
    if strongest_planet.num_ships < neededUnits or not strongest_planet:
        return False
    return issue_order(state, strongest_planet.ID, planet, neededUnits)
    """


def useStockpiles(state):
    source = None
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True))
    planet = next(my_planets)
    if planet.num_ships > 100:
        source = planet
    if len(state.not_my_planets()) == 0:
        return issue_order(state, state.my_planets()[0].ID, state.my_planets()[1].ID, source.num_ships/2)

    if len(state.neutral_planets()) > 0:
        targets = iter(sorted(state.neutral_planets(), key=lambda p: p.num_ships))
        target = next(targets)
        neededUnits = target.num_ships + 1
        if not source or not target:
            return False
        return issue_order(state, source.ID, target.ID, neededUnits)

    enemys = iter(sorted(state.enemy_planets(), key=lambda p: p.num_ships))
    weakest = next(enemys)
    if not source or not weakest:
            return False
    return issue_order(state, source.ID, weakest.ID, source.num_ships/2)

def reinforce(state):
    for fleet in state.enemy_fleets():
        for planet in state.my_planets():
            if fleet.destination_planet == planet.ID:
                counter = 0
                for my_fleet in state.my_fleets():
                    if my_fleet.destination_planet == fleet.destination_planet:
                        counter = counter + my_fleet.num_ships
                if counter+planet.num_ships > fleet.num_ships:
                        return False
                strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
                return issue_order(state, strongest_planet.ID, fleet.destination_planet, fleet.num_ships)
        
    return False


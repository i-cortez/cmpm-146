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

def attack(state):
    if len(state.enemy_planets()) < 1:
        return False
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True))

    enemy_planets = [planet for planet in state.enemy_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    enemy_planets.sort(key=lambda p: p.num_ships)
    
    try:
        my_planet = next(my_planets)
        for planet in enemy_planets:
            units = planet.num_ships + state.distance(my_planet.ID, planet.ID)*planet.growth_rate + 1
            #return False
            if my_planet.num_ships > units:
                issue_order(state, my_planet.ID, planet.ID, units)
                my_planet = next(my_planets)
            else:
                my_planet = next(my_planets)
    except StopIteration:
        return False

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
    # If there are no neutral planets end the function immediately
    if state.neutral_planets() == []: return False
    if state.my_planets() == []: return False

    # Get a list of neutral planets that we are not en route to and sort
    # in ascending order
    neutral_planets = [planet for planet in state.neutral_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    neutral_planets.sort(key=lambda p: p.num_ships)

    # Get the list of enemy fleets
    enemyFleetsList = state.enemy_fleets()

    # Get an iterator to the list of neutral planets and planets the enemy
    # is attacking
    target_planets = iter(neutral_planets)
    #enemyPlanets = iter(enemyAttackingPlanets)
    enemyFleets = iter(enemyFleetsList)

    # Get an iterator to a list of our planets sorted in Descending order
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))

    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        enemyFleet = next(enemyFleets)
        while True:
            required_ships = target_planet.num_ships + 1
            # Check to see if the enemy is attacking the current target planet
            if enemyFleet.destination_planet == target_planet.ID:
                required_ships = target_planet.num_ships + state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1
                if my_planet.num_ships > required_ships:
                    issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                    my_planet = next(my_planets)
                    target_planet = next(target_planets)
                    enemyFleet = next(enemyFleets)
                else:
                    my_planet = next(my_planets)
            elif my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)

    except StopIteration:
        if enemyFleetsList == []:
            required_ships = target_planet.num_ships + 1
            if my_planet.num_ships > required_ships:
                return issue_order(state, my_planet.ID, target_planet.ID, required_ships)
        return False
    

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
"""
def useStockpiles(state):
    strongest = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    for planet in state.my_planets():
        if planet.num_ships > 100:
            return issue_order(state, planet.ID, strongest.ID, planet.num_ships/2)
    return False

"""
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
"""

def reinforce(state):
    # Variables needed
    planetUnderAttack = None
    numEnemyShips = None
    hasEnoughShips = False

    # Begin by checking if there is a planet that is under attack
    for planet in state.my_planets():
        for enemyFleet in state.enemy_fleets():
            if enemyFleet.destination_planet == planet.ID:
                growth = planet.growth_rate*enemyFleet.turns_remaining
                if (planet.num_ships + growth) < enemyFleet.num_ships:
                    planetUnderAttack = planet
                    numEnemyShips = enemyFleet.num_ships
                    break
        if planetUnderAttack: break
    if planetUnderAttack is None: return False

    
    # A planet is under attack, check if ships are already on the way
    for myFleet in state.my_fleets():
        totalShips = planetUnderAttack.num_ships + myFleet.num_ships
        if myFleet.destination_planet == planetUnderAttack.ID:
            # If there are enough ships to weather this attack
            # break the loop and end the function
            if totalShips > numEnemyShips:
                hasEnoughShips = True
                break
    if hasEnoughShips: return False

    
    # A planet is under attack, and ships are Not on the way or ships are on 
    # the way but not enough
    # Proceed by finding our closest planet to the planet under attack
    shortestDist = None
    closestPlanet = None
    planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True))
    shortestDist = state.distance(next(planets).ID,planetUnderAttack.ID)
    for planet in planets:
        distance = state.distance(planet.ID, planetUnderAttack.ID)
        if distance < shortestDist:
            shortestDist = distance
            if planet.num_ships + 100 > numEnemyShips:
                closestPlanet = planet
                return issue_order(state, closestPlanet.ID, planetUnderAttack.ID, numEnemyShips + 25)
    
    return False

def press(state):
    planets = iter(sorted(state.enemy_planets(), key=lambda p: p.num_ships, reverse=False))
    units = None
    for planet in planets:
        my_planets = state.my_planets()
        closestPlanet = None
        shortestDist = state.distance(my_planets.pop(0).ID, planet.ID)
        for my_planet in my_planets:
            distance = state.distance(planet.ID, my_planet.ID)
            if distance < shortestDist or closestPlanet==None:
                shortestDist = distance
                if planet.num_ships < my_planet.num_ships + 10:
                    closestPlanet = planet
                    units = (planet.num_ships) + (distance*planet.growth_rate) + 1
        if(closestPlanet != None):
            return issue_order(state, closestPlanet.ID, planet.ID, units)
    return False


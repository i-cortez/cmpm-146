

from planet_wars import Planet


def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def blitzable(state):
  if len(state.enemy_fleets())<1:
        return False
  growth = 0
  eGrowth = 0
  for planet in state.my_planets():
    growth += planet.growth_rate
  for eplanet in state.enemy_planets():
    eGrowth += eplanet.growth_rate
  if(growth > eGrowth):
    return True
  else:
    return False

def spreadConditions(state):
  #planets = state.neutral_planets()
  if len(state.neutral_planets()) > 1:
    return True
  else:
    return False

def underAttackCheck(state):
  enemys = iter(sorted(state.enemy_fleets(), key=lambda p: p.num_ships, reverse=True))

  my_planets = state.my_planets()

  for fleet in enemys:
    for planet in my_planets:
      if fleet.destination_planet == planet.ID:
        return True
  return False
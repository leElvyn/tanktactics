def get_distance(tank_offender, tank_defender):
    """return the distance between the 2 tanks"""
    return max(abs((tank_offender.x - tank_defender.x)), abs((tank_offender.y - tank_defender.y)))
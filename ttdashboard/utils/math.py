def get_distance(tank_offender, tank_deffender):
    """return the distance between the 2 tanks"""
    return max(abs((tank_offender.x - tank_deffender.x)), abs((tank_offender.y - tank_deffender.y)))
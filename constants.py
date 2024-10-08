import enum

class Status(enum.Enum):
    WORKING = 'WO'
    NOT_WORKING = 'NW'
    E_WASTE = 'EW'
    
class Owner(enum.Enum):
    HIGH_COURT = 'HC'
    ECOURT = 'EC'
    DISTRICT_COURT = 'DC'
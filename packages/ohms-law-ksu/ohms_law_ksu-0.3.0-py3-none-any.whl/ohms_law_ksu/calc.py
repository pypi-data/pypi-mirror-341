def calcVoltage(current, resistance):
    # Returns current * resistance
    return current * resistance
    
def calcCurrent(voltage, resistance):
    # Returns voltage / resistance
    return voltage / resistance
    
def calcResistance(voltage, current):
    # Returns voltage / current
    return voltage / current

class Drive:
    def __init__(self):
        pass
        
    def calcVoltage(self, current, resistance):
        return calcVoltage(current, resistance)
    
    def calcCurrent(self, voltage, resistance):
        return calcCurrent(voltage, resistance)
    
    def calcResistance(self, voltage, current):
        return calcResistance(voltage, current)
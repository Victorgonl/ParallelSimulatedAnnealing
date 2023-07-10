def linear_reduction(temperature, alpha):
    return temperature - alpha

def geometric_reduction(temperature, alpha):
    return temperature * (1 - alpha)
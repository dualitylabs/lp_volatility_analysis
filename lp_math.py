import math
from mpmath import *

def validate_params(k, gamma, p_0, p_1):
    assert (k > 0), "k must be greater than 0"
    assert (gamma <= 1 and gamma > 0), "gamma must be between 0 and 1"
    assert (p_0 > 0 and p_1 > 0), "prices must be greater than 0"

def calc_reserves(k, p_0):
    r_a = math.sqrt(k/p_0)
    r_b = k/r_a
    return (r_a, r_b)

def calc_delta_alpha(k, gamma, p_0, p_1):
    factor = math.sqrt(k / p_0) / (2 * gamma)
    radicand = gamma * (4 * (p_0 / p_1) + gamma - 2) + 1
    main = math.sqrt(radicand) - gamma - 1
    delta_alpha = factor * main
    assert (delta_alpha > 0), "delta_alpha is not greater than 0"
    return delta_alpha

def calc_delta_beta(k, gamma, p_0, delta_alpha):
    r_a, r_b = calc_reserves(k, p_0)
    delta_beta = r_b - (k/(r_a + gamma*delta_alpha))
    assert (delta_beta > 0), "delta_beta is not greater than 0"
    return delta_beta

def calc_updated_price(r_a, r_b, delta_alpha, delta_beta):
    price = (r_b - delta_beta) / (r_a + delta_alpha)
    assert (price > 0), "price is not greater than 0"
    return price

def calc_updated_k(r_a, r_b, delta_alpha, delta_beta):
    return (r_a + delta_alpha) * (r_b - delta_beta)

# equation shows that the growth factor of our LP position given a trade
# depends solely on gamma and the ratio of p_0 to p_1 (and is therefore scale invariant)
def calc_rootk_growth(gamma, p_0, p_1):
    radicand = gamma * (4 * (p_0 / p_1) + gamma - 2) + 1
    numerator = math.sqrt(radicand) - (1 - gamma)
    denominator = gamma * (math.sqrt(radicand) + (1 - gamma))

    return math.sqrt(numerator/denominator)

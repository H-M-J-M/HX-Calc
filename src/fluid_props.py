import math


def fnGasCp(coeffs: list[float], T: float, MW: float) -> float:
    """
    Calculate gas heat capacity using DIPPR 102.
    
    Args:
        coeffs (list[float]): List containing the coefficients for the gas.
        T: Temperature of the gas.
        MW: Molecular weight of the gas.
    
    Returns:
        float: Heat capacity of the gas in SI base units.
    """
    sinh_term = coeffs[1] * ((coeffs[2] /T) / math.sinh(coeffs[2] /T))**2
    cosh_term = coeffs[3] * ((coeffs[4] /T) / math.cosh(coeffs[4] /T))**2
    cp_mol = coeffs[0] + sinh_term + cosh_term
    cp_mass = cp_mol / MW
    return cp_mass

def fnLiquidCp(coeffs: list[float], T: float, MW: float) -> float:
    """
    Calculate liquid heat capacity using a polynomial equation.
    
    Args:
        coeffs (list[float]): List of coefficients [C1, C2, C3, C4, C5].
        T: Temperature (K).
        MW: Molecular weight.
        
    Returns:
        float: Heat capacity (mass basis) in SI base units.
    """
    cp_mol = coeffs[0] + coeffs[1] * T + coeffs[2] * T**2 + coeffs[3] * T**3 + coeffs[4] * T**4
    cp_mass = cp_mol / MW
    return cp_mass

def fnGasMu(coeffs: list[float], T: float) -> float:
    """
    Calculate gas dynamic viscosity.
    Note: only 3 coefficients from the full formula implemented (fix after deadline)
    
    Args:
        coeffs (list[float]): List containing the coefficients for the gas.
        T: Temperature of the gas.
    
    Returns:
        float: Dynamic viscosity of the gas in SI base units.
    """
    mu = (coeffs[0] * T**coeffs[1]) / (1 + (coeffs[2] / T))
    return mu

def fnLiquidMu(coeffs: list[float], T: float) -> float:
    """
    Calculate liquid dynamic viscosity.
    Note: only 2 coefficients from the full formula implemented (fix after deadline)

    Args:
        coeffs (list[float]): List containing the coefficients for the liquid.
        T: Temperature of the liquid.
    
    Returns:
        float: Dynamic viscosity of the liquid in SI base units.
    """
    mu = coeffs[0] * math.exp(coeffs[1] / T)
    return mu

def fnGasK(coeffs: list[float], T: float) -> float:
    """
    Calculate gas thermal conductivity.
    
    Args:
        coeffs (list[float]): List containing the coefficients for the gas.
        T: Temperature of the gas.
    
    Returns:
        float: Thermal conductivity of the gas in SI base units.
    """
    k = (coeffs[0] * T**coeffs[1]) / (1 + (coeffs[2] / T) + (coeffs[3] / T**2))
    return k

def fnLiquidK(coeffs: list[float], T: float) -> float:
    """
    Calculate liquid thermal conductivity.
    Note: only 2 coefficients from the full formula implemented (fix after deadline)
    
    Args:
        coeffs (list[float]): List containing the coefficients for the liquid.
        T: Temperature of the liquid.
    
    Returns:
        float: Thermal conductivity of the liquid in SI base units.
    """
    k = coeffs[0] + T * coeffs[1]
    return k

# gas density will be provided from precomputed empirical correlations for the specific fluid (in this case the Span-Wagner EoS).
# 2.784058

def fnLiquidRho(coeffs: list[float], T: float, MW: float) -> float:
    """
    Calculate liquid density.
    
    Args:
        coeffs (list[float]): List containing the coefficients for the liquid.
        T: Temperature of the liquid.
    
    Returns:
        float: Density of the liquid in SI base units.
    """
    rho = (coeffs[0] / (coeffs[1]**(1 + (1 - (T/coeffs[2]))**coeffs[3]))) * MW
    return rho
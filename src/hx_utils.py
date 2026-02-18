import math

def fnPrandtl(cp: float, mu: float, k: float) -> float:
    """
    Calculate Prandtl number.
    
    Args:
        cp: Heat capacity of the fluid.
        mu: Dynamic viscosity of the fluid.
        k: Thermal conductivity of the fluid.
    
    Returns:
        float: Prandtl number of the fluid.
    """
    return (cp * mu) / k

def fnReynolds(rho: float, u: float, D_h: float, mu: float) -> float:
    """
    Calculate Reynolds number.
    
    Args:
        rho: Density of the fluid.
        u: Velocity of the fluid.
        D_h: Characteristic length of the fluid.
        mu: Dynamic viscosity of the fluid.
    
    Returns:
        float: Reynolds number of the fluid.
    """
    return rho * u * D_h / mu

def fnLMTD(T_i: float, T_o: float, t_i:float, t_o:float) -> float:
    """
    Calculate Log Mean Temperature Difference.
    
    Args:
        T_i: Hot side inlet temperature.
        T_o: Hot side outlet temperature.
        t_i: Cold side inlet temperature.
        t_o: Cold side outlet temperature.
    
    Returns:
        float: Log Mean Temperature Difference of the fluid.
    """
    lmtd = ( (T_i-t_o) - (T_o-t_i) ) / math.log( (T_i-t_o) / (T_o-t_i) )

    return lmtd

def fnDuty(m_dot: float, cp: float, T_i: float, T_o: float) -> float:
    """
    Calculate heat duty.
    
    Args:
        m_dot: Mass flow rate of the fluid.
        cp: Heat capacity of the fluid.
        T_i: Inlet temperature of the fluid.
        T_o: Outlet temperature of the fluid.
    
    Returns:
        float: Heat duty of the fluid.
    """
    return m_dot * cp * (T_i - T_o)
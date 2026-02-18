from src.design_structure import HXGeometry
import math

# --- Heat Transfer & Pressure Drop Correlations ---

def fnShellHTC(geo: HXGeometry, flow_rate: float, cp: float, mu: float, k: float, rho: float, mu_wall: float = None) -> float:
    """
    Calculate Shell Side Heat Transfer Coefficient (ho).
    """
    # TODO: Implement Kern's method for shell side HTC
    pass

def fnShellDP(geo: HXGeometry, flow_rate: float, rho: float, mu: float, mu_wall: float = None) -> float:
    """
    Calculate Shell Side Pressure Drop.
    """
    # TODO: Implement Kern's method for shell side Pressure Drop
    pass

def fnTubeHTC(geo: HXGeometry, flow_rate: float, cp: float, mu: float, k: float, rho: float, mu_wall: float = None) -> float:
    """
    Calculate Tube Side Heat Transfer Coefficient (hi).
    """
    # TODO: Implement Sieder-Tate or similar correlation for tube side HTC
    pass

def fnTubeDP(geo: HXGeometry, flow_rate: float, rho: float, mu: float, mu_wall: float = None) -> float:
    """
    Calculate Tube Side Pressure Drop.
    """
    # TODO: Implement tube side pressure drop
    pass

def fnCorrectLMTD(geo: HXGeometry, lmtd: float, T_i: float, T_o: float, t_i:float, t_o:float) -> float:
    """
    Correct LMTD for shell and tube heat exchangers.
    
    Args:
        lmtd: Log mean temperature difference.
        shell_passes: Number of shell passes.
        tube_passes: Number of tube passes.
    
    Returns:
        float: Corrected LMTD.
    """
    if geo.shell_passes == 1 and geo.tube_passes == 1:
        return lmtd
    R = (T_i - T_o) / (t_o - t_i)
    P = (t_o - t_i) / (T_i - t_i)
    if geo.tube_passes % 2 == 0:
        sqR2p1 = math.sqrt(R**2 + 1)
        F_t = ((sqR2p1 * math.log((1-P) / (1 - R*P)))
                /
                ((R-1) * math.log(
                    (2 - P*(R + 1 - sqR2p1))
                    /
                    (2 - P*(R + 1 + sqR2p1))))
                )
    elif geo.shell_passes == 1:
        pass
    else:
        F_t = 1.0

    return F_t * lmtd

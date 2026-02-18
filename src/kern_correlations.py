from src.design_structure import HXGeometry
import math

# --- Heat Transfer & Pressure Drop Correlations ---

def calc_shell_side_h(geo: HXGeometry, flow_rate: float, cp: float, mu: float, k: float, rho: float, mu_wall: float = None) -> float:
    """
    Calculate Shell Side Heat Transfer Coefficient (ho).
    """
    # TODO: Implement Kern's method for shell side HTC
    pass

def calc_shell_side_dP(geo: HXGeometry, flow_rate: float, rho: float, mu: float, mu_wall: float = None) -> float:
    """
    Calculate Shell Side Pressure Drop.
    """
    # TODO: Implement Kern's method for shell side Pressure Drop
    pass

def calc_tube_side_h(geo: HXGeometry, flow_rate: float, cp: float, mu: float, k: float, rho: float, mu_wall: float = None) -> float:
    """
    Calculate Tube Side Heat Transfer Coefficient (hi).
    """
    # TODO: Implement Sieder-Tate or similar correlation for tube side HTC
    pass

def calc_tube_side_dP(geo: HXGeometry, flow_rate: float, rho: float, mu: float, mu_wall: float = None) -> float:
    """
    Calculate Tube Side Pressure Drop.
    """
    # TODO: Implement tube side pressure drop
    pass

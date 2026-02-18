from dataclasses import dataclass, field
from typing import Literal

@dataclass
class ProcessConditions:
    """
    Stores the fixed process conditions for the heat exchanger design.
    """
    # Mass flow rates (kg/s)
    mass_flow_hot: float
    # mass_flow_cold is calculated from heat balance usually, or specified.
    # If both specified, check balance.
    mass_flow_cold: float

    # Temperatures (K)
    t_in_hot: float
    t_out_hot: float
    t_in_cold: float
    t_out_cold: float

    # Pressures (Pa) - Inlet pressures
    p_in_hot: float
    p_in_cold: float
    
    # Allowable pressure drops (Pa)
    max_dp_hot: float
    max_dp_cold: float

    # Dirt/Fouling factors (m^2 K / W)
    fouling_factor_hot: float
    fouling_factor_cold: float

    # Fluid properties coefficients (could be passed here or looked up globally)
    # For now, we assume the solver knows which fluid is which.


@dataclass
class HXGeometry:
    """
    Defines the geometry of a specific heat exchanger design candidate.
    """
    # Fixed parameters (usually)
    tube_od: float  # Outer Diameter (m)
    tube_id: float  # Inner Diameter (m)
    tube_length: float # Length (m)
    
    # Variable parameters (iteration variables)
    shell_diameter: float # Inner Diameter of Shell (m)
    num_tubes: int
    
    num_tube_passes: int # 1, 2, 4, 6...
    num_shell_passes: int # 1, 2...
    
    pitch_ratio: float # Pitch / Tube OD
    pitch_layout: Literal["triangular", "square"]
    
    baffle_cut: float # e.g., 0.25 for 25%
    baffle_spacing: float # Distance between baffles (m)
    
    head_type: str = "Front Head A" # Placeholder for now

from dataclasses import dataclass, field
from typing import Literal

@dataclass
class ProcessConditions:
    """
    Stores the fixed process conditions for the heat exchanger design.
    """
    # Mass flow rates (kg/s)
    m_flow_tube: float
    m_flow_shell: float

    # Temperatures (K)
    t_in_tube: float
    t_out_tube: float
    t_in_shell: float
    t_out_shell: float

    # Pressures (Pa) - Inlet pressures
    p_in_tube: float
    p_in_shell: float

    # Pressure Drops (Pa) - Maximum Allowable
    max_Pdrop_tube: float
    max_Pdrop_shell: float


@dataclass
class HXGeometry:
    """
    Defines the geometry of a specific heat exchanger design candidate.
    """
    # Fixed parameters
    tube_od: float  # Outer Diameter (m)
    tube_id: float  # Inner Diameter (m)
    tube_length: float # Length (m) (Assume fixed unless we can't find a soution without changing length)
    baffle_cut: float # Usually 0.25 (25%) is optimal.

    # Independent variables (iteration variables)
    pitch_layout: Literal["triangular", "square"]
    num_tube_passes: int # 1, 2, 4, 6...
    num_shell_passes: int # 1, 2...
    head_type: Literal["pull-through_floating", "split-ring_floating", "fixed_u-tube", "outside_packed"]
    
    # Dependent variables (calculated)
    num_tubes: int
    bundle_diameter: float # diameter of the tube bundle (m)
    bundle_clearance: float # clearance between the tube bundle and the shell (m)
    shell_diameter: float # Inner Diameter of Shell (m)
    
    baffle_spacing: float # Distance between baffles (m)

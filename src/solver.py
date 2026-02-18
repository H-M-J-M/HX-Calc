import math
from typing import List, Tuple, Optional
from src.design_structure import ProcessConditions, HXGeometry
from src import kern_correlations as kern
from src import hx_utils as hxu

def solve_design(
    conditions: ProcessConditions,
    tube_od: float,
    tube_id: float,
    tube_length: float,
    hot_fluid_props: dict,
    cold_fluid_props: dict,
    hot_side: str = "shell",
    fixed_pitch_layout: str = "triangular",
    fixed_pitch_ratio: float = 1.25
) -> List[HXGeometry]:
    """
    Main iteration loop.
    Iterates: Head Type -> Shell Passes -> Tube Passes.
    Converges: Assumed U -> Geometry.
    """
    valid_designs = []
    
    # Iteration Parameters
    tube_passes_options = [1, 2, 4, 6, 8]
    shell_passes_options = [1, 2]
    # Head types loop could also be user-defined if needed, but keeping here for now.
    head_types = ["Front Head A", "Front Head B"] 
    
    # Duty Calculation
    Q = hxu.fnDuty(conditions.m_flow_tube, hot_fluid_props['cp'], conditions.t_in_hot, conditions.t_out_hot)
        
    # Calculate LMTD
    lmtd = hxu.fnLMTD(conditions.t_in_hot, conditions.t_out_hot, conditions.t_in_cold, conditions.t_out_cold)
    
    print(f"Target Duty: {Q/1000:.2f} kW")
    print(f"LMTD (base): {lmtd:.2f} K")

    # Brute Force Loop
    for head in head_types:
        for s_pass in shell_passes_options:
            for t_pass in tube_passes_options:
                
                # F-Correction (Simplified)
                F = 1.0 # TODO: User to implement F-correction if needed
                if s_pass == 1 and t_pass >= 2: F = 0.9
                elif s_pass == 2 and t_pass >= 4: F = 0.95
                
                dT_mean = F * lmtd
                
                # Attempt to find a converged design for this configuration
                design = converge_design_for_config(
                    conditions, 
                    Q, dT_mean, 
                    tube_od, tube_id, tube_length, 
                    fixed_pitch_ratio, fixed_pitch_layout,
                    s_pass, t_pass, head,
                    hot_fluid_props, cold_fluid_props,
                    hot_side
                )
                
                if design:
                    valid_designs.append(design)

    # Sort by Area
    valid_designs.sort(key=lambda x: x.num_tubes * x.shell_diameter)
    
    return valid_designs

def converge_design_for_config(
    cond: ProcessConditions,
    Q: float,
    dT_mean: float,
    tod: float, tid: float, L: float,
    pr: float, layout: str,
    s_pass: int, t_pass: int, head: str,
    hot_props: dict, cold_props: dict, hot_side: str
) -> Optional[HXGeometry]:
    """
    Iterates on Assumed U to find a consistent geometry.
    """
    
    # Initial Guess for U (W/m2K)
    U_trial = 500.0 
    
    max_iter = 10
    tolerance = 0.05 # 5%
    
    for i in range(max_iter):
        # 1. Calc Required Area
        A_req = Q / (U_trial * dT_mean)
        
        # 2. Calc Required Tubes
        # A = Nt * pi * D * L
        N_req = A_req / (math.pi * tod * L)
        
        # 3. Find Shell Diameter (USING USER LOGIC)
        Ds = kern.get_optimal_shell_diameter(N_req, tod, pr, layout, t_pass)
        
        if Ds is None:
            return None # No shell fits
            
        # 4. Get Actual Tube Count for this shell (USING USER LOGIC)
        Nt = kern.get_tube_count_for_shell(Ds, tod, pr, layout, t_pass)
        
        # 5. Construct Geometry
        geo = HXGeometry(
            tube_od=tod,
            tube_id=tid,
            tube_length=L,
            shell_diameter=Ds,
            num_tubes=Nt,
            num_tube_passes=t_pass,
            num_shell_passes=s_pass,
            pitch_ratio=pr,
            pitch_layout=layout,
            baffle_cut=0.25,
            baffle_spacing=Ds * 0.4, # Rule: 0.4 * Ds
            head_type=head
        )
        
        # 6. Evaluate Performance
        is_valid, metrics = evaluate_design(geo, cond, hot_props, cold_props, hot_side, Q, dT_mean)
        
        U_calc = metrics.get('U_design')
        if not U_calc or U_calc <= 0:
            return None
            
        # 7. Check Convergence
        error = abs(U_calc - U_trial) / U_trial
        
        if error < tolerance:
            if not is_valid: return None
            return geo
        else:
            U_trial = 0.5 * U_trial + 0.5 * U_calc
            
    return None

def evaluate_design(
    geo: HXGeometry, 
    cond: ProcessConditions, 
    hot_props: dict, 
    cold_props: dict, 
    hot_side: str,
    Q_target: float,
    dT_mean: float
) -> Tuple[bool, dict]:
    # (Same as before, simplified for brevity)
    # Assign Fluids
    if hot_side == "shell":
        shell_props, shell_flow = hot_props, cond.m_flow_tube
        tube_props, tube_flow = cold_props, cond.m_flow_shell
        shell_fouling = cond.fouling_factor_hot
        tube_fouling = cond.fouling_factor_cold
        allowed_dp_shell = cond.max_dp_hot
        allowed_dp_tube = cond.max_dp_cold
    else:
        shell_props, shell_flow = cold_props, cond.m_flow_shell
        tube_props, tube_flow = hot_props, cond.m_flow_tube
        shell_fouling = cond.fouling_factor_cold
        tube_fouling = cond.fouling_factor_hot
        allowed_dp_shell = cond.max_dp_cold
        allowed_dp_tube = cond.max_dp_hot
        
    ho = kern.fnShellHTC(geo, shell_flow, shell_props['cp'], shell_props['mu'], shell_props['k'], shell_props['rho'])
    hi = kern.fnTubeHTC(geo, tube_flow, tube_props['cp'], tube_props['mu'], tube_props['k'], tube_props['rho'])
    
    R_wall = 0.0001
    
    if ho is None or hi is None: 
         # Placeholder for dry run
        ho = 1000.0; hi = 1000.0
    
    area_ratio = geo.tube_od / geo.tube_id
    try:
         u_clean = 1.0 / ( (1.0/ho) + (area_ratio/hi) + R_wall )
    except ZeroDivisionError: return False, {}
        
    R_f_total = shell_fouling + (tube_fouling * area_ratio)
    u_design = 1.0 / ( (1.0/u_clean) + R_f_total )
    
    dPs = kern.fnShellDP(geo, shell_flow, shell_props['rho'], shell_props['mu'])
    dPt = kern.fnTubeDP(geo, tube_flow, tube_props['rho'], tube_props['mu'])
    
    if dPs is None: dPs = 1000.0
    if dPt is None: dPt = 1000.0

    A_req = Q_target / (u_design * dT_mean)
    A_prov = geo.num_tubes * math.pi * geo.tube_od * geo.tube_length
    
    is_valid = True
    if A_prov < A_req: is_valid = False
    if dPs > allowed_dp_shell: is_valid = False
    if dPt > allowed_dp_tube: is_valid = False
    
    metrics = {"U_design": u_design, "A_req": A_req, "A_prov": A_prov, "dPs": dPs, "dPt": dPt}
    return is_valid, metrics

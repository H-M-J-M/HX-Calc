from src.fluid_props import fnGasCp, fnLiquidCp, fnGasMu, fnLiquidMu, fnGasK, fnLiquidK, fnLiquidRho
from src.design_structure import ProcessConditions
from src.solver import solve_design

def run_kern_method():
    print("Running Kern's Method Design...")
    
    # --- HARDCODED INPUTS
        
    # Mass Flows (kg/s)
    m_tube = 35.0 # CO2 M Flow
    m_shell = 0.0 # calculated below
    
    # Temperatures (K)
    t_in_tube = 673.15
    t_out_tube = 393.15
    t_in_shell = 298.15
    t_out_shell = 333.15
    
    # Pressures (Pa)
    p_in_tube = 2.8e5 
    p_in_shell = 3e5
    
    # Allowable DeltaP (Pa)
    max_Pdrop_tube = p_in_tube * 0.1
    max_Pdrop_shell = p_in_shell * 0.1
    

    # --- FLUID PROPERTIES COEFFICIENTS ---
    tube_coeffs = {
        'cp': [29370.0, 34540.0, 1428.0, 26400.0, 588.0],
        'mu': [0.000002148, 0.46, 290],
        'k': [3.69, -0.3838, 964, 1860000],
        'rho': [2.7840579163],
        'MW': [44.0095]
    }
    shell_coeffs = {
        'cp': [85600.0, -122.0, 0.5605, -0.001452, 2.008E-6],
        'mu': [-10.306, 703.01],
        'k': [0.2333, -0.000275],
        'rho': [1.7968, 0.28749, 552, 0.3226],
        'MW': [76.1407]
    }
    
    # Calculate Mean Properties
    avg_temp_tube = (t_in_tube + t_out_tube) / 2
    avg_temp_shell = (t_in_shell + t_out_shell) / 2
    
    # TODO Add handling of gas in shell and vice versa
    tube_scalar_props = {'rho': 2.7840579163,
                         'cp': fnGasCp(tube_coeffs['cp'], avg_temp_tube, tube_coeffs['MW']),
                         'mu': fnGasMu(tube_coeffs['mu'], avg_temp_tube),
                         'k': fnGasK(tube_coeffs['k'], avg_temp_tube)}
    shell_scalar_props = {'rho': fnLiquidRho(shell_coeffs['rho'],avg_temp_shell, shell_coeffs['MW']),
                          'cp': fnLiquidCp(shell_coeffs['cp'],avg_temp_shell, shell_coeffs['MW']),
                          'mu': fnLiquidMu(shell_coeffs['mu'],avg_temp_shell),
                          'k': fnLiquidK(shell_coeffs['k'],avg_temp_shell)}
    
    # Calculate Heat Duty
    Q_tube = fnDuty(m_tube, tube_scalar_props['cp'], t_in_tube, t_out_tube)
    m_shell = Q_tube / (shell_scalar_props['cp'] * (t_out_shell - t_in_shell))

    conditions = ProcessConditions(
        m_flow_tube=m_tube,
        m_flow_shell=m_shell,
        t_in_tube=t_in_tube,
        t_out_tube=t_out_tube,
        t_in_shell=t_in_shell,
        t_out_shell=t_out_shell,
        p_in_tube=p_in_tube,
        p_in_shell=p_in_shell,
        max_Pdrop_tube=max_Pdrop_tube,
        max_Pdrop_shell=max_Pdrop_shell
    )

    # --- FIXED GEOMETRY ---
    tube_od = 0.0270
    tube_id = 0.0250
    tube_length = 8.0
    
    print("Starting Solver...")
    designs = solve_design(
        conditions, 
        tube_od, tube_id, tube_length, 
        tube_scalar_props, shell_scalar_props, 
        hot_side="tube"
    )
    
    print(f"Found {len(designs)} valid designs.")
    for i, d in enumerate(designs[:3]):
        print(f"Option {i+1}: Shell={d.shell_diameter:.3f}m, Tubes={d.num_tubes}, Passes={d.num_tube_passes}")

if __name__ == "__main__":
    run_kern_method()

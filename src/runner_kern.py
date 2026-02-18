from src.fluid_props import fnGasCp, fnLiquidCp, fnGasMu, fnLiquidMu, fnGasK, fnLiquidK, fnLiquidRho
from src.design_structure import ProcessConditions
from src.solver import solve_design

def calculate_scalar_properties(t_mean, coeffs, is_gas=False, mw=1.0):
    """
    Calculates scalar properties at a single temperature.
    """
    props = {}
    if is_gas:
        props['cp'] = fnGasCp(coeffs['cp'], t_mean, mw)
        props['mu'] = fnGasMu(coeffs['mu'], t_mean)
        props['k'] = fnGasK(coeffs['k'], t_mean)
        props['rho'] = 1.0 # Placeholder, gas density usually from EOS
    else:
        props['cp'] = fnLiquidCp(coeffs['cp'], t_mean, mw)
        props['mu'] = fnLiquidMu(coeffs['mu'], t_mean)
        props['k'] = fnLiquidK(coeffs['k'], t_mean)
        props['rho'] = fnLiquidRho(coeffs['rho'], t_mean, mw)
    return props

def run_kern_method():
    print("Running Kern's Method Design...")
    
    # --- HARDCODED INPUTS (Example: Cooling Hot Methanol with Water) ---
    # These should be replaced by user inputs or specific assignment values.
    
    # Example: 100,000 lb/hr Methanol (Hot) from 150F to 100F
    # Cooling water (Cold) from 85F to 120F
    # Converted to SI for calculation
    
    # Mass Flows (kg/s)
    # 100,000 lb/hr = 12.6 kg/s approx
    m_hot = 12.6 
    # Q = m * Cp * dT ... need to balance
    # Let's just put placeholders for now that the USER can edit clearly.
    m_cold = 0.0 # Will be calculated if 0, or specified.
    
    # Temperatures (K)
    t_in_hot = 338.7 # 150 F
    t_out_hot = 310.9 # 100 F
    t_in_cold = 302.6 # 85 F
    t_out_cold = 310.9 # wait, if outlet is same as hot outlet, we have pinch 0. Let's say 290 K to 300 K
    # Using User's Assignment Specs placeholders:
    t_in_hot = 373.15 # 100 C
    t_out_hot = 323.15 # 50 C
    t_in_cold = 293.15 # 20 C
    t_out_cold = 313.15 # 40 C
    
    # Pressures (Pa)
    p_in_hot = 500000 
    p_in_cold = 300000
    
    # Allowable dP (Pa) (10% rule mentioned by user)
    max_dp_hot = 50000 # 50 kPa
    max_dp_cold = 30000 # 30 kPa
    
    # Fouling Factors
    ff_hot = 0.0002
    ff_cold = 0.0002
    
    conditions = ProcessConditions(
        mass_flow_hot=m_hot,
        mass_flow_cold=20.0, # Placeholder, implies Q is balanced.
        t_in_hot=t_in_hot,
        t_out_hot=t_out_hot,
        t_in_cold=t_in_cold,
        t_out_cold=t_out_cold,
        p_in_hot=p_in_hot,
        p_in_cold=p_in_cold,
        max_dp_hot=max_dp_hot,
        max_dp_cold=max_dp_cold,
        fouling_factor_hot=ff_hot,
        fouling_factor_cold=ff_cold
    )
    
    # --- FLUID PROPERTIES COEFFICIENTS ---
    # User needs to fill these in for their specific fluids.
    # Providing dummies for now so code runs.
    hot_coeffs = {
        'cp': [1.0, 0.0, 0.0, 0.0, 0.0], # Constant Cp
        'mu': [0.001, 0.0], # Constant Visc
        'k': [0.6, 0.0],
        'rho': [1000.0, 0.0, 0.0, 0.0]
    }
    cold_coeffs = hot_coeffs.copy() # Same fluid for test
    
    # Calculate Mean Properties
    hot_mean_temp = (t_in_hot + t_out_hot) / 2
    cold_mean_temp = (t_in_cold + t_out_cold) / 2
    
    # Mocking the property calculation for this skeleton
    # In reality, we call calculate_scalar_properties above
    
    # For safe execution WITHOUT valid coefficients, let's hardcode scalar props for the demo
    hot_scalar_props = {'rho': 990.0, 'cp': 4180.0, 'mu': 0.0005, 'k': 0.65}
    cold_scalar_props = {'rho': 998.0, 'cp': 4180.0, 'mu': 0.001, 'k': 0.60}
    
    # --- FIXED GEOMETRY ---
    tube_od = 0.0254 # 1 inch
    tube_id = 0.0210 # approx
    tube_length = 6.096 # 20 ft
    
    print("Starting Solver...")
    designs = solve_design(
        conditions, 
        tube_od, tube_id, tube_length, 
        hot_scalar_props, cold_scalar_props, 
        hot_side="shell"
    )
    
    print(f"Found {len(designs)} valid designs.")
    for i, d in enumerate(designs[:3]):
        print(f"Option {i+1}: Shell={d.shell_diameter:.3f}m, Tubes={d.num_tubes}, Passes={d.num_tube_passes}")

if __name__ == "__main__":
    # If run directly
    run_kern_method()

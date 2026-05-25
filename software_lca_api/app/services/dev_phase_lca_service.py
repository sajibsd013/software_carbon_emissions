class DevPhaseLCACalculator:
    def __init__(self, project_data: dict, custom_assumptions: dict = None):
        self.project_data = project_data
        self.assumptions = {
            'DEVELOPER_WORK_HOURS_PER_MONTH': 10,
            'DEVICE_POWER': 45,
            'DEVELOPER_MACHINES_GRID_INTENSITY': 436,
            'DEVICE_EMBODIED_CARBON': 320_000,
            'DEVICE_LIFETIME_HOURS': 35_040,
            'CI_GRID_INTENSITY': 380,
            'CI_PUE': 1.2,
            'CI_CPU_POWER': 7.68,
            'CI_EMBODIED_CARBON': 1_200_000,
            'CI_SERVER_LIFETIME_HOURS': 35_040,
            'CI_CORE_SHARE': 2,
            'CI_TOTAL_CORES': 96,
            'DATA_TRANSFER_GRID_INTENSITY': 380,
            'ELECTRICITY_PER_GB': 0.001
        }
        if custom_assumptions:
            self.assumptions.update(custom_assumptions)

    def calculate_emissions(self):
        a = self.assumptions
        p = self.project_data
        
        dev_hours = p.get('active_contributors', 0) * a['DEVELOPER_WORK_HOURS_PER_MONTH']
        dev_e = (a['DEVICE_POWER'] * dev_hours) / 1000.0
        dev_m = (a['DEVICE_EMBODIED_CARBON'] / a['DEVICE_LIFETIME_HOURS']) * dev_hours 
        dev_total = (dev_e * a['DEVELOPER_MACHINES_GRID_INTENSITY']) + dev_m

        ci_hours = (p.get('ci_runs_per_month', 0) * p.get('ci_avg_duration_min', 0)) / 60.0 
        ci_e = ci_hours * a['CI_CPU_POWER'] * a['CI_PUE'] / 1000.0
        ci_m = (a['CI_EMBODIED_CARBON'] / a['CI_SERVER_LIFETIME_HOURS']) * (a['CI_CORE_SHARE'] / a['CI_TOTAL_CORES']) * ci_hours 
        ci_total = (ci_e * a['CI_GRID_INTENSITY']) + ci_m

        gb = (p.get('repo_size_mb', 0) * p.get('ci_runs_per_month', 0)) / 1024.0
        data_total = (gb * a['ELECTRICITY_PER_GB']) * a['DATA_TRANSFER_GRID_INTENSITY']

        total = dev_total + ci_total + data_total
        commits = p.get('monthly_commits', 1) or 1 

        return {
            "dev_machine_carbon_footprint_gCO2eq": round(dev_total, 2),
            "ci_cd_carbon_footprint_gCO2eq": round(ci_total, 2),
            "data_transfer_carbon_footprint_gCO2eq": round(data_total, 2),
            "total_carbon_footprint_gCO2eq": round(total, 2),
            "carbon_footprint_per_commit_gCO2eq": round(total / commits, 2)
        }
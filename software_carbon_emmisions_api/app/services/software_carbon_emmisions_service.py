from datetime import datetime
from math import isnan

class SoftwareCarbonEmission:
    def __init__(self, **kwargs):
        """
        Expected kwargs:

        Development Phase (mandatory):
            - months (int/float)
            - repo_size_gb (float)
            - avg_monthly_active_contributors (int)
            - total_ci_runs (int)
            - total_ci_duration_minutes (float)
            - total_commits (int)

        Deployment Phase (mandatory):
            - total_deployments (int)
            - deployment_duration_minutes (float)
            - cloud_region (str)

        Usage Phase (mandatory):
            - monthly_active_users (int/float)  
            - avg_monthly_usage_hours_per_user (float)
            - avg_monthly_data_transfer_gb (float) — avg GB transferred per user per month (up + down)

        Optional:
            - db_migration_gb (float)                  — default 0.0
            - docker_image_size_gb (float)             — default 0.0
            - dependency_size_gb (float)               — default 0.0
            - server_uptime_hours_per_month (float)    — default 0.0
            - server_instance_power_w (float)          — default 0.0
            - assumptions (dict)                       — override any constant
        """
        try:
            #  Development Phase 
            self.months = kwargs['months']
            self.repo_size_gb = kwargs['repo_size_gb']
            self.avg_monthly_active_contributors = kwargs['avg_monthly_active_contributors']
            self.total_ci_runs = kwargs['total_ci_runs']
            self.total_ci_duration_minutes = kwargs['total_ci_duration_minutes']
            self.total_commits = kwargs['total_commits']

            #  Deployment Phase
            self.total_deployments = kwargs['total_deployments']
            self.deployment_duration_minutes = kwargs['deployment_duration_minutes']
            self.cloud_region = kwargs['cloud_region']

            #  Usage Phase  
            self.monthly_active_users = kwargs['monthly_active_users']
            self.avg_monthly_usage_hours_per_user = kwargs['avg_monthly_usage_hours_per_user']
            self.avg_monthly_data_transfer_gb = kwargs['avg_monthly_data_transfer_gb']

        except KeyError as e:
            raise ValueError(f"Missing mandatory parameter: {e}")

        # ── Optional Parameters ────────────────────────────────────────────────
        self.db_migration_gb               = kwargs.get('db_migration_gb', 0.0)
        self.docker_image_size_gb          = kwargs.get('docker_image_size_gb', 0.0)
        self.dependency_size_gb            = kwargs.get('dependency_size_gb', 0.0)
        self.server_uptime_hours_per_month = kwargs.get('server_uptime_hours_per_month', 0.0)
        self.server_instance_power_w       = kwargs.get('server_instance_power_w', 0.0)

        assumptions = kwargs.get('assumptions', {})

        # ── Default Assumptions ────────────────────────────────────────────────

        """
        Assuming 75% of developers use laptops (average ~45 W under moderate load) and 25% use
        desktops (average ~250 W including monitor), the weighted average power consumption per
        developer machine is approximately 96 W (Ferreira & Domingos, 2025).
        https://doi.org/10.3390/su17104455
        """
        self.DEVELOPER_LAPTOP_PERCENT = self.__get_numeric_assumption(assumptions, 'DEVELOPER_LAPTOP_PERCENT', 0.75)
        self.DEVELOPER_DESKTOP_PERCENT = self.__get_numeric_assumption(assumptions, 'DEVELOPER_DESKTOP_PERCENT', 0.25)
        self.DEVELOPER_LAPTOP_AVG_POWER_W = self.__get_numeric_assumption(assumptions, 'DEVELOPER_LAPTOP_AVG_POWER_W', 45)
        self.DEVELOPER_DESKTOP_AVG_POWER_W = self.__get_numeric_assumption(assumptions, 'DEVELOPER_DESKTOP_AVG_POWER_W', 250)
        self.ARTIFACT_SIZE = self.__get_numeric_assumption(assumptions, 'ARTIFACT_SIZE', 0)

        # Assuming 10 hours of work per developer per month (open source contributors may work less than full-time)
        self.DEVELOPER_WORK_HOURS_PER_MONTH = self.__get_numeric_assumption(assumptions, 'DEVELOPER_WORK_HOURS_PER_MONTH', 10)

        """
        Client device mix for Usage Phase: 75% laptop, 25% desktop, consistent
        with developer machine assumptions in the Development Phase.
        For CLI tools / libraries the end-user is almost always a developer.
        (Ferreira & Domingos, 2025), https://doi.org/10.3390/su17104455
        """
        self.CLIENT_LAPTOP_PERCENT = self.__get_numeric_assumption(assumptions, 'CLIENT_LAPTOP_PERCENT',  0.75)
        self.CLIENT_DESKTOP_PERCENT = self.__get_numeric_assumption(assumptions, 'CLIENT_DESKTOP_PERCENT', 0.25)
        self.CLIENT_MOBILE_OR_TAB_PERCENT = self.__get_numeric_assumption(assumptions, 'CLIENT_MOBILE_OR_TAB_PERCENT', 0.00)

        """
        Average power consumption per client device:
        Laptop: 45 W, Desktop: 250 W (weighted avg ≈ 96 W).
        (Ferreira & Domingos, 2025), https://doi.org/10.3390/su17104455
        """
        self.CLIENT_LAPTOP_POWER_W = self.__get_numeric_assumption(assumptions, 'CLIENT_LAPTOP_POWER_W', 45)   # Watts
        self.CLIENT_DESKTOP_POWER_W = self.__get_numeric_assumption(assumptions, 'CLIENT_DESKTOP_POWER_W', 250)  # Watts
        self.CLIENT_MOBILE_OR_TAB_POWER_W = self.__get_numeric_assumption(assumptions, 'CLIENT_MOBILE_OR_TAB_POWER_W', 5)  # Watts

        """
        Client embodied carbon values:
        Laptop: 218.7 kgCO2eq = 218,700 gCO2eq
        Desktop: 113.2 kgCO2eq (tower) + 400.2 kgCO2eq (monitor) = 513,400 gCO2eq
        (Ferreira & Domingos, 2025), https://doi.org/10.3390/su17104455
        """
        self.CLIENT_LAPTOP_EMBODIED_CARBON = self.__get_numeric_assumption(assumptions, 'CLIENT_LAPTOP_EMBODIED_CARBON', 218_700)  # gCO2eq
        self.CLIENT_DESKTOP_EMBODIED_CARBON = self.__get_numeric_assumption(assumptions, 'CLIENT_DESKTOP_EMBODIED_CARBON', 513_400)  # gCO2eq
        self.CLIENT_MOBILE_OR_TAB_EMBODIED_CARBON = self.__get_numeric_assumption(assumptions, 'CLIENT_MOBILE_OR_TAB_EMBODIED_CARBON', 75_000)  # gCO2eq

        # Shared Constants  

        """
        The global average carbon intensity of electricity was 435 gCO₂/kWh in 2025 and the annual
        decline rate is 3.7% (IEA Electricity 2026, https://www.iea.org/reports/electricity-2026)
        """
        self.GLOBAL_AVG_BASE_INTENSITY = 435    # gCO2eq per kWh
        self.GLOBAL_AVG_ANNUAL_DECLINE_RATE = 0.037  # 3.7%
        self.BASE_YEAR = 2025

        """
        The open-source Cloud Carbon Footprint methodology used for AWS, GCP, and Azure sets a
        default coefficient of 0.001 kWh/GB for network data transfer.
        https://www.cloudcarbonfootprint.org/docs/methodology/
        """
        self.ELECTRICITY_PER_GB = 0.001  # kWh per GB

        """
        GitHub is hosted in Microsoft Azure data centers primarily in Northern Virginia (US East),
        with PUE ≈ 1.16 (Microsoft Sustainability Report, FY25).
        https://datacenters.microsoft.com/sustainability/efficiency/
        """
        self.SERVER_PUE = 1.16

        """
        The power consumption is estimated at 7.5 Watts for a standard 2 vCPU GitHub Actions runner
        based on Cloud Carbon Footprint methodology (Min: 1.56 W, Max: 7.52 W), using a near-max
        value for bursty CI/CD workloads.
        https://www.cloudcarbonfootprint.org/docs/methodology/
        """
        self.SERVER_CPU_POWER = 7.5  # Watts

        self.current_year = datetime.now().year

    def __get_numeric_assumption(self, assumptions: dict, key: str, default):
        value = assumptions.get(key)
        return value if isinstance(value, (int, float)) and not isnan(value) else default

    def __get_server_embodied_carbon(self, allocation):

        """
        4-year (35,040 hours) lifetime was assumed for the server, consistent with standard practices
        in embodied carbon calculations for data center equipment (Ferreira & Domingos, 2025), https://doi.org/10.3390/su17104455.

        """
        SERVER_LIFETIME_HOURS = 35_040 # hours

        """
        Server embodied carbon 1,000 kgCO₂eq per server was assumed, consistent with typical values used for cloud servers in Microsoft
        Azure environments (Microsoft, 2023), https://devblogs.microsoft.com/ise/saving-co2-using-location-and-time-shifting-in-azure/
        """

        SERVER_EMBODIED_CARBON = 1_000_000 # gCO2eq

        """
        Assuming each CI run uses 4 CPU cores on average and the CI server has 96 CPU cores available,
        as GitHub-hosted runners for public repositories use 4 vCPU for standard ubuntu-latest
        workflows (GitHub Documentation), https://docs.github.com/en/actions/reference/runners
        """
        CI_CORE_SHARE = 4
        CI_TOTAL_CORES = 96

        # Embodied Carbon (gCO2eq) = (Server Embodied Carbon / Server Lifetime Hours) * (Core Share / Total Cores) * Allocation
        return (SERVER_EMBODIED_CARBON / SERVER_LIFETIME_HOURS) * (CI_CORE_SHARE / CI_TOTAL_CORES) * allocation

    def __get_region_grid_intensity(self, region):
        """
        Returns the predicted grid carbon intensity (gCO2eq/kWh) for a given
        cloud region, adjusted for annual grid decarbonisation from BASE_YEAR.

        Sources: IEA Electricity 2026, ElectricityMap annual averages.
        https://www.iea.org/reports/electricity-2026
        """
        REGION_METRICS = {
            # ── AWS ───────────────────────────────────────────────────────────
            'us-east-1': {'base_intensity': 380, 'decline_rate': 0.025},  # Virginia
            'us-west-2': {'base_intensity': 135, 'decline_rate': 0.028},  # Oregon
            'eu-west-1': {'base_intensity': 165, 'decline_rate': 0.105},  # Ireland
            'eu-central-1': {'base_intensity': 175, 'decline_rate': 0.110},  # Frankfurt
            'ap-southeast-1': {'base_intensity': 620, 'decline_rate': 0.015},  # Singapore
            'ap-northeast-1': {'base_intensity': 450, 'decline_rate': 0.035},  # Tokyo
            'ap-south-1': {'base_intensity': 680, 'decline_rate': 0.030},  # Mumbai
            'sa-east-1': {'base_intensity': 95,  'decline_rate': 0.020},  # São Paulo
            'cn-north-1': {'base_intensity': 520, 'decline_rate': 0.045},  # Beijing
            # ── Azure ─────────────────────────────────────────────────────────
            'eastus': {'base_intensity': 380, 'decline_rate': 0.025},  # Virginia
            'westus2': {'base_intensity': 125, 'decline_rate': 0.028},  # Washington
            'northeurope': {'base_intensity': 165, 'decline_rate': 0.105},  # Ireland
            'westeurope': {'base_intensity': 170, 'decline_rate': 0.110},  # Netherlands
            'southeastasia': {'base_intensity': 620, 'decline_rate': 0.015},  # Singapore
            'centralindia': {'base_intensity': 680, 'decline_rate': 0.030},  # India
            'brazilsouth': {'base_intensity': 95,  'decline_rate': 0.020},  # São Paulo
            'chinaeast2': {'base_intensity': 520, 'decline_rate': 0.045},  # China
            # ── GCP ───────────────────────────────────────────────────────────
            'us-central1': {'base_intensity': 420, 'decline_rate': 0.028},  # Iowa
            'us-east1': {'base_intensity': 380, 'decline_rate': 0.025},  # South Carolina
            'europe-west1': {'base_intensity': 170, 'decline_rate': 0.110},  # Belgium
            'europe-west3': {'base_intensity': 175, 'decline_rate': 0.110},  # Frankfurt
            'asia-southeast1': {'base_intensity': 620, 'decline_rate': 0.015},  # Singapore
            'asia-south1': {'base_intensity': 675, 'decline_rate': 0.030},  # Mumbai
            'asia-east2': {'base_intensity': 500, 'decline_rate': 0.040},  # Hong Kong
            # ── DigitalOcean ──────────────────────────────────────────────────
            'nyc': {'base_intensity': 360, 'decline_rate': 0.025},  # New York
            'sfo3': {'base_intensity': 220, 'decline_rate': 0.028},  # San Francisco
            'lon1': {'base_intensity': 220, 'decline_rate': 0.045},  # London
            'ams3': {'base_intensity': 170, 'decline_rate': 0.110},  # Amsterdam
            'fra1': {'base_intensity': 175, 'decline_rate': 0.110},  # Frankfurt
            'sgp1': {'base_intensity': 620, 'decline_rate': 0.015},  # Singapore
            'blr1': {'base_intensity': 680, 'decline_rate': 0.030},  # Bangalore
        }

        region_metrics = REGION_METRICS.get(region, {})
        base_intensity = region_metrics.get('base_intensity', self.GLOBAL_AVG_BASE_INTENSITY)
        decline_rate   = region_metrics.get('decline_rate',   self.GLOBAL_AVG_ANNUAL_DECLINE_RATE)

        if self.current_year > self.BASE_YEAR:
            years_ahead = self.current_year - self.BASE_YEAR
            return base_intensity * ((1 - decline_rate) ** years_ahead)

        return base_intensity

    # ══════════════════════════════════════════════════════════════════════════
    # DEVELOPMENT PHASE
    # ══════════════════════════════════════════════════════════════════════════

    def __estimate_developer_device_power(self):
        # Estimated Average Device Power = (LAPTOP_PERCENT × DEVELOPER_LAPTOP_AVG_POWER_W) + (DESKTOP_PERCENT × DEVELOPER_DESKTOP_AVG_POWER_W)
        return (self.DEVELOPER_LAPTOP_PERCENT * self.DEVELOPER_LAPTOP_AVG_POWER_W) + (self.DEVELOPER_DESKTOP_PERCENT * self.DEVELOPER_DESKTOP_AVG_POWER_W)

    def __get_developer_allocation(self):
        # Developer Allocation (hours) = Active Contributors × Work Hours per month × months
        return self.avg_monthly_active_contributors * self.DEVELOPER_WORK_HOURS_PER_MONTH * self.months

    def __get_dev_machine_operational_energy(self):
        # Operational Energy (kWh) = (Power in Watts × Hours of Use) / 1000
        return self.__estimate_developer_device_power() * self.__get_developer_allocation() / 1000.0

    def __get_dev_machine_predicted_grid_intensity(self):
        dev_machine_predicted_grid_intensity = self.GLOBAL_AVG_BASE_INTENSITY

        if self.current_year > self.BASE_YEAR:
            years_ahead = self.current_year - self.BASE_YEAR
            dev_machine_predicted_grid_intensity = self.GLOBAL_AVG_BASE_INTENSITY * ((1 - self.GLOBAL_AVG_ANNUAL_DECLINE_RATE) ** years_ahead)

        return dev_machine_predicted_grid_intensity

    def __get_dev_machine_embodied_carbon(self):
        """
        4-year (35,040 hours) lifetime was assumed for both laptop and desktop
        developer machines, consistent with standard corporate IT replacement
        cycles (Ferreira & Domingos, 2025), https://doi.org/10.3390/su17104455.
        """
        DEVICE_LIFETIME_HOURS = 35_040  # hours

        """
        Embodied carbon values used: 218.7 kg CO₂eq per laptop and 113.2 kg CO₂eq
        (desktop tower) + 400.2 kg CO₂eq (monitor) per desktop setup.
        (Ferreira & Domingos, 2025), https://doi.org/10.3390/su17104455.
        """
        DEVICE_EMBODIED_CARBON_LAPTOP  = 218_700 # gCO2eq
        DEVICE_EMBODIED_CARBON_DESKTOP = 113_200 + 400_200 # gCO2eq

        weighted_avg_embodied_carbon = (DEVICE_EMBODIED_CARBON_LAPTOP * self.DEVELOPER_LAPTOP_PERCENT + DEVICE_EMBODIED_CARBON_DESKTOP * self.DEVELOPER_DESKTOP_PERCENT)

        # Embodied Carbon (gCO2eq) = (Device Embodied Carbon / Device Lifetime Hours) × Developer Allocation
        return (weighted_avg_embodied_carbon / DEVICE_LIFETIME_HOURS) * self.__get_developer_allocation()

    def __calculate_developer_machine_emissions(self):
        # Carbon emissions from electricity usage and hardware while writing code and running local tests
        return self.__get_dev_machine_operational_energy() * self.__get_dev_machine_predicted_grid_intensity() + self.__get_dev_machine_embodied_carbon()

    def __get_ci_cd_run_allocation(self):
        return self.total_ci_duration_minutes / 60.0  # hours

    def __get_ci_cd_predicted_grid_intensity(self):
        """
        The United States (GitHub is hosted in Azure US East / Northern Virginia) average carbon
        intensity of electricity was 390 gCO₂/kWh (≈ 380–410 gCO₂/kWh) in 2025 and the annual
        decline rate is 3.2% (IEA Electricity 2026, https://www.iea.org/reports/electricity-2026)
        """
        CI_BASE_INTENSITY = 390    # gCO2eq per kWh
        CI_ANNUAL_DECLINE    = 0.032  # 3.2%
        CI_BASE_YEAR = 2025

        ci_grid_intensity = CI_BASE_INTENSITY

        if self.current_year > CI_BASE_YEAR:
            years_ahead = self.current_year - CI_BASE_YEAR
            ci_grid_intensity = CI_BASE_INTENSITY * ((1 - CI_ANNUAL_DECLINE) ** years_ahead)

        return ci_grid_intensity

    def __get_ci_cd_operational_energy(self):
        # Operational Energy (kWh) = CI/CD Run Allocation (hours) × CPU Power (Watts) × PUE / 1000
        return self.__get_ci_cd_run_allocation() * self.SERVER_CPU_POWER * self.SERVER_PUE / 1000.0

    def __calculate_ci_cd_emissions(self):
        # Total Carbon Emissions = Operational Energy (E) × Grid Intensity (I) + Embodied Carbon (M)
        return (self.__get_ci_cd_operational_energy() * self.__get_ci_cd_predicted_grid_intensity()
                + self.__get_server_embodied_carbon(self.__get_ci_cd_run_allocation()))

    def __calculate_dev_phase_data_transfer_emissions(self):
        """
        Fotmula adapted from https://arxiv.org/html/2510.26413v1 on estimating
        the environmental impact of CI/CD pipelines through total network data transfer.
        """
        OTHER_NETWORK_DATA = 0.15

        # Data Transfer (GB) = (Repo Size + Dependency Size + Docker Image Size + Artifact Size + Other) × Total CI Runs
        total_data_transfer_gb = ((self.repo_size_gb + self.dependency_size_gb + self.docker_image_size_gb + self.ARTIFACT_SIZE + OTHER_NETWORK_DATA) * self.total_ci_runs)

        data_transfer_energy = total_data_transfer_gb * self.ELECTRICITY_PER_GB

        return data_transfer_energy * self.__get_ci_cd_predicted_grid_intensity()

    def development_phase_emissions(self):
        developer_machines_carbon_emissions = self.__calculate_developer_machine_emissions() # gCO2eq
        ci_server_carbon_emissions = self.__calculate_ci_cd_emissions() # gCO2eq
        data_transfer_carbon_emissions = self.__calculate_dev_phase_data_transfer_emissions() # gCO2eq

        dev_phase_total_carbon_emissions_kgCO2eq = (developer_machines_carbon_emissions + ci_server_carbon_emissions + data_transfer_carbon_emissions) / 1000  # kgCO2eq

        # Carbon Emissions per Functional Unit (R) = Total Carbon Emissions / R
        dev_phase_carbon_emissions_per_month_kgCO2eq = dev_phase_total_carbon_emissions_kgCO2eq / self.months # SCI (kgCO2eq/month)
        dev_phase_carbon_emissions_per_commit_kgCO2eq = dev_phase_total_carbon_emissions_kgCO2eq / self.total_ci_runs # SCI (kgCO2eq/CI run)
        dev_phase_carbon_emissions_per_ci_kgCO2eq = dev_phase_total_carbon_emissions_kgCO2eq / self.total_commits # SCI (kgCO2eq/commit)

        return {
            "dev_phase_carbon_emissions_per_month_kgCO2eq":  dev_phase_carbon_emissions_per_month_kgCO2eq,
            "dev_phase_carbon_emissions_per_commit_kgCO2eq": dev_phase_carbon_emissions_per_commit_kgCO2eq,
            "dev_phase_carbon_emissions_per_ci_kgCO2eq":     dev_phase_carbon_emissions_per_ci_kgCO2eq,
            "dev_phase_total_carbon_emissions_kgCO2eq":      dev_phase_total_carbon_emissions_kgCO2eq,
        }

    # ══════════════════════════════════════════════════════════════════════════
    # DEPLOYMENT PHASE
    # ══════════════════════════════════════════════════════════════════════════

    def __get_deployment_duration_hours(self):
        # Deployment_Duration_Hours = deployment_duration_minutes × total_deployments / 60
        return (self.deployment_duration_minutes * self.total_deployments) / 60.0

    def __get_deployment_predicted_grid_intensity(self):
        return self.__get_region_grid_intensity(self.cloud_region)

    def __calculate_deploy_phase_data_transfer_emissions(self):
        total_data_transfer_gb = (self.docker_image_size_gb + self.db_migration_gb) * self.total_deployments

        # Data Transfer Energy = Data Transfer (GB) * Electricity per GB (kWh)
        data_transfer_energy = total_data_transfer_gb * self.ELECTRICITY_PER_GB

        # Total Carbon Emissions (gCO2eq) = Data Transfer Energy (E) * Grid Intensity (I)
        return data_transfer_energy * self.__get_deployment_predicted_grid_intensity()

    def __calculate_deployment_run_emissions(self):
        deployment_duration_hours = self.__get_deployment_duration_hours()

        # Operational Energy (kWh) = Deployment Duration (hours) × CPU Power (Watts) × PUE / 1000
        deployment_run_energy = deployment_duration_hours * self.SERVER_PUE * self.SERVER_CPU_POWER / 1000.0

        # Total Carbon Emissions = Operational Energy (E) × Grid Intensity (I) + Embodied Carbon (M)
        return (deployment_run_energy * self.__get_deployment_predicted_grid_intensity() + self.__get_server_embodied_carbon(deployment_duration_hours))

    def deployment_phase_emissions(self):
        data_transfer_emissions  = self.__calculate_deploy_phase_data_transfer_emissions()  # gCO2eq
        deployment_run_emissions = self.__calculate_deployment_run_emissions()              # gCO2eq

        deploy_phase_total_carbon_emissions_kgCO2eq = (data_transfer_emissions + deployment_run_emissions) / 1000  # kgCO2eq

        # Carbon Emissions per Functional Unit (R) = Total Carbon Emissions / R
        deploy_phase_carbon_emissions_per_release_kgCO2eq = deploy_phase_total_carbon_emissions_kgCO2eq / self.total_deployments  # SCI (kgCO2eq/release)

        return {
            "deploy_phase_carbon_emissions_per_release_kgCO2eq": deploy_phase_carbon_emissions_per_release_kgCO2eq,
            "deploy_phase_total_carbon_emissions_kgCO2eq": deploy_phase_total_carbon_emissions_kgCO2eq,
        }

    # ══════════════════════════════════════════════════════════════════════════
    # USAGE PHASE
    # ══════════════════════════════════════════════════════════════════════════

    def __get_usage_phase_grid_intensity(self):
        # Server grid intensity reuses the shared REGION_METRICS lookup
        return self.__get_region_grid_intensity(self.cloud_region)

    def __get_client_grid_intensity(self):
        """
        Client device locations are globally distributed and unknown, so the global
        average is used: 435 gCO2/kWh in 2025, declining at 3.7%/year.
        (IEA Electricity 2026), https://www.iea.org/reports/electricity-2026
        """
        client_grid_intensity = self.GLOBAL_AVG_BASE_INTENSITY

        if self.current_year > self.BASE_YEAR:
            years_ahead = self.current_year - self.BASE_YEAR
            client_grid_intensity = self.GLOBAL_AVG_BASE_INTENSITY * ((1 - self.GLOBAL_AVG_ANNUAL_DECLINE_RATE) ** years_ahead)

        return client_grid_intensity

    # ── E_server ───────────────────────────────────────────────────────────────

    def __get_server_operational_energy(self) -> float:
        """
        Energy consumed by the cloud server hosting the software over the period.

        server_uptime_hours_per_month:
            Always-on services (web APIs, infra tools): 730 h/month (≈ 24×365/12)
            CLI libraries: 0 h/month (no server component)
        """
        total_server_hours = self.server_uptime_hours_per_month * self.months

        # server operational energy = server_uptime_hours_per_month × months × server_instance_power_w × (SERVER_PUE / 1000)
        return total_server_hours * self.server_instance_power_w * (self.SERVER_PUE / 1000.0)  # kWh

    def __get_usage_server_embodied_carbon(self):

        total_server_hours = self.server_uptime_hours_per_month * self.months

        return self.__get_server_embodied_carbon(total_server_hours)

    # ── E_client ───────────────────────────────────────────────────────────────

    def __get_client_avg_power_w(self):
        # Weighted Avg Power = (CLIENT_LAPTOP_PERCENT × CLIENT_LAPTOP_POWER_W) + (CLIENT_DESKTOP_PERCENT × CLIENT_DESKTOP_POWER_W + (self.CLIENT_MOBILE_OR_TAB_PERCENT x self.CLIENT_MOBILE_OR_TAB_POWER_W *))
        return (self.CLIENT_LAPTOP_PERCENT  * self.CLIENT_LAPTOP_POWER_W + 
                self.CLIENT_DESKTOP_PERCENT * self.CLIENT_DESKTOP_POWER_W + 
                self.CLIENT_MOBILE_OR_TAB_PERCENT * self.CLIENT_MOBILE_OR_TAB_POWER_W)

    def __get_total_client_usage_hours(self):
        # Total_Client_Hours = monthly_active_users × avg_monthly_usage_hours_per_user × months
        return self.monthly_active_users * self.avg_monthly_usage_hours_per_user * self.months

    def __get_client_operational_energy(self):
        # E_client (kWh) = total_client_usage_hours × client_avg_power_w / 1000
        return self.__get_total_client_usage_hours() * self.__get_client_avg_power_w() / 1000.0

    def __get_client_embodied_carbon(self):
      
        DEVICE_LIFETIME_HOURS = 35_040  # hours

        # Weighted Average Embodied Carbon = (LAPTOP_PERCENT * DEVICE_EMBODIED_CARBON_LAPTOP) + (DESKTOP_PERCENT * DEVICE_EMBODIED_CARBON_DESKTOP) +(MOBILE_OR_TAB_PERCENT * DEVICE_EMBODIED_CARBON_DESKTOP_MOBILE_OR_TAB )
        weighted_avg_embodied_carbon = (self.CLIENT_LAPTOP_PERCENT  * self.CLIENT_LAPTOP_EMBODIED_CARBON + 
                                        self.CLIENT_DESKTOP_PERCENT * self.CLIENT_DESKTOP_EMBODIED_CARBON
                                        + self.CLIENT_MOBILE_OR_TAB_PERCENT * self.CLIENT_MOBILE_OR_TAB_EMBODIED_CARBON)
        
        # Embodied Carbon (gCO2eq) = (DEVICE Embodied Carbon / Device Lifetime Hours) * Developer Allocation
        return (weighted_avg_embodied_carbon / DEVICE_LIFETIME_HOURS) * self.__get_total_client_usage_hours()

    # ── E_network ──────────────────────────────────────────────────────────────

    def __get_usage_network_energy(self):

        # total_transfer_gb = monthly_active_users × avg_monthly_data_transfer_gb × months
        total_transfer_gb = (self.monthly_active_users* self.avg_monthly_data_transfer_gb * self.months)

        # Data Transfer Energy = Data Transfer (GB) * Electricity per GB (kWh)
        return total_transfer_gb * self.ELECTRICITY_PER_GB  # kWh

    # ── Public: Usage Phase ────────────────────────────────────────────────────

    def __calculate_usage_server_emissions(self):
        # Carbon emissions from server-side cloud hosting: (E_server × I_server) + M_server
        return (self.__get_server_operational_energy() * self.__get_usage_phase_grid_intensity()
                + self.__get_usage_server_embodied_carbon())

    def __calculate_usage_client_emissions(self):
        # Carbon emissions from end-user devices: (E_client × I_client) + M_client
        return (self.__get_client_operational_energy() * self.__get_client_grid_intensity()
                + self.__get_client_embodied_carbon())

    def __calculate_usage_data_transfer_emissions(self):
        # Carbon emissions from network transfer between users and server: E_network × I_server
        # Server grid intensity used: transfer path is primarily data-center-to-user (server egress dominant)
        return self.__get_usage_network_energy() * self.__get_usage_phase_grid_intensity()

    def usage_phase_emissions(self):
        server_emissions = self.__calculate_usage_server_emissions() # gCO2eq
        client_emissions = self.__calculate_usage_client_emissions() # gCO2eq
        data_transfer_emissions = self.__calculate_usage_data_transfer_emissions()  # gCO2eq

        usage_phase_total_carbon_emissions_kgCO2eq = (server_emissions + client_emissions + data_transfer_emissions) / 1000  # kgCO2eq

        # Carbon Emissions per Functional Unit (R) = Total Carbon Emissions / R
        usage_phase_carbon_emissions_per_month_kgCO2eq = usage_phase_total_carbon_emissions_kgCO2eq / self.months # SCI (kgCO2eq/month)
        usage_phase_carbon_emissions_per_user_kgCO2eq = usage_phase_total_carbon_emissions_kgCO2eq / self.monthly_active_users # SCI (kgCO2eq/user)

        return {
            "usage_phase_carbon_emissions_per_month_kgCO2eq": usage_phase_carbon_emissions_per_month_kgCO2eq,
            "usage_phase_carbon_emissions_per_user_kgCO2eq": usage_phase_carbon_emissions_per_user_kgCO2eq,
            "usage_phase_total_carbon_emissions_kgCO2eq": usage_phase_total_carbon_emissions_kgCO2eq,
        }

    # ══════════════════════════════════════════════════════════════════════════
    # AGGREGATE
    # ══════════════════════════════════════════════════════════════════════════

    def calculate_emissions(self):
        development_phase = self.development_phase_emissions()
        deployment_phase = self.deployment_phase_emissions()
        usage_phase = self.usage_phase_emissions()

        total_carbon_emissions_kgCO2eq = (
            development_phase["dev_phase_total_carbon_emissions_kgCO2eq"]
            + deployment_phase["deploy_phase_total_carbon_emissions_kgCO2eq"]
            + usage_phase["usage_phase_total_carbon_emissions_kgCO2eq"]
        )

        return {
            **development_phase,
            **deployment_phase,
            **usage_phase,
            "total_carbon_emissions_kgCO2eq": total_carbon_emissions_kgCO2eq,
        }

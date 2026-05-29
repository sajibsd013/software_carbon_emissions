from math import isnan
from datetime import datetime
class SoftwareCarbonEmission:
    def __init__(self, months, repo_size_gb, avg_monthly_active_contributors, total_ci_runs, total_ci_duration_minutes,
                 docker_image_size_gb = 0.3, dependency_size_gb = 0.12,
                 assumptions: dict = {}):


        self.months = months
        self.repo_size_gb = repo_size_gb
        self.avg_monthly_active_contributors = avg_monthly_active_contributors
        self.total_ci_runs = total_ci_runs
        self.total_ci_duration_minutes = total_ci_duration_minutes
        self.docker_image_size_gb = docker_image_size_gb
        self.dependency_size_gb = dependency_size_gb


        # Default assumptions
        """
        Assuming 75% of developers use laptops (average ~45 W under moderate load) and 25% use
        desktops (average ~250 W including monitor), the weighted average power consumption per
        developer machine is approximately 96 W (Ferreira & Domingos, 2025,) https://doi.org/10.3390/su17104455

        """
        self.LAPTOP_PERCENT = self.__get_numeric_assumption(assumptions,'LAPTOP_PERCENT',0.75)
        self.DESKTOP_PERCENT = self.__get_numeric_assumption(assumptions,'DESKTOP_PERCENT',0.25)
        self.DEVELOPER_LAPTOP_AVG_POWER_W = self.__get_numeric_assumption(assumptions,'DEVELOPER_LAPTOP_AVG_POWER_W',45)
        self.DEVELOPER_DESKTOP_AVG_POWER_W = self.__get_numeric_assumption(assumptions,'DEVELOPER_DESKTOP_AVG_POWER_W',250)
        self.ARTIFACT_SIZE = self.__get_numeric_assumption(assumptions,'ARTIFACT_SIZE',0)

        # Assuming 10 hours of work per developer per month (open source contributors may work less than full-time)
        self.DEVELOPER_WORK_HOURS_PER_MONTH = self.__get_numeric_assumption(assumptions,'DEVELOPER_WORK_HOURS_PER_MONTH',10)

        self.current_year = datetime.now().year

    def __get_numeric_assumption(self, assumptions: dict, key: str, default):
        value = assumptions.get(key)

        return value if isinstance(value, (int, float)) and not isnan(value) else default

    def __estimate_developer_device_power(self):
        # Estimate Average Power Consumption per Developer Device (laptop vs desktop)

        # Estimated Average Device Power = (LAPTOP_PERCENT * DEVELOPER_LAPTOP_AVG_POWER_W) + (DESKTOP_PERCENT * DEVELOPER_DESKTOP_AVG_POWER_W)
        return (self.LAPTOP_PERCENT * self.DEVELOPER_LAPTOP_AVG_POWER_W) + (self.DESKTOP_PERCENT * self.DEVELOPER_DESKTOP_AVG_POWER_W)

    def __get_developer_allocation(self):
        # Developer Allocation (hours) = Active Contributors * Work Hours per month

        return self.avg_monthly_active_contributors * self.DEVELOPER_WORK_HOURS_PER_MONTH * self.months # hours

    def __get_dev_machine_operational_energy(self):
        # Operational Energy Calculation (Developer Machines)

        # Operational Energy (kWh) = (Power in Watts * Hours of Use) / 1000
        return self.__estimate_developer_device_power() * self.__get_developer_allocation() / 1000.0 #  kWh

    def __get_dev_machine_predicted_grid_intensity(self):
        # Predicted Grid Intensity (Developer Machines)

        """
        The global average carbon intensity of electricity was 435 gCO₂/kWh in 2025 and the annual
        decline rate is 3.7% (IEA Electricity 2026, https://www.iea.org/reports/electricity-2026)

        """

        BASE_INTENSITY = 435 # gCO2eq per kWh
        ANNUAL_DECLINE_RATE = 0.037  # 3.7%
        BASE_YEAR = 2025

        dev_machine_predicted_grid_intensity = BASE_INTENSITY

        if self.current_year > BASE_YEAR:
            years_ahead = self.current_year - BASE_YEAR

            # Predicted Grid Intensity = Base Intensity * (1 - Annual Decline Rate) ^ Years Ahead
            dev_machine_predicted_grid_intensity = BASE_INTENSITY * ((1 - ANNUAL_DECLINE_RATE) ** years_ahead)

        return dev_machine_predicted_grid_intensity

    def __get_dev_machine_embodied_carbon(self):
        # Embodied Carbon Calculation (Developer Machines)

        """
        4-year (35,040 hours) lifetime was assumed for both laptop and desktop
        developer machines, consistent with standard corporate IT replacement
        cycles (Ferreira & Domingos, 2025), https://doi.org/10.3390/su17104455.

        """
        DEVICE_LIFETIME_HOURS = 35_040 # hours

        """
        Embodied carbon values used: 218.7 kg CO₂eq per laptop and 113.2 kg CO₂eq (desktop tower) + 400.2 kg CO₂eq (monitor)
        per desktop setup (Ferreira & Domingos, 2025), https://doi.org/10.3390/su17104455..
        """
        DEVICE_EMBODIED_CARBON_LAPTOP = 218_700 # gCO2eq
        DEVICE_EMBODIED_CARBON_DESKTOP = 113_200 + 400_200 # gCO2eq

        # Weighted Average Embodied Carbon = (LAPTOP_PERCENT * DEVICE_EMBODIED_CARBON_LAPTOP) + (DESKTOP_PERCENT * DEVICE_EMBODIED_CARBON_DESKTOP)
        weighted_avg_embodied_carbon = DEVICE_EMBODIED_CARBON_LAPTOP * self.LAPTOP_PERCENT + DEVICE_EMBODIED_CARBON_DESKTOP * self.DESKTOP_PERCENT


        # Embodied Carbon (gCO2eq) = (DEVICE Embodied Carbon / Device Lifetime Hours) * Developer Allocation
        dev_machine_embodied_carbon = (weighted_avg_embodied_carbon / DEVICE_LIFETIME_HOURS) * self.__get_developer_allocation() # gCO2eq
        return dev_machine_embodied_carbon

    def calculate_developer_machine_emissions(self):
        #  Carbon emissions from electricity usage and hardware while writing code and running local tests

        return self.__get_dev_machine_operational_energy() * self.__get_dev_machine_predicted_grid_intensity() + self.__get_dev_machine_embodied_carbon()

    def __get_ci_cd_run_allocation(self):
        return self.total_ci_duration_minutes/60.0 # hours

    def __get_ci_cd_predicted_grid_intensity(self):
        # Predicted Grid Intensity (CI/CD Server)

        """
        The United States (GitHub is hosted in Azure US East / Northern Virginia) average carbon
        intensity of electricity was 390 gCO₂/kWh (≈ 380–410 gCO₂/kWh) in 2025 and the annual
        decline rate is 3.2% (IEA Electricity 2026, https://www.iea.org/reports/electricity-2026)
        """

        CI_BASE_INTENSITY = 390 # gCO2eq per kWh
        CI_ANNUAL_DECLINE_RATE = 0.032  # 3.2%
        CI_BASE_YEAR = 2025

        ci_server_predicted_grid_intensity = CI_BASE_INTENSITY

        if self.current_year > CI_BASE_YEAR:
            years_ahead = self.current_year - CI_BASE_YEAR

            # Predicted Grid Intensity = Base Intensity * (1 - Annual Decline Rate) ^ Years Ahead
            ci_server_predicted_grid_intensity = CI_BASE_INTENSITY * ((1 - CI_ANNUAL_DECLINE_RATE) ** years_ahead)

        return ci_server_predicted_grid_intensity

    def __get_ci_cd_operational_energy(self):
        # Operational Energy Calculation (CI/CD Server)

        """
        GitHub is hosted in Microsoft Azure data centers primarily in Northern Virginia (US East),
        with PUE ≈1.16 (Microsoft Sustainability Report, FY25), https://datacenters.microsoft.com/sustainability/efficiency/
        """
        CI_PUE = 1.16

        """
        The power consumption is estimated at 7.5 Watts for a standard 2 vCPU GitHub Actions runner
        based on Cloud Carbon Footprint methodology (Min: 1.56 W, Max: 7.52 W), using a near-max value for bursty
        CI/CD workloads (Cloud Carbon Footprint Official Methodology), https://www.cloudcarbonfootprint.org/docs/methodology/.
        """
        CI_CPU_POWER = 7.5 # Watts

        # Operational Energy (kWh) = CI/CD Run Allocation (hours) * CPU Power (Watts) * PUE / 1000
        return self.__get_ci_cd_run_allocation() * CI_CPU_POWER * CI_PUE / 1000.0  # kWh

    def __get_ci_cd_embodied_carbon(self):
        # Embodied Carbon Calculation (CI/CD Server)

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

        # Embodied Carbon (gCO2eq) = (Server Embodied Carbon / Server Lifetime Hours) * (Core Share / Total Cores) * CI/CD Run Allocation
        return (SERVER_EMBODIED_CARBON / SERVER_LIFETIME_HOURS) * (CI_CORE_SHARE/CI_TOTAL_CORES) * self.__get_ci_cd_run_allocation()

    def _calculate_ci_cd_emissions(self):
        # Carbon Emissions from CI/CD Server

        # Total Carbon Emissions = Operational Energy (E) * Grid Intensity (I) + Embodied Carbon (M)
        return self.__get_ci_cd_operational_energy() * self.__get_ci_cd_predicted_grid_intensity() + self.__get_ci_cd_embodied_carbon() # Total Carbon Emissions (gCO2eq)


    def calculate_data_transfer_emissions(self):
        # Carbon Emissions from Data Transfer

        """
        The open-source Cloud Carbon Footprint methodology used for AWS, GCP, and Azure sets a
        default coefficient of 0.001 kWh/GB for network data transfer,https://www.cloudcarbonfootprint.org/docs/methodology/
        """
        ELECTRICITY_PER_GB = 0.001 # kWh per GB (conservative estimate for data transfer energy consumption)


        """
        eq adapted from https://arxiv.org/html/2510.26413v1 on estimating the environmental impact of CI/CD pipelines through total network data transfer.
        """

        OTHER_NETWORK_DATA = 0.15

        # Data Transfer (GB) = ( Repo Size + Dependency Size + Docker Image Size + Artifact Size + Other Network Data ) * Total CI/CD Runs
        total_data_transfer_gb = ((self.repo_size_gb + self.dependency_size_gb + self.docker_image_size_gb + self.ARTIFACT_SIZE + OTHER_NETWORK_DATA ) * self.total_ci_runs)

        # Data Transfer Energy = Data Transfer (GB) * Electricity per GB (kWh)
        data_transfer_energy = total_data_transfer_gb * ELECTRICITY_PER_GB

        # Total Carbon Emissions (gCO2eq) = Data Transfer Energy (E) * Grid Intensity (I)
        return data_transfer_energy * self.__get_ci_cd_predicted_grid_intensity()

    def calculate_emissions(self):
        developer_machines_carbon_emissions_kgCO2eq = self.calculate_developer_machine_emissions()/1000 # kgCO2eq
        ci_server_carbon_emissions_kgCO2eq = self._calculate_ci_cd_emissions()/1000 # kgCO2eq
        data_transfer_carbon_emissions_kgCO2eq = self.calculate_data_transfer_emissions()/1000 # kgCO2eq

        dev_phase_total_carbon_emissions_kgCO2eq = (developer_machines_carbon_emissions_kgCO2eq + ci_server_carbon_emissions_kgCO2eq + data_transfer_carbon_emissions_kgCO2eq) # (kgCO2eq)

        # Carbon Emmisions per Functional unit (S) = Total Carbon Emmisions (E*I+M) / Funtional unit (R)
        carbon_emissions_per_month_kgCO2eq = dev_phase_total_carbon_emissions_kgCO2eq / self.months # Total Carbon Emissions (kgCO2eq/month)

        return {
            "dev_machines_kgCO2eq": developer_machines_carbon_emissions_kgCO2eq,
            "ci_cd_servers_kgCO2eq": ci_server_carbon_emissions_kgCO2eq,
            "data_transfer_kgCO2eq": data_transfer_carbon_emissions_kgCO2eq,
            "total_emissions_kgCO2eq": dev_phase_total_carbon_emissions_kgCO2eq,
            "emissions_per_month_kgCO2eq": carbon_emissions_per_month_kgCO2eq
        }

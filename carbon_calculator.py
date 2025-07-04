"""
Carbon footprint calculation logic with realistic emission factors
"""

class CarbonCalculator:
    def __init__(self):
        # Emission factors (tonnes CO₂ per unit)
        self.emission_factors = {
            # Flights (tonnes CO₂ per flight)
            'flight_short': 0.3,  # Short flights < 3 hours
            'flight_long': 1.5,   # Long flights > 3 hours
            
            # Transportation (kg CO₂ per km per day * 365 days / 1000)
            'transport': {
                'Walking/Cycling': 0.0,
                'Public Transport': 0.04,  # 40g CO₂ per km
                'Car (Petrol)': 0.18,      # 180g CO₂ per km
                'Car (Diesel)': 0.16,      # 160g CO₂ per km
                'Car (Electric)': 0.05,    # 50g CO₂ per km (including electricity generation)
                'Motorcycle': 0.12         # 120g CO₂ per km
            },
            
            # Diet (tonnes CO₂ per year based on frequency)
            'meat': {
                'Never': 0.0,
                '1-2 times per month': 0.3,
                '1-2 times per week': 0.8,
                '3-4 times per week': 1.5,
                'Daily': 2.5
            },
            
            'dairy': {
                'Never': 0.0,
                'Rarely': 0.1,
                'Sometimes': 0.3,
                'Regularly': 0.6,
                'Daily': 1.0
            },
            
            # Shopping (kg CO₂ per £ spent * 12 months / 1000)
            'clothing_factor': 0.025,    # 25kg CO₂ per £100 spent
            'shopping_factor': 0.015,    # 15kg CO₂ per £100 spent
            
            # Home energy (tonnes CO₂ per year based on home size and heating)
            'home_base': {
                'Apartment/Flat': 1.5,
                'Small House': 2.5,
                'Medium House': 3.5,
                'Large House': 5.0
            },
            
            'heating_multiplier': {
                'Gas Boiler': 1.0,
                'Electric Heating': 1.2,
                'Heat Pump': 0.4,
                'Oil Heating': 1.3,
                'Wood/Biomass': 0.1
            }
        }
    
    def calculate_emissions(self, lifestyle_data):
        """
        Calculate total carbon emissions based on lifestyle data
        
        Args:
            lifestyle_data (dict): Dictionary containing user inputs
            
        Returns:
            dict: Results containing total emissions and breakdown by category
        """
        
        emissions = {
            'travel': 0.0,
            'transport': 0.0,
            'diet': 0.0,
            'shopping': 0.0,
            'home_energy': 0.0
        }
        
        # Calculate travel emissions
        emissions['travel'] += lifestyle_data['flights_short'] * self.emission_factors['flight_short']
        emissions['travel'] += lifestyle_data['flights_long'] * self.emission_factors['flight_long']
        
        # Calculate daily transport emissions (convert to annual)
        transport_type = lifestyle_data['transport_type']
        daily_distance = lifestyle_data['daily_distance']
        
        if transport_type in self.emission_factors['transport']:
            daily_emissions = daily_distance * self.emission_factors['transport'][transport_type]
            emissions['transport'] = daily_emissions * 365 / 1000  # Convert to tonnes
        
        # Calculate diet emissions
        meat_freq = lifestyle_data['meat_frequency']
        dairy_freq = lifestyle_data['dairy_frequency']
        
        emissions['diet'] += self.emission_factors['meat'].get(meat_freq, 0)
        emissions['diet'] += self.emission_factors['dairy'].get(dairy_freq, 0)
        
        # Calculate shopping emissions (convert monthly to annual)
        clothing_annual = lifestyle_data['clothing_spend'] * 12
        shopping_annual = lifestyle_data['online_shopping'] * 12
        
        emissions['shopping'] += clothing_annual * self.emission_factors['clothing_factor']
        emissions['shopping'] += shopping_annual * self.emission_factors['shopping_factor']
        
        # Calculate home energy emissions
        home_type = lifestyle_data['home_type']
        heating_type = lifestyle_data['heating_type']
        
        base_emissions = self.emission_factors['home_base'].get(home_type, 2.5)
        heating_multiplier = self.emission_factors['heating_multiplier'].get(heating_type, 1.0)
        
        emissions['home_energy'] = base_emissions * heating_multiplier
        
        # Calculate total
        total_emissions = sum(emissions.values())
        
        # Round values for display
        breakdown = {k: round(v, 2) for k, v in emissions.items()}
        total_emissions = round(total_emissions, 2)
        
        return {
            'total_emissions': total_emissions,
            'breakdown': breakdown,
            'lifestyle_data': lifestyle_data
        }
    
    def get_category_insights(self, breakdown, total_emissions):
        """
        Generate insights about emission categories
        
        Args:
            breakdown (dict): Emissions breakdown by category
            total_emissions (float): Total emissions
            
        Returns:
            dict: Insights for each category
        """
        insights = {}
        
        for category, emissions in breakdown.items():
            percentage = (emissions / total_emissions) * 100 if total_emissions > 0 else 0
            
            if percentage > 40:
                level = "Very High"
            elif percentage > 25:
                level = "High"
            elif percentage > 15:
                level = "Medium"
            elif percentage > 5:
                level = "Low"
            else:
                level = "Very Low"
            
            insights[category] = {
                'emissions': emissions,
                'percentage': round(percentage, 1),
                'level': level
            }
        
        return insights

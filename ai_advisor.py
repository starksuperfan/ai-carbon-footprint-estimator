"""
AI-powered carbon footprint advice generator using OpenAI
"""

import os
import json
from openai import OpenAI

class AIAdvisor:
    def __init__(self):
        # Get API key from environment variables
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
        
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"
    
    def get_recommendations(self, results):
        """
        Generate personalized recommendations based on carbon footprint results
        
        Args:
            results (dict): Carbon footprint calculation results
            
        Returns:
            list: List of recommendation dictionaries
        """
        
        try:
            # Prepare the prompt with user data
            prompt = self._create_prompt(results)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful environmental advisor. Provide practical, "
                        "non-judgmental advice for reducing carbon footprint. Always respond with "
                        "valid JSON containing an array of recommendations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
                max_tokens=1500
            )
            
            # Parse the response
            response_content = response.choices[0].message.content
            recommendations_data = json.loads(response_content)
            
            # Extract recommendations from the response
            if 'recommendations' in recommendations_data:
                return recommendations_data['recommendations']
            else:
                return []
                
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return self._get_fallback_recommendations(results)
        except Exception as e:
            print(f"API error: {e}")
            return self._get_fallback_recommendations(results)
    
    def _create_prompt(self, results):
        """Create a detailed prompt for the AI advisor"""
        
        total_emissions = results['total_emissions']
        breakdown = results['breakdown']
        lifestyle_data = results['lifestyle_data']
        
        # Find the highest emission categories
        sorted_categories = sorted(breakdown.items(), key=lambda x: x[1], reverse=True)
        top_categories = [cat for cat, emissions in sorted_categories if emissions > 0][:3]
        
        prompt = f"""
        A user has calculated their annual carbon footprint with the following results:
        
        TOTAL EMISSIONS: {total_emissions} tonnes CO₂ per year
        
        BREAKDOWN BY CATEGORY:
        - Travel (flights): {breakdown['travel']} tonnes CO₂
        - Daily Transport: {breakdown['transport']} tonnes CO₂  
        - Diet: {breakdown['diet']} tonnes CO₂
        - Shopping: {breakdown['shopping']} tonnes CO₂
        - Home Energy: {breakdown['home_energy']} tonnes CO₂
        
        KEY LIFESTYLE DETAILS:
        - Short flights per year: {lifestyle_data['flights_short']}
        - Long flights per year: {lifestyle_data['flights_long']}
        - Primary transport: {lifestyle_data['transport_type']}
        - Daily driving distance: {lifestyle_data['daily_distance']} km
        - Red meat frequency: {lifestyle_data['meat_frequency']}
        - Dairy frequency: {lifestyle_data['dairy_frequency']}
        - Monthly clothing spend: £{lifestyle_data['clothing_spend']}
        - Monthly online shopping: £{lifestyle_data['online_shopping']}
        - Home type: {lifestyle_data['home_type']}
        - Heating type: {lifestyle_data['heating_type']}
        
        Please provide exactly 3 personalized, practical recommendations to help reduce their carbon footprint.
        Focus on the highest-impact categories: {', '.join(top_categories[:3])}.
        
        Make the advice:
        1. Specific and actionable
        2. Non-judgmental and encouraging
        3. Realistic for their lifestyle
        4. Include estimated CO₂ savings where possible
        
        Respond in JSON format:
        {{
            "recommendations": [
                {{
                    "title": "Short, clear title",
                    "description": "Detailed explanation with specific actions",
                    "potential_savings": "X.X tonnes CO₂ per year"
                }}
            ]
        }}
        """
        
        return prompt
    
    def _get_fallback_recommendations(self, results):
        """
        Provide fallback recommendations when AI is unavailable
        """
        
        breakdown = results['breakdown']
        lifestyle_data = results['lifestyle_data']
        recommendations = []
        
        # Generate basic recommendations based on highest emissions
        sorted_categories = sorted(breakdown.items(), key=lambda x: x[1], reverse=True)
        
        for category, emissions in sorted_categories[:3]:
            if emissions > 0:
                rec = self._get_category_recommendation(category, emissions, lifestyle_data)
                if rec:
                    recommendations.append(rec)
        
        return recommendations[:3]
    
    def _get_category_recommendation(self, category, emissions, lifestyle_data):
        """Generate basic recommendation for a specific category"""
        
        recommendations_map = {
            'travel': {
                'title': 'Reduce Flight Emissions',
                'description': 'Consider reducing the number of flights per year, choosing direct routes when possible, and exploring train alternatives for shorter distances. Video conferencing can replace some business travel.',
                'potential_savings': f'{emissions * 0.3:.1f} tonnes CO₂ per year'
            },
            'transport': {
                'title': 'Optimize Daily Transportation',
                'description': 'Consider walking, cycling, or using public transport more often. If driving is necessary, consider carpooling, combining trips, or switching to an electric vehicle.',
                'potential_savings': f'{emissions * 0.4:.1f} tonnes CO₂ per year'
            },
            'diet': {
                'title': 'Adjust Your Diet',
                'description': 'Reducing red meat consumption and choosing more plant-based meals can significantly lower your carbon footprint. Try "Meatless Monday" or explore delicious vegetarian recipes.',
                'potential_savings': f'{emissions * 0.5:.1f} tonnes CO₂ per year'
            },
            'shopping': {
                'title': 'Mindful Shopping Habits',
                'description': 'Buy less, choose quality over quantity, shop second-hand when possible, and avoid impulse purchases. Consider the lifecycle of products before buying.',
                'potential_savings': f'{emissions * 0.3:.1f} tonnes CO₂ per year'
            },
            'home_energy': {
                'title': 'Improve Home Energy Efficiency',
                'description': 'Improve insulation, use energy-efficient appliances, lower heating temperatures by 1-2°C, and consider renewable energy options like solar panels or green energy suppliers.',
                'potential_savings': f'{emissions * 0.25:.1f} tonnes CO₂ per year'
            }
        }
        
        return recommendations_map.get(category)

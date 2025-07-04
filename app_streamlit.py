import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from carbon_calculator import CarbonCalculator
from ai_advisor import AIAdvisor

# Initialize session state
if 'calculated' not in st.session_state:
    st.session_state.calculated = False
if 'results' not in st.session_state:
    st.session_state.results = None

def reset_app():
    """Reset the application state"""
    st.session_state.calculated = False
    st.session_state.results = None
    st.rerun()

def main():
    st.set_page_config(
        page_title="🌱 AI Carbon Footprint Estimator",
        page_icon="🌱",
        layout="wide"
    )
    
    st.title("🌱 AI Carbon Footprint Estimator")
    st.markdown("---")
    
    if not st.session_state.calculated:
        show_questionnaire()
    else:
        show_results()

def show_questionnaire():
    """Display the questionnaire form"""
    st.markdown("### Tell us about your lifestyle")
    st.markdown("Answer a few simple questions to estimate your annual carbon footprint.")
    
    with st.form("carbon_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("✈️ Travel")
            flights_short = st.number_input(
                "Number of short flights (< 3 hours) in the past year:",
                min_value=0,
                max_value=50,
                value=0,
                help="Domestic or short international flights"
            )
            
            flights_long = st.number_input(
                "Number of long flights (> 3 hours) in the past year:",
                min_value=0,
                max_value=20,
                value=0,
                help="Long-haul international flights"
            )
            
            st.subheader("🚗 Transportation")
            transport_type = st.selectbox(
                "Primary mode of daily transportation:",
                ["Walking/Cycling", "Public Transport", "Car (Petrol)", "Car (Diesel)", "Car (Electric)", "Motorcycle"]
            )
            
            if transport_type in ["Car (Petrol)", "Car (Diesel)", "Car (Electric)", "Motorcycle"]:
                daily_distance = st.slider(
                    "Average daily driving distance (km):",
                    min_value=0,
                    max_value=200,
                    value=20,
                    help="Total kilometers driven per day"
                )
            else:
                daily_distance = 0
        
        with col2:
            st.subheader("🥩 Diet")
            meat_frequency = st.selectbox(
                "How often do you eat red meat (beef, lamb, pork)?",
                ["Never", "1-2 times per month", "1-2 times per week", "3-4 times per week", "Daily"]
            )
            
            dairy_frequency = st.selectbox(
                "How often do you consume dairy products?",
                ["Never", "Rarely", "Sometimes", "Regularly", "Daily"]
            )
            
            st.subheader("🛍️ Shopping & Consumption")
            clothing_spend = st.slider(
                "Monthly spending on clothing and fashion (£):",
                min_value=0,
                max_value=1000,
                value=50,
                help="Average amount spent on new clothes per month"
            )
            
            online_shopping = st.slider(
                "Monthly spending on online shopping/deliveries (£):",
                min_value=0,
                max_value=2000,
                value=100,
                help="Electronics, household items, etc."
            )
            
            st.subheader("🏠 Home Energy")
            home_type = st.selectbox(
                "Type of home:",
                ["Apartment/Flat", "Small House", "Medium House", "Large House"]
            )
            
            heating_type = st.selectbox(
                "Primary heating source:",
                ["Gas Boiler", "Electric Heating", "Heat Pump", "Oil Heating", "Wood/Biomass"]
            )
        
        submitted = st.form_submit_button("Calculate My Carbon Footprint", type="primary")
        
        if submitted:
            try:
                with st.spinner("Calculating your carbon footprint..."):
                    # Create calculator instance
                    calculator = CarbonCalculator()
                    
                    # Prepare input data
                    lifestyle_data = {
                        'flights_short': flights_short,
                        'flights_long': flights_long,
                        'transport_type': transport_type,
                        'daily_distance': daily_distance,
                        'meat_frequency': meat_frequency,
                        'dairy_frequency': dairy_frequency,
                        'clothing_spend': clothing_spend,
                        'online_shopping': online_shopping,
                        'home_type': home_type,
                        'heating_type': heating_type
                    }
                    
                    # Calculate emissions
                    results = calculator.calculate_emissions(lifestyle_data)
                    
                    # Store results in session state
                    st.session_state.results = results
                    st.session_state.calculated = True
                    
                    st.rerun()
                    
            except Exception as e:
                st.error(f"Error calculating emissions: {str(e)}")

def show_results():
    """Display the calculation results and AI recommendations"""
    results = st.session_state.results
    
    st.markdown("### 📊 Your Carbon Footprint Results")
    
    # Total emissions display
    total_emissions = results['total_emissions']
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Annual Emissions",
            f"{total_emissions:.1f} tonnes CO₂",
            help="Your estimated annual carbon footprint"
        )
    
    with col2:
        uk_average = 8.5  # UK average carbon footprint
        difference = total_emissions - uk_average
        st.metric(
            "vs UK Average",
            f"{uk_average} tonnes CO₂",
            f"{difference:+.1f} tonnes",
            help="Comparison with UK national average"
        )
    
    with col3:
        global_average = 4.8  # Global average carbon footprint
        difference_global = total_emissions - global_average
        st.metric(
            "vs Global Average",
            f"{global_average} tonnes CO₂",
            f"{difference_global:+.1f} tonnes",
            help="Comparison with global average"
        )
    
    # Emissions breakdown chart
    st.markdown("### 📈 Emissions Breakdown")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart
        categories = list(results['breakdown'].keys())
        values = list(results['breakdown'].values())
        
        fig_pie = px.pie(
            values=values,
            names=categories,
            title="Emissions by Category",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Bar chart
        fig_bar = px.bar(
            x=categories,
            y=values,
            title="Emissions by Category (tonnes CO₂)",
            color=categories,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_bar.update_layout(showlegend=False)
        fig_bar.update_xaxes(title="Category")
        fig_bar.update_yaxes(title="Emissions (tonnes CO₂)")
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # AI-powered recommendations
    st.markdown("### 🤖 AI-Powered Recommendations")
    
    try:
        with st.spinner("Generating personalized recommendations..."):
            advisor = AIAdvisor()
            recommendations = advisor.get_recommendations(results)
            
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                    with st.expander(f"💡 Recommendation {i}: {rec['title']}", expanded=i==1):
                        st.write(rec['description'])
                        if 'potential_savings' in rec:
                            st.info(f"**Potential CO₂ savings:** {rec['potential_savings']}")
            else:
                st.warning("Unable to generate AI recommendations at this time.")
                
    except Exception as e:
        st.error(f"AI recommendations unavailable: {str(e)}")
        st.info("You can still see your carbon footprint breakdown above!")
    
    # Action buttons
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Calculate Again", type="primary"):
            reset_app()
    
    with col2:
        # Export data button
        export_data = {
            'Total Emissions (tonnes CO₂)': total_emissions,
            **{f"{k} (tonnes CO₂)": v for k, v in results['breakdown'].items()}
        }
        
        df_export = pd.DataFrame([export_data])
        csv = df_export.to_csv(index=False)
        
        st.download_button(
            label="📄 Download Results (CSV)",
            data=csv,
            file_name="carbon_footprint_results.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()

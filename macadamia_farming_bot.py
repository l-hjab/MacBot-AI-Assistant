"""
Macadamia Farming AI Chatbot - Streamlit Interface
==================================================

A comprehensive AI-powered chatbot for macadamia farmers providing advice on
planting, pest management, fertilization, harvesting, and organic certification.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from typing import Dict, Any, List
from dotenv import load_dotenv


load_dotenv()


# Import our chatbot components
try:
    from macadamia_bot.core.chatbot import MacadamiaBot
    from macadamia_bot.models.model_trainer import MacadamiaModelTrainer
except ImportError as e:
    st.error(f"Error importing chatbot modules: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="🥜 Macadamia Farming AI Assistant",
    page_icon="🥜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #E3F2FD;
        border-left: 4px solid #2196F3;
        color:#000000;
    }
    .bot-message {
        background-color: #F1F8E9;
        color:#000000;
        border-left: 4px solid #4CAF50;
    }
    .metric-card {
        background-color: #FAFAFA;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #E0E0E0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'farm_data' not in st.session_state:
    st.session_state.farm_data = {}
if 'models_trained' not in st.session_state:
    st.session_state.models_trained = False

def initialize_chatbot():
    """Initialize the chatbot with API key"""
    try:
        api_key = os.getenv("TOGETHER_API_KEY", "")
        if not api_key:
            st.warning("⚠️ No API key found. Some features may be limited. Set TOGETHER_API_KEY environment variable.")
        
        chatbot = MacadamiaBot(api_key=api_key)
        st.session_state.chatbot = chatbot
        return True
    except Exception as e:
        st.error(f"Failed to initialize chatbot: {e}")
        return False

def display_header():
    """Display the main header"""
    st.markdown('<h1 class="main-header"> Macadamia Farming AI Assistant</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p style="font-size: 1.2rem; color: #666;">
            Your MacBot for organic macadamia farming advice
        </p>
    </div>
    """, unsafe_allow_html=True)

def setup_sidebar():
    """Setup the sidebar with farm data input and controls"""
    st.sidebar.header("Farm Details")
    
    # Farm data input
    with st.sidebar.expander("Enter Your Farm Data", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            soil_ph = st.number_input("Soil pH", min_value=4.0, max_value=8.0, value=6.2, step=0.1)
            temperature = st.number_input("Temperature (°C)", min_value=0, max_value=50, value=24)
            humidity = st.number_input("Humidity (%)", min_value=0, max_value=100, value=65)
        
        with col2:
            rainfall = st.number_input("Recent Rainfall (mm)", min_value=0, max_value=500, value=120)
            tree_age = st.number_input("Tree Age (years)", min_value=1, max_value=50, value=5)
            season = st.selectbox("Current Season", ["spring", "summer", "autumn", "winter"])
        
        # Optional farm details
        # st.subheader("Optional Details")
        # farm_location = st.text_input("Farm Location", placeholder="e.g., Queensland, Australia")
        # orchard_size = st.number_input("Orchard Size (hectares)", min_value=0.1, max_value=1000.0, value=5.0)
        # varieties = st.multiselect("Macadamia Varieties", 
        #                          ["Beaumont", "A4", "A16", "A38", "Own Venture", "Daddow"],
        #                          default=["Beaumont"])
        
        # Update session state
        st.session_state.farm_data = {
            'soil_ph': soil_ph,
            'temperature': temperature,
            'humidity': humidity,
            'rainfall': rainfall,
            'tree_age': tree_age,
            'season': season,
            # 'farm_location': farm_location,
            # 'orchard_size': orchard_size,
            # 'varieties': varieties
        }
    
    # Model training section
    st.sidebar.header("🤖 AI Models")
    if st.sidebar.button("Train/Update Models"):
        with st.sidebar.spinner("Training models..."):
            try:
                trainer = MacadamiaModelTrainer()
                results = trainer.train_all_models()
                st.session_state.models_trained = True
                st.sidebar.success("✅ Models trained successfully!")
                
                # Display training results
                with st.sidebar.expander("Training Results"):
                    for model_name, metrics in results.items():
                        if 'test_accuracy' in metrics:
                            st.write(f"**{model_name}**: {metrics['test_accuracy']:.3f} accuracy")
                        elif 'test_r2' in metrics:
                            st.write(f"**{model_name}**: {metrics['test_r2']:.3f} R²")
            except Exception as e:
                st.sidebar.error(f"Model training failed: {e}")
    
    # Quick actions
    st.sidebar.header("Quick Actions")
    if st.sidebar.button("🔍 Analyze Current Conditions"):
        if st.session_state.chatbot:
            response = st.session_state.chatbot.chat(
                "Analyze my current farm conditions and provide recommendations",
                farm_data=st.session_state.farm_data
            )
            st.session_state.conversation_history.append({
                'user': "Analyze my current farm conditions",
                'bot': response['final_response'],
                'timestamp': datetime.now()
            })
    
    # if st.sidebar.button("📅 Seasonal Advice"):
    #     if st.session_state.chatbot:
    #         season = st.session_state.farm_data.get('season', 'spring')
    #         response = st.session_state.chatbot.chat(
    #             f"What should I focus on during {season} season?",
    #             farm_data=st.session_state.farm_data
    #         )
    #         st.session_state.conversation_history.append({
    #             'user': f"Seasonal advice for {season}",
    #             'bot': response['final_response'],
    #             'timestamp': datetime.now()
    #         })

def display_farm_dashboard():
    """Display farm condition dashboard"""
    st.header("📊 Farm Conditions Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Soil pH", f"{st.session_state.farm_data.get('soil_ph', 6.2):.1f}", 
                 delta="Optimal" if 6.0 <= st.session_state.farm_data.get('soil_ph', 6.2) <= 6.5 else "Check")
    
    with col2:
        temp = st.session_state.farm_data.get('temperature', 24)
        st.metric("Temperature", f"{temp}°C", 
                 delta="Good" if 18 <= temp <= 25 else "Monitor")
    
    with col3:
        humidity = st.session_state.farm_data.get('humidity', 65)
        st.metric("Humidity", f"{humidity}%", 
                 delta="Optimal" if 60 <= humidity <= 80 else "Watch")
    
    with col4:
        rainfall = st.session_state.farm_data.get('rainfall', 120)
        st.metric("Rainfall", f"{rainfall}mm", 
                 delta="Good" if 100 <= rainfall <= 200 else "Monitor")
    
    # Visualization
    if st.session_state.farm_data:
        col1, col2 = st.columns(2)
        
        with col1:
            # Radar chart for farm conditions
            categories = ['Soil pH', 'Temperature', 'Humidity', 'Rainfall']
            values = [
                (st.session_state.farm_data.get('soil_ph', 6.2) - 5.0) / 2.5 * 100,  # Normalize pH
                st.session_state.farm_data.get('temperature', 24) / 35 * 100,  # Normalize temp
                st.session_state.farm_data.get('humidity', 65),  # Already percentage
                min(st.session_state.farm_data.get('rainfall', 120) / 200 * 100, 100)  # Normalize rainfall
            ]
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='Current Conditions'
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=True,
                title="Farm Conditions Overview"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Tree age and variety info
            st.subheader("🌳 Orchard Information")
            tree_age = st.session_state.farm_data.get('tree_age', 5)
            
            if tree_age <= 3:
                stage = "Young Trees"
                color = "#FFA726"
            elif tree_age <= 7:
                stage = "Maturing Trees"
                color = "#66BB6A"
            else:
                stage = "Mature Trees"
                color = "#2E7D32"
            
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: {color};">{stage}</h4>
                <p><strong>Age:</strong> {tree_age} years</p>
                <p><strong>Size:</strong> {st.session_state.farm_data.get('orchard_size', 5)} hectares</p>
                <p><strong>Varieties:</strong> {', '.join(st.session_state.farm_data.get('varieties', ['Beaumont']))}</p>
            </div>
            """, unsafe_allow_html=True)

def display_chat_interface():
    # """Display the main chat interface"""
    # st.header(" Chat with Your Farming Assistant")
    
    # Initialize chatbot if not already done
    if st.session_state.chatbot is None:
        if not initialize_chatbot():
            st.error("Failed to initialize chatbot. Please check your setup.")
            return
    
    # Display conversation history
    chat_container = st.container()
    
    with chat_container:
        for i, message in enumerate(st.session_state.conversation_history):
            # User message
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong> You:</strong> {message['user']}
                <small style="float: right; color: #666;">
                    {message['timestamp'].strftime('%H:%M')}
                </small>
            </div>
            """, unsafe_allow_html=True)
            
            # Bot response
            st.markdown(f"""
            <div class="chat-message bot-message">
                <strong>🤖 Assistant:</strong><br>
                {message['bot'].replace('\n', '<br>')}
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    st.markdown("---")
    
    # Quick question buttons
    st.subheader(" Quick Questions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🌱 Planting Advice"):
            user_input = "I need advice on planting macadamia trees"
    
    with col2:
        if st.button("🐛 Pest Management"):
            user_input = "How do I manage pests organically?"
    
    with col3:
        if st.button("🌿 Fertilization"):
            user_input = "What fertilizers should I use?"
    
    with col4:
        if st.button("🥜 Harvesting"):
            user_input = "When and how should I harvest?"
    
    # Text input for custom questions
    user_input = st.text_input("Ask your farming question:", 
                              placeholder="e.g., When should I plant macadamia trees?",
                              key="user_input")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        send_button = st.button("Send 📤", type="primary")
    
    # Process user input
    if send_button and user_input:
        with st.spinner("🤔 Thinking..."):
            try:
                response = st.session_state.chatbot.chat(
                    user_input,
                    farm_data=st.session_state.farm_data
                )
                
                # Add to conversation history
                st.session_state.conversation_history.append({
                    'user': user_input,
                    'bot': response['final_response'],
                    'timestamp': datetime.now()
                })
                
                # Clear input and rerun to show new message
                st.rerun()
                
            except Exception as e:
                st.error(f"Error processing your question: {e}")

def display_resources():
    """Display additional resources and information"""
    # st.header(" Farming Resources")
    
    # col1, col2 = st.columns(2)
    
    # with col1:
    #     st.subheader("🌱 Planting Guide")
    #     st.markdown("""
    #     - **Site Selection**: Well-draining soil, pH 6.0-6.5
    #     - **Timing**: Spring (Sep-Nov) or Autumn (Mar-May)
    #     - **Spacing**: 8m x 8m traditional, 6m x 6m intensive
    #     - **Varieties**: Beaumont, A4, A16, A38
    #     """)
        
    #     st.subheader("🐛 Common Pests")
    #     st.markdown("""
    #     - **Nut Borer**: Monitor with pheromone traps
    #     - **Stink Bugs**: Use beneficial predators
    #     - **Scale Insects**: Apply horticultural oil
    #     """)
    
    # with col2:
    #     st.subheader("🌿 Organic Fertilizers")
    #     st.markdown("""
    #     - **Compost**: 10-30kg per tree annually
    #     - **Blood Meal**: Nitrogen source for growth
    #     - **Bone Meal**: Phosphorus for root development
    #     - **Kelp Meal**: Trace elements and hormones
    #     """)
        
    #     st.subheader("🏆 Certification")
    #     st.markdown("""
    #     - **Transition**: 3 years without prohibited substances
    #     - **Records**: Document all inputs and practices
    #     - **Inspection**: Annual on-farm inspections
    #     - **Compliance**: Use only approved organic inputs
    #     """)

def main():
    """Main application function"""
    display_header()
    
    # Setup sidebar
    setup_sidebar()
    
    # Main content tabs
    tab1, tab2 = st.tabs([" Chat Assistant", "Farm Dashboard"])
    
    with tab1:
        display_chat_interface()
    
    with tab2:
        display_farm_dashboard()
    
    # with tab3:
    #     display_resources()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        🥜 Macadamia Farming AI Assistant | Built by Daphine Nekesa for sustainable farming
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()


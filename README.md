# MacBot-AI-Assistant
# 🥜 Macadamia Farming AI Chatbot

An intelligent AI-powered chatbot designed specifically for macadamia farmers, providing comprehensive organic farming advice using Random Forest machine learning models and Llama API for natural language processing.

## 🌟 Features

### 🤖 AI-Powered Advice
- **Random Forest Models**: Trained on macadamia farming data for pest risk prediction, fertilization needs, harvest timing, and yield estimation
- **Llama API Integration**: Natural language processing for conversational farming advice
- **Hybrid Intelligence**: Combines ML predictions with expert knowledge base

### 🌱 Comprehensive Farming Domains
- **Planting**: Site selection, timing, varieties, spacing, and establishment
- **Pest Management**: Organic IPM strategies, pest identification, and treatment recommendations
- **Fertilization**: Organic nutrient management, soil testing, and feeding schedules
- **Harvesting**: Maturity indicators, harvest methods, and post-harvest handling
- **Certification**: Organic certification process, requirements, and compliance

### 💻 User-Friendly Interface
- **Streamlit Web App**: Intuitive chat interface with farm dashboard
- **Mobile Responsive**: Works on desktop, tablet, and mobile devices
- **Visual Analytics**: Farm condition monitoring and prediction visualizations
- **Quick Actions**: Pre-built queries for common farming questions

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Together AI API key (get one at [together.xyz](https://api.together.xyz/))

### Installation

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd macadamia-farming-bot
   python setup_farming_bot.py
   ```

2. **Configure API Key**
   ```bash
   cp .env.example .env
   # Edit .env and add your Together AI API key
   ```

3. **Run the Application**
   ```bash
   streamlit run macadamia_farming_bot.py
   ```

4. **Or Test with Demo**
   ```bash
   python demo_farming_bot.py
   ```

## 📊 How It Works

### 1. Query Classification
The system intelligently classifies user queries to determine the best response approach:
- **Domain Detection**: Identifies farming area (planting, pest, fertilization, etc.)
- **Intent Recognition**: Understands what the user wants (advice, prediction, information)
- **Parameter Extraction**: Pulls relevant details from the query

### 2. Multi-Modal Response Generation
- **ML Predictions**: Uses Random Forest models for data-driven recommendations
- **Knowledge Base**: Accesses comprehensive farming knowledge database
- **Conversational AI**: Generates natural language responses via Llama API

### 3. Contextual Advice
- **Farm-Specific**: Tailors advice based on your farm conditions
- **Seasonal Awareness**: Considers current season and timing
- **Experience Level**: Adapts complexity based on farming experience

## 🎯 Usage Examples

### Basic Chat
```python
from macadamia_bot.core.chatbot import MacadamiaBot

bot = MacadamiaBot(api_key="your_api_key")

# Simple question
response = bot.chat("When should I plant macadamia trees?")
print(response['final_response'])
```

### With Farm Data
```python
farm_data = {
    'soil_ph': 6.2,
    'temperature': 24,
    'humidity': 65,
    'rainfall': 120,
    'season': 'spring',
    'tree_age': 5
}

response = bot.chat("Should I spray for pests?", farm_data=farm_data)
```

### Streamlit Interface
1. Enter your farm conditions in the sidebar
2. Ask questions in the chat interface
3. View predictions and recommendations
4. Monitor farm conditions on the dashboard

## 🧠 Machine Learning Models

### Pest Risk Predictor
- **Input**: Soil pH, temperature, humidity, rainfall, season, tree age
- **Output**: Risk level (very_low to very_high) with specific pest analysis
- **Accuracy**: ~85% on test data

### Fertilizer Need Advisor
- **Input**: Same environmental parameters plus soil conditions
- **Output**: Fertilization recommendations and timing
- **Features**: Organic-focused with seasonal scheduling

### Harvest Timing Predictor
- **Input**: Tree age, variety, environmental conditions
- **Output**: Harvest readiness assessment
- **Integration**: Combined with maturity indicators

### Yield Estimator
- **Input**: Tree age, environmental conditions, management practices
- **Output**: Expected yield per tree
- **Use Case**: Planning and resource allocation

     
## 🔧 Configuration

### Environment Variables (.env)
```bash
# Required
TOGETHER_API_KEY=your_api_key_here


### Configuration File (config/farming_config.yaml)
- Model parameters and hyperparameters
- Farming condition thresholds
- UI settings and themes
- Data paths and model locations

## 🧪 Testing

### Run Tests
```bash
python -m pytest tests/
```

### Manual Testing
```bash
# Test individual components
python demo_farming_bot.py

# Test model training
python -c "from macadamia_bot.models.model_trainer import MacadamiaModelTrainer; MacadamiaModelTrainer().train_all_models()"

# Test chatbot
python -c "from macadamia_bot.core.chatbot import MacadamiaBot; print(MacadamiaBot().chat('Hello'))"
```

## 📱 SMS/WhatsApp Integration (Future)

The current implementation uses Streamlit for the web interface. For SMS/WhatsApp integration, you can:

1. **Twilio Integration**: Use Twilio API for SMS
2. **WhatsApp Business API**: Integrate with WhatsApp Business
3. **Webhook Endpoints**: Create API endpoints for messaging platforms
4. **Message Formatting**: Adapt responses for text-based interfaces

Example webhook structure:
```python
@app.route('/webhook/sms', methods=['POST'])
def handle_sms():
    message = request.form['Body']
    response = bot.chat(message)
    return format_for_sms(response['final_response'])
```

##  Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Format code
black macadamia_bot/
flake8 macadamia_bot/
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Macadamia Farmers**: For domain expertise and feedback
- **Together AI**: For Llama API access
- **Streamlit**: For the excellent web framework
- **Scikit-learn**: For machine learning capabilities
- **Open Source Community**: For the tools and libraries

## 📞 Support

- **Documentation**: Check this README and inline code comments
- **Issues**: Report bugs and feature requests via GitHub issues
- **Discussions**: Join community discussions for farming advice
- **Email**: Contact the development team for enterprise support

## 🔮 Roadmap

### Version 2.0
- [ ] SMS/WhatsApp integration
- [ ] Multi-language support
- [ ] Advanced yield prediction models
- [ ] Weather API integration
- [ ] Farm management dashboard

### Version 3.0
- [ ] Computer vision for pest/disease identification
- [ ] IoT sensor integration
- [ ] Blockchain traceability
- [ ] Market price predictions
- [ ] Community farmer network

---

**Happy Farming! 🌱🥜**

*Built with by Daphine Nekesa sustainable macadamia farming*


# 🪞 MirrorMe - AI Personality Cloning System

> **An innovative AI that learns your personality and communication style over time**

MirrorMe is a cutting-edge personality cloning AI that uses advanced machine learning to analyze your communication patterns and gradually mirror your unique style. Built with modern web technologies and powered by OpenAI's GPT models, it creates a truly personalized AI experience.

## 🌟 Features

### 🧠 **Intelligent Personality Learning**
- **Real-time Analysis**: Continuously analyzes your messages using advanced NLP
- **Big Five Personality Model**: Tracks openness, conscientiousness, extraversion, agreeableness, and neuroticism
- **Communication Style Mapping**: Learns your tone, formality, enthusiasm, and linguistic patterns
- **Semantic Memory**: Uses FAISS vector search to find and reference similar past conversations

### 💬 **Advanced Chat Interface**
- **Adaptive Responses**: AI responses become more like you over time
- **Style Mirroring**: Adopts your favorite phrases, expressions, and communication patterns
- **Context Awareness**: Maintains conversation context and personality consistency
- **Progressive Learning**: 5-stage learning system from basic patterns to advanced mirroring

### 📊 **Comprehensive Analytics**
- **Personality Dashboard**: Visual representation of your personality traits
- **Learning Progress**: Track how well the AI has learned your style
- **Communication Insights**: Detailed analysis of your messaging patterns
- **Word Cloud Visualization**: See your most frequently used words and phrases

### 🎨 **Modern UI/UX**
- **Sleek Design**: Beautiful gradients and smooth animations
- **Responsive Layout**: Works perfectly on desktop and mobile
- **Interactive Elements**: Engaging charts and visualizations
- **Real-time Updates**: Live typing indicators and smooth transitions

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- OpenAI API key
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mirrorme.git
   cd mirrorme
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   ```
   http://localhost:8501
   ```

## 🐳 Docker Deployment

### Simple Deployment
```bash
docker-compose up -d
```

### Production Deployment
```bash
docker-compose --profile production up -d
```

## 🏗️ Architecture

### **Tech Stack**
- **Frontend**: Streamlit with custom CSS animations
- **Backend**: Python with LangChain for AI orchestration
- **AI Models**: OpenAI GPT-3.5-Turbo for language generation
- **Memory System**: FAISS for semantic similarity search
- **Data Analysis**: TextBlob for sentiment analysis
- **Visualizations**: Plotly for interactive charts
- **Deployment**: Docker and Streamlit Cloud support

### **System Components**

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   Streamlit UI      │    │   MirrorAgent       │    │   Memory Manager    │
│   - Chat Interface  │◄──►│   - Response Gen    │◄──►│   - FAISS Store     │
│   - Analytics       │    │   - Style Learning  │    │   - Chat History    │
│   - Visualizations  │    │   - Context Mgmt    │    │   - Personality DB  │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
           │                           │                           │
           └─────────────────────────────────────────────────────────┘
                                       │
                            ┌─────────────────────┐
                            │  Personality        │
                            │  Analyzer           │
                            │  - Trait Extraction │
                            │  - Style Analysis   │
                            │  - Pattern Learning │
                            └─────────────────────┘
```

## 🎯 How It Works

### **Learning Process**

1. **Initial Learning** (0-4 messages)
   - Basic response generation
   - Establishing baseline communication

2. **Basic Patterns** (5-19 messages)
   - Identifying communication patterns
   - Learning basic style elements

3. **Style Recognition** (20-49 messages)
   - Adopting user's style elements
   - Personality trait modeling

4. **Personality Modeling** (50-99 messages)
   - Deep personality integration
   - Advanced pattern recognition

5. **Advanced Mirroring** (100+ messages)
   - Sophisticated style replication
   - Contextual personality adaptation

### **Personality Analysis**

The system analyzes multiple dimensions:

- **Communication Style**: Tone, formality, enthusiasm, sentence structure
- **Personality Traits**: Big Five personality model scoring
- **Interests**: Topics frequently discussed
- **Linguistic Patterns**: Word choice, phrase usage, complexity
- **Emotional Patterns**: Sentiment analysis and mood tracking

## 📈 Analytics Features

### **Personality Dashboard**
- Radar chart of Big Five personality traits
- Communication style breakdown
- Favorite phrases and expressions
- Interest and topic analysis

### **Learning Analytics**
- Progress tracking across learning stages
- Message statistics and patterns
- Word frequency analysis
- Sentiment evolution over time

### **Export Options**
- Complete chat history export
- Personality profile backup
- Analytics data download
- JSON format for portability

## 🔧 Configuration

### **Environment Variables**
```bash
OPENAI_API_KEY=your-api-key-here
```

### **Config Settings**
Edit `config.py` to customize:
- Model parameters (temperature, max tokens)
- Learning frequency and thresholds
- Memory limits and retention
- UI theme and styling

## 🚀 Deployment Options

### **Streamlit Cloud**
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Deploy directly from repository

### **Docker**
```bash
docker build -t mirrorme .
docker run -p 8501:8501 -e OPENAI_API_KEY=your-key mirrorme
```

### **Heroku**
```bash
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your-key
git push heroku main
```

## 🎨 Screenshots

### Chat Interface
![Chat Interface](https://via.placeholder.com/800x600?text=Chat+Interface)

### Personality Dashboard
![Personality Dashboard](https://via.placeholder.com/800x600?text=Personality+Dashboard)

### Learning Analytics
![Learning Analytics](https://via.placeholder.com/800x600?text=Learning+Analytics)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing GPT models
- Streamlit for the amazing web framework
- LangChain for AI orchestration tools
- FAISS for efficient similarity search

## 🔮 Future Enhancements

- [ ] Voice input/output capabilities
- [ ] Multi-language personality analysis
- [ ] Advanced emotion recognition
- [ ] Integration with social media platforms
- [ ] Custom personality templates
- [ ] Team collaboration features

---

**Built with ❤️ by [Your Name]**

*If you find this project helpful, please consider giving it a ⭐ on GitHub!*
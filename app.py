import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import os
from utils.mirror_agent import MirrorAgent
from utils.memory_manager import MemoryManager
from utils.personality_analyzer import PersonalityAnalyzer

# Page configuration
st.set_page_config(
    page_title="🪞 MirrorMe - AI Personality Cloning",
    page_icon="🪞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    with open("assets/mirrorme_theme.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'mirror_agent' not in st.session_state:
        st.session_state.mirror_agent = MirrorAgent()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'typing' not in st.session_state:
        st.session_state.typing = False

# Create animated header
def create_header():
    st.markdown("""
    <div class="main-header">
        <div class="header-content">
            <div class="logo-section">
                <div class="logo-icon">🪞</div>
                <div class="logo-text">
                    <h1>MirrorMe</h1>
                    <p>Advanced AI Personality Cloning System</p>
                </div>
            </div>
            <div class="header-stats">
                <div class="stat-item">
                    <span class="stat-number" id="messages-count">0</span>
                    <span class="stat-label">Messages</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number" id="learning-stage">1</span>
                    <span class="stat-label">Stage</span>
                </div>
            </div>
        </div>
        <div class="header-gradient"></div>
    </div>
    """, unsafe_allow_html=True)

# Create sidebar navigation
def create_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <h2>🎯 Navigation</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation menu
        page = st.selectbox(
            "Choose a page",
            ["💬 Chat", "📊 Dashboard", "📈 Analytics", "⚙️ Settings"],
            key="navigation"
        )
        
        st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
        
        # Quick stats
        st.markdown("""
        <div class="sidebar-section">
            <h3>⚡ Quick Stats</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Get current stats
        progress = st.session_state.mirror_agent.get_learning_progress()
        
        # Stats cards
        create_stat_card("Messages Analyzed", progress.get('messages_analyzed', 0), "💬")
        create_stat_card("Learning Stage", progress.get('learning_stage', 'Initial Learning'), "🎯")
        create_stat_card("Next Update", f"Message {progress.get('next_analysis_at', 5)}", "⏰")
        
        st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
        
        # Action buttons
        if st.button("🔄 Reset Memory", key="reset_btn", help="Clear all chat history and start fresh"):
            st.session_state.mirror_agent.reset_memory()
            st.session_state.chat_history = []
            st.success("Memory reset successfully!")
            st.rerun()
        
        if st.button("📥 Export Data", key="export_btn", help="Download your personality data"):
            data = st.session_state.mirror_agent.export_data()
            st.download_button(
                "💾 Download JSON",
                json.dumps(data, indent=2),
                file_name=f"mirrorme_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    return page

def create_stat_card(label, value, icon):
    st.markdown(f"""
    <div class="sidebar-stat-card">
        <div class="stat-icon">{icon}</div>
        <div class="stat-content">
            <div class="stat-value">{value}</div>
            <div class="stat-label">{label}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Chat page
def chat_page():
    st.markdown("""
    <div class="page-header">
        <h2>💬 Chat with Your AI Mirror</h2>
        <p>Start a conversation and watch as the AI learns your personality!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        for i, message in enumerate(st.session_state.chat_history):
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message" style="animation-delay: {i * 0.1}s">
                    <div class="message-avatar user-avatar">👤</div>
                    <div class="message-content">
                        <div class="message-text">{message["content"]}</div>
                        <div class="message-time">{message.get("timestamp", "")}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message ai-message" style="animation-delay: {i * 0.1}s">
                    <div class="message-avatar ai-avatar">🪞</div>
                    <div class="message-content">
                        <div class="message-text">{message["content"]}</div>
                        <div class="message-time">{message.get("timestamp", "")}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Typing indicator
    if st.session_state.typing:
        st.markdown("""
        <div class="typing-indicator">
            <div class="typing-avatar">🪞</div>
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat input
    st.markdown("<div class='chat-input-container'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([6, 1])
    
    with col1:
        user_input = st.text_input(
            "Type your message...",
            key="chat_input",
            placeholder="Ask me anything or just chat naturally...",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Send", key="send_btn", type="primary")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Handle message sending
    if send_button and user_input:
        # Add user message
        user_message = {
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().strftime("%H:%M")
        }
        st.session_state.chat_history.append(user_message)
        
        # Clear input by rerunning
        st.rerun()
    
    # Generate AI response if last message was from user
    if (st.session_state.chat_history and 
        st.session_state.chat_history[-1]["role"] == "user" and
        not st.session_state.typing):
        
        # Show typing indicator
        st.session_state.typing = True
        
        # Generate AI response
        with st.spinner("🤖 Thinking..."):
            try:
                last_user_message = st.session_state.chat_history[-1]["content"]
                ai_response = st.session_state.mirror_agent.generate_response(last_user_message)
                
                ai_message = {
                    "role": "assistant",
                    "content": ai_response,
                    "timestamp": datetime.now().strftime("%H:%M")
                }
                st.session_state.chat_history.append(ai_message)
                
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
                ai_message = {
                    "role": "assistant",
                    "content": "I'm having trouble processing that right now. Please try again or check your OpenAI API key configuration.",
                    "timestamp": datetime.now().strftime("%H:%M")
                }
                st.session_state.chat_history.append(ai_message)
            
            finally:
                # Hide typing indicator
                st.session_state.typing = False
                st.rerun()
        
        # Show typing indicator
        st.session_state.typing = True
        st.rerun()
        
        # Generate AI response
        try:
            ai_response = st.session_state.mirror_agent.generate_response(user_input)
            
            ai_message = {
                "role": "assistant",
                "content": ai_response,
                "timestamp": datetime.now().strftime("%H:%M")
            }
            st.session_state.chat_history.append(ai_message)
            
        except Exception as e:
            ai_message = {
                "role": "assistant",
                "content": f"I'm having trouble processing that right now. Error: {str(e)}",
                "timestamp": datetime.now().strftime("%H:%M")
            }
            st.session_state.chat_history.append(ai_message)
        
        # Hide typing indicator
        st.session_state.typing = False
        st.rerun()

# Dashboard page
def dashboard_page():
    st.markdown("""
    <div class="page-header">
        <h2>📊 Personality Dashboard</h2>
        <p>Explore your AI's understanding of your personality</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get personality data
    personality_data = st.session_state.mirror_agent.memory_manager.get_personality_traits()
    
    if not personality_data:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🤖</div>
            <h3>No Personality Data Yet</h3>
            <p>Start chatting to help the AI learn your personality!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Create dashboard layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="dashboard-section">
            <h3>🎭 Personality Traits</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Personality radar chart
        traits = personality_data.get("personality_traits", {})
        if traits:
            fig = create_personality_radar(traits)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.markdown("""
        <div class="dashboard-section">
            <h3>💬 Communication Style</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Communication style metrics
        comm_style = personality_data.get("communication_style", {})
        if comm_style:
            create_communication_metrics(comm_style)
    
    # Interests and phrases
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div class="dashboard-section">
            <h3>🎯 Interests & Topics</h3>
        </div>
        """, unsafe_allow_html=True)
        
        interests = personality_data.get("interests_and_topics", [])
        if interests:
            for interest in interests[:5]:
                st.markdown(f"""
                <div class="interest-tag">
                    <span class="tag-icon">•</span>
                    <span class="tag-text">{interest}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<p class='no-data'>No interests identified yet</p>", unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="dashboard-section">
            <h3>💭 Favorite Phrases</h3>
        </div>
        """, unsafe_allow_html=True)
        
        phrases = personality_data.get("favorite_phrases", [])
        if phrases:
            for phrase in phrases[:5]:
                st.markdown(f"""
                <div class="phrase-tag">
                    <span class="phrase-icon">"</span>
                    <span class="phrase-text">{phrase}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<p class='no-data'>No favorite phrases identified yet</p>", unsafe_allow_html=True)

def create_personality_radar(traits):
    categories = list(traits.keys())
    values = list(traits.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Personality Traits',
        line=dict(color='rgba(102, 126, 234, 0.8)', width=3),
        fillcolor='rgba(102, 126, 234, 0.2)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                gridcolor='rgba(255, 255, 255, 0.2)',
                tickcolor='rgba(255, 255, 255, 0.6)',
                tickfont=dict(color='white', size=10)
            ),
            angularaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.2)',
                tickcolor='rgba(255, 255, 255, 0.8)',
                tickfont=dict(color='white', size=12)
            )
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(t=40, b=40, l=40, r=40)
    )
    
    return fig

def create_communication_metrics(comm_style):
    metrics = [
        ("Tone", comm_style.get("tone", "neutral").title()),
        ("Formality", f"{comm_style.get('formality_level', 5)}/10"),
        ("Enthusiasm", f"{comm_style.get('enthusiasm_level', 5)}/10")
    ]
    
    for label, value in metrics:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

# Analytics page
def analytics_page():
    st.markdown("""
    <div class="page-header">
        <h2>📈 Learning Analytics</h2>
        <p>Track your AI's learning progress and insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get progress data
    progress = st.session_state.mirror_agent.get_learning_progress()
    
    # Learning progress cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_analytics_card("Messages Analyzed", progress.get('messages_analyzed', 0), "💬", "#667eea")
    
    with col2:
        create_analytics_card("Next Update At", f"Message {progress.get('next_analysis_at', 5)}", "⏰", "#764ba2")
    
    with col3:
        create_analytics_card("Profile Updated", "Yes" if progress.get('personality_updates', False) else "No", "✅", "#4ecdc4")
    
    with col4:
        create_analytics_card("Learning Stage", progress.get('learning_stage', 'Initial Learning'), "🎯", "#ff6b6b")
    
    # Learning progress chart
    st.markdown("""
    <div class="analytics-section">
        <h3>📊 Learning Progress</h3>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        fig = create_learning_progress_chart(progress)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    except Exception as e:
        st.markdown("""
        <div class="chart-placeholder">
            <div class="placeholder-icon">📊</div>
            <h4>Chart Loading</h4>
            <p>Chart will appear as you interact more with the AI</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Message statistics
    personality_data = st.session_state.mirror_agent.memory_manager.get_personality_traits()
    stats = personality_data.get("message_statistics", {})
    
    if stats:
        st.markdown("""
        <div class="analytics-section">
            <h3>📝 Message Statistics</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            create_analytics_card("Avg Words/Message", f"{stats.get('avg_words_per_message', 0):.1f}", "📝", "#667eea")
        
        with col2:
            sentiment = stats.get('avg_sentiment', 0)
            sentiment_label = "Positive" if sentiment > 0.1 else "Negative" if sentiment < -0.1 else "Neutral"
            create_analytics_card("Overall Sentiment", sentiment_label, "😊", "#4ecdc4")
        
        with col3:
            create_analytics_card("Total Messages", stats.get('total_messages', 0), "💬", "#ff6b6b")

def create_analytics_card(title, value, icon, color):
    st.markdown(f"""
    <div class="analytics-card" style="border-color: {color}40;">
        <div class="card-icon" style="color: {color};">{icon}</div>
        <div class="card-content">
            <div class="card-value" style="color: {color};">{value}</div>
            <div class="card-title">{title}</div>
        </div>
        <div class="card-glow" style="background: {color}20;"></div>
    </div>
    """, unsafe_allow_html=True)

def create_learning_progress_chart(progress):
    stages = ["Initial Learning", "Basic Patterns", "Style Recognition", "Personality Modeling", "Advanced Mirroring"]
    current_stage = progress.get('learning_stage', 'Initial Learning')
    messages = progress.get('messages_analyzed', 0)
    
    # Create progress data
    stage_progress = []
    for i, stage in enumerate(stages):
        if stage == current_stage:
            stage_progress.append(min(100, (messages / (20 * (i + 1))) * 100))
        elif stages.index(current_stage) > i:
            stage_progress.append(100)
        else:
            stage_progress.append(0)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=stages,
        y=stage_progress,
        marker=dict(
            color=['#667eea', '#764ba2', '#4ecdc4', '#ff6b6b', '#45b7d1'],
            line=dict(color='rgba(255,255,255,0.2)', width=1)
        ),
        text=[f"{p:.0f}%" for p in stage_progress],
        textposition='auto',
        textfont=dict(color='white', size=12)
    ))
    
    fig.update_layout(
        title=dict(
            text="Learning Stage Progress",
            font=dict(color='white', size=16),
            x=0.5
        ),
        xaxis=dict(
            tickfont=dict(color='white'),
            gridcolor='rgba(255,255,255,0.1)'
        ),
        yaxis=dict(
            tickfont=dict(color='white'),
            gridcolor='rgba(255,255,255,0.1)',
            range=[0, 100]
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=60, b=40, l=40, r=40)
    )
    
    return fig

# Settings page
def settings_page():
    st.markdown("""
    <div class="page-header">
        <h2>⚙️ Settings & Export</h2>
        <p>Manage your AI personality data and preferences</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Export section
    st.markdown("""
    <div class="settings-section">
        <h3>📥 Data Export</h3>
        <p>Download your complete personality profile and chat history</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export Personality Profile", key="export_personality"):
            personality_data = st.session_state.mirror_agent.memory_manager.get_personality_traits()
            st.download_button(
                "💾 Download Profile",
                json.dumps(personality_data, indent=2),
                file_name=f"personality_profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("💬 Export Chat History", key="export_chat"):
            chat_data = st.session_state.mirror_agent.export_data()
            st.download_button(
                "💾 Download History",
                json.dumps(chat_data, indent=2),
                file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    # Reset section
    st.markdown("""
    <div class="settings-section">
        <h3>🔄 Reset Options</h3>
        <p>Clear data and start fresh</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear Chat History", key="clear_chat"):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
    
    with col2:
        if st.button("🔄 Reset All Data", key="reset_all"):
            st.session_state.mirror_agent.reset_memory()
            st.session_state.chat_history = []
            st.success("All data reset successfully!")
            st.rerun()
    
    # System info
    st.markdown("""
    <div class="settings-section">
        <h3>ℹ️ System Information</h3>
    </div>
    """, unsafe_allow_html=True)
    
    progress = st.session_state.mirror_agent.get_learning_progress()
    
    info_data = {
        "Messages Processed": progress.get('messages_analyzed', 0),
        "Current Learning Stage": progress.get('learning_stage', 'Initial Learning'),
        "Next Analysis": f"Message {progress.get('next_analysis_at', 5)}",
        "Personality Profile": "Available" if progress.get('personality_updates', False) else "Not Available"
    }
    
    for key, value in info_data.items():
        st.markdown(f"""
        <div class="info-row">
            <span class="info-key">{key}:</span>
            <span class="info-value">{value}</span>
        </div>
        """, unsafe_allow_html=True)

# Main app
def main():
    load_css()
    init_session_state()
    
    # Create header
    create_header()
    
    # Create sidebar and get selected page
    selected_page = create_sidebar()
    
    # Route to appropriate page
    if selected_page == "💬 Chat":
        chat_page()
    elif selected_page == "📊 Dashboard":
        dashboard_page()
    elif selected_page == "📈 Analytics":
        analytics_page()
    elif selected_page == "⚙️ Settings":
        settings_page()

if __name__ == "__main__":
    main()
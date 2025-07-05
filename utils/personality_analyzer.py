import re
from typing import Dict, List, Any
from collections import Counter
from textblob import TextBlob
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from config import Config

class PersonalityAnalyzer:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name=Config.MODEL_NAME,
            temperature=0.3,
            openai_api_key=Config.OPENAI_API_KEY
        )
        
        self.analysis_prompt = PromptTemplate.from_template("""
        You are an expert personality analyst. Analyze the following messages from a user and extract their personality traits, communication style, and preferences.

        User Messages:
        {messages}

        Please provide a detailed analysis in JSON format with the following structure:
        {{
            "communication_style": {{
                "tone": "casual/formal/mixed",
                "formality_level": "1-10 scale",
                "enthusiasm_level": "1-10 scale",
                "typical_sentence_length": "short/medium/long",
                "uses_emojis": true/false,
                "uses_slang": true/false
            }},
            "personality_traits": {{
                "openness": "1-10 scale",
                "conscientiousness": "1-10 scale", 
                "extraversion": "1-10 scale",
                "agreeableness": "1-10 scale",
                "neuroticism": "1-10 scale"
            }},
            "interests_and_topics": [
                "list of topics they frequently discuss"
            ],
            "favorite_phrases": [
                "phrases they use often"
            ],
            "emotional_patterns": {{
                "default_mood": "positive/neutral/negative",
                "emotional_range": "1-10 scale",
                "stress_indicators": ["list of indicators"]
            }},
            "linguistic_patterns": {{
                "avg_words_per_message": "number",
                "complexity_level": "1-10 scale",
                "question_frequency": "1-10 scale"
            }}
        }}

        Respond with ONLY the JSON, no additional text.
        """)
    
    def analyze_messages(self, messages: List[str]) -> Dict[str, Any]:
        """Analyze user messages and extract personality traits"""
        if not messages:
            return self._get_default_profile()
        
        # Combine messages for analysis
        combined_messages = "\n".join(messages)
        
        try:
            # Get AI analysis
            response = self.llm.invoke(
                self.analysis_prompt.format(messages=combined_messages)
            )
            
            # Extract content from response
            if hasattr(response, 'content'):
                response_text = response.content
            else:
                response_text = str(response)
            
            # Parse JSON response
            import json
            personality_data = json.loads(response_text)
            
            # Add statistical analysis
            stats = self._calculate_message_statistics(messages)
            personality_data.update(stats)
            
            return personality_data
            
        except Exception as e:
            print(f"Error in personality analysis: {e}")
            return self._get_default_profile()
    
    def _calculate_message_statistics(self, messages: List[str]) -> Dict[str, Any]:
        """Calculate statistical patterns from messages"""
        if not messages:
            return {}
        
        # Basic statistics
        total_words = sum(len(msg.split()) for msg in messages)
        total_chars = sum(len(msg) for msg in messages)
        
        # Sentiment analysis
        sentiments = []
        for msg in messages:
            blob = TextBlob(msg)
            sentiments.append(blob.sentiment.polarity)
        
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
        
        # Common words (excluding stop words)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'}
        
        all_words = []
        for msg in messages:
            words = re.findall(r'\b\w+\b', msg.lower())
            all_words.extend([w for w in words if w not in stop_words and len(w) > 2])
        
        common_words = Counter(all_words).most_common(10)
        
        # Punctuation patterns
        exclamations = sum(msg.count('!') for msg in messages)
        questions = sum(msg.count('?') for msg in messages)
        
        return {
            "message_statistics": {
                "total_messages": len(messages),
                "avg_words_per_message": total_words / len(messages),
                "avg_chars_per_message": total_chars / len(messages),
                "avg_sentiment": avg_sentiment,
                "common_words": [word for word, count in common_words],
                "exclamation_frequency": exclamations / len(messages),
                "question_frequency": questions / len(messages)
            }
        }
    
    def _get_default_profile(self) -> Dict[str, Any]:
        """Return default personality profile"""
        return {
            "communication_style": {
                "tone": "neutral",
                "formality_level": 5,
                "enthusiasm_level": 5,
                "typical_sentence_length": "medium",
                "uses_emojis": False,
                "uses_slang": False
            },
            "personality_traits": {
                "openness": 5,
                "conscientiousness": 5,
                "extraversion": 5,
                "agreeableness": 5,
                "neuroticism": 5
            },
            "interests_and_topics": [],
            "favorite_phrases": [],
            "emotional_patterns": {
                "default_mood": "neutral",
                "emotional_range": 5,
                "stress_indicators": []
            },
            "linguistic_patterns": {
                "avg_words_per_message": 10,
                "complexity_level": 5,
                "question_frequency": 5
            },
            "message_statistics": {
                "total_messages": 0,
                "avg_words_per_message": 0,
                "avg_chars_per_message": 0,
                "avg_sentiment": 0,
                "common_words": [],
                "exclamation_frequency": 0,
                "question_frequency": 0
            }
        }
    
    def get_personality_summary(self, profile: Dict[str, Any]) -> str:
        """Generate a human-readable personality summary"""
        if not profile:
            return "No personality data available yet."
        
        comm_style = profile.get("communication_style", {})
        personality = profile.get("personality_traits", {})
        stats = profile.get("message_statistics", {})
        
        summary = f"""
        🎭 **Communication Style**: {comm_style.get('tone', 'neutral').title()} tone, 
        {'high' if comm_style.get('enthusiasm_level', 5) > 7 else 'moderate' if comm_style.get('enthusiasm_level', 5) > 3 else 'low'} enthusiasm
        
        🧠 **Personality Traits**: 
        - Openness: {personality.get('openness', 5)}/10
        - Conscientiousness: {personality.get('conscientiousness', 5)}/10  
        - Extraversion: {personality.get('extraversion', 5)}/10
        - Agreeableness: {personality.get('agreeableness', 5)}/10
        
        📊 **Message Patterns**: 
        - Average {stats.get('avg_words_per_message', 0):.1f} words per message
        - {'Positive' if stats.get('avg_sentiment', 0) > 0.1 else 'Negative' if stats.get('avg_sentiment', 0) < -0.1 else 'Neutral'} sentiment overall
        - {stats.get('total_messages', 0)} total messages analyzed
        """
        
        return summary.strip()
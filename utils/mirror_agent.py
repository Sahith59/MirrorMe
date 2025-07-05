from typing import Dict, List, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from config import Config
from utils.memory_manager import MemoryManager
from utils.personality_analyzer import PersonalityAnalyzer

class MirrorAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name=Config.MODEL_NAME,
            temperature=Config.TEMPERATURE,
            max_tokens=Config.MAX_TOKENS,
            openai_api_key=Config.OPENAI_API_KEY
        )
        
        self.memory_manager = MemoryManager()
        self.personality_analyzer = PersonalityAnalyzer()
        
        # Initialize conversation messages
        self.conversation_messages = []
        
        # Base prompt template
        self.base_prompt = PromptTemplate.from_template("""
        You are MirrorMe, an AI that learns to mirror the user's personality and communication style over time.

        PERSONALITY PROFILE:
        {personality_context}

        SIMILAR PAST MESSAGES:
        {similar_messages}

        CONVERSATION CONTEXT:
        {conversation_context}

        INSTRUCTIONS:
        1. Respond in the user's typical communication style based on the personality profile
        2. Use similar tone, formality level, and enthusiasm as shown in past messages
        3. Reference their interests and use their favorite phrases when appropriate
        4. Keep responses concise and engaging
        5. Gradually become more like them as you learn more about their style

        Current message: {input}
        
        Response:""")
    
    def generate_response(self, user_input: str) -> str:
        """Generate a response that mirrors the user's style"""
        # Add user message to memory
        self.memory_manager.add_message("user", user_input)
        
        # Check if we need to update personality profile
        self._maybe_update_personality()
        
        # Get context for response generation
        personality_context = self._get_personality_context()
        similar_messages = self.memory_manager.get_similar_messages(user_input, k=3)
        conversation_context = self._get_conversation_context()
        
        # Generate response
        try:
            # Create the full prompt
            full_prompt = self.base_prompt.format(
                personality_context=personality_context,
                similar_messages=self._format_similar_messages(similar_messages),
                conversation_context=conversation_context,
                input=user_input
            )
            
            # Generate response using invoke method
            response = self.llm.invoke(full_prompt)
            
            # Extract content from response
            if hasattr(response, 'content'):
                response_text = response.content
            else:
                response_text = str(response)
            
            # Add AI response to memory
            self.memory_manager.add_message("assistant", response_text)
            
            return response_text.strip()
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm still learning about your communication style. Could you tell me more?"
    
    def _maybe_update_personality(self):
        """Update personality profile if we have enough new messages"""
        user_count = self.memory_manager.get_user_message_count()
        
        if (user_count >= Config.MIN_MESSAGES_FOR_ANALYSIS and 
            user_count % Config.PERSONALITY_ANALYSIS_FREQUENCY == 0):
            
            # Get recent messages for analysis
            messages = self.memory_manager.get_user_messages_for_analysis()
            
            # Analyze personality
            new_profile = self.personality_analyzer.analyze_messages(messages)
            
            # Update profile
            self.memory_manager.update_personality_profile(new_profile)
    
    def _get_personality_context(self) -> str:
        """Get formatted personality context"""
        profile = self.memory_manager.get_personality_traits()
        
        if not profile:
            return "User personality still being learned..."
        
        context = []
        
        # Communication style
        comm_style = profile.get("communication_style", {})
        if comm_style:
            context.append(f"Communication Style: {comm_style.get('tone', 'neutral')} tone, "
                         f"formality level {comm_style.get('formality_level', 5)}/10")
        
        # Personality traits
        personality = profile.get("personality_traits", {})
        if personality:
            traits = []
            for trait, score in personality.items():
                if score > 7:
                    traits.append(f"high {trait}")
                elif score < 4:
                    traits.append(f"low {trait}")
            if traits:
                context.append(f"Personality: {', '.join(traits)}")
        
        # Interests
        interests = profile.get("interests_and_topics", [])
        if interests:
            context.append(f"Interests: {', '.join(interests[:5])}")
        
        # Favorite phrases
        phrases = profile.get("favorite_phrases", [])
        if phrases:
            context.append(f"Typical phrases: {', '.join(phrases[:3])}")
        
        # Message statistics
        stats = profile.get("message_statistics", {})
        if stats:
            avg_words = stats.get("avg_words_per_message", 0)
            sentiment = stats.get("avg_sentiment", 0)
            context.append(f"Typical message length: {avg_words:.1f} words")
            
            if sentiment > 0.1:
                context.append("Generally positive tone")
            elif sentiment < -0.1:
                context.append("Generally more reserved tone")
        
        return "\n".join(context) if context else "User personality still being learned..."
    
    def _format_similar_messages(self, messages: List[str]) -> str:
        """Format similar messages for context"""
        if not messages:
            return "No similar messages found yet."
        
        formatted = []
        for i, msg in enumerate(messages, 1):
            formatted.append(f"{i}. {msg}")
        
        return "\n".join(formatted)
    
    def _get_conversation_context(self) -> str:
        """Get recent conversation context"""
        context = self.memory_manager.get_conversation_context(limit=6)
        
        if not context:
            return "Start of conversation"
        
        formatted = []
        for msg in context[-6:]:  # Last 6 messages
            role = "User" if msg["role"] == "user" else "Assistant"
            formatted.append(f"{role}: {msg['content']}")
        
        return "\n".join(formatted)
    
    def get_personality_summary(self) -> str:
        """Get a summary of the learned personality"""
        profile = self.memory_manager.get_personality_traits()
        return self.personality_analyzer.get_personality_summary(profile)
    
    def get_learning_progress(self) -> Dict[str, Any]:
        """Get learning progress statistics"""
        user_count = self.memory_manager.get_user_message_count()
        profile = self.memory_manager.get_personality_traits()
        
        return {
            "messages_analyzed": user_count,
            "personality_updates": len(profile) > 0,
            "learning_stage": self._get_learning_stage(user_count),
            "next_analysis_at": ((user_count // Config.PERSONALITY_ANALYSIS_FREQUENCY) + 1) * Config.PERSONALITY_ANALYSIS_FREQUENCY
        }
    
    def _get_learning_stage(self, message_count: int) -> str:
        """Determine current learning stage"""
        if message_count < Config.MIN_MESSAGES_FOR_ANALYSIS:
            return "Initial Learning"
        elif message_count < 20:
            return "Basic Patterns"
        elif message_count < 50:
            return "Style Recognition"
        elif message_count < 100:
            return "Personality Modeling"
        else:
            return "Advanced Mirroring"
    
    def reset_memory(self):
        """Reset all memory and start fresh"""
        self.memory_manager.clear_memory()
        self.conversation_messages = []
    
    def export_data(self) -> Dict[str, Any]:
        """Export all learning data"""
        return self.memory_manager.export_data()
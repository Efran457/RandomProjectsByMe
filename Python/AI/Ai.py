#!/usr/bin/env python3
"""
AI Chatbot with built-in intelligence - No API required!
Uses pattern matching, keyword detection, and basic learning capabilities.
"""

import re
import random
import json
import os
from datetime import datetime


class AIchatbot:
    def __init__(self):
        self.name = "AI Assistant"
        self.user_name = None
        self.context = {}
        self.memory_file = "chatbot_memory.json"
        self.learned_responses = {}
        self.conversation_count = 0

        # Load any previously learned responses
        self.load_memory()

        # Greetings
        self.greetings = {
            'patterns': [r'\b(hi|hello|hey|greetings|sup|yo)\b'],
            'responses': [
                "Hello! How can I help you today?",
                "Hi there! What's on your mind?",
                "Hey! Nice to meet you. What can I do for you?",
                "Greetings! How are you doing?"
            ]
        }

        # Farewells
        self.farewells = {
            'patterns': [r'\b(bye|goodbye|see you|later|exit|quit)\b'],
            'responses': [
                "Goodbye! Have a great day!",
                "See you later! Take care!",
                "Bye! It was nice chatting with you!",
                "Until next time! Goodbye!"
            ]
        }

        # How are you questions
        self.wellbeing = {
            'patterns': [r'how are you|how\'re you|hows it going|whats up'],
            'responses': [
                "I'm doing great, thanks for asking! How about you?",
                "I'm functioning perfectly! How can I assist you?",
                "I'm excellent! What brings you here today?",
                "I'm doing well! How are you feeling?"
            ]
        }

        # Name questions
        self.name_questions = {
            'patterns': [r'what is your name|what\'s your name|who are you|your name'],
            'responses': [
                f"I'm {self.name}, your AI assistant!",
                f"You can call me {self.name}. I'm here to help!",
                f"My name is {self.name}. Nice to meet you!"
            ]
        }

        # Thank you responses
        self.thanks = {
            'patterns': [r'\b(thank you|thanks|thx|ty|appreciate)\b'],
            'responses': [
                "You're welcome!",
                "Happy to help!",
                "No problem at all!",
                "Glad I could assist!",
                "Anytime!"
            ]
        }

        # Jokes
        self.jokes = [
            "Why did the programmer quit his job? Because he didn't get arrays!",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
            "Why did the computer go to the doctor? It had a virus!",
            "What's a programmer's favorite place to hang out? The Foo Bar!"
        ]

        # Math capability
        self.math_patterns = r'(what is|calculate|compute|solve)\s*([\d\s\+\-\*\/\(\)\.]+)'

        # Time/date
        self.time_patterns = [r'\b(time|clock|what time)\b', r'\b(date|today|day)\b']

        # Emotional responses
        self.emotions = {
            'happy': {
                'patterns': [r'\b(happy|excited|great|wonderful|fantastic|good|glad)\b'],
                'responses': [
                    "That's wonderful! I'm happy to hear that!",
                    "Great to hear you're feeling good!",
                    "Awesome! Keep that positive energy going!"
                ]
            },
            'sad': {
                'patterns': [r'\b(sad|depressed|down|unhappy|upset|bad)\b'],
                'responses': [
                    "I'm sorry to hear that. Is there anything I can do to help?",
                    "That's tough. Remember, things will get better!",
                    "I'm here if you need to talk. What's bothering you?"
                ]
            },
            'angry': {
                'patterns': [r'\b(angry|mad|furious|annoyed|frustrated)\b'],
                'responses': [
                    "I understand you're frustrated. Let's see how I can help.",
                    "Take a deep breath. What's making you angry?",
                    "I'm here to listen. What happened?"
                ]
            }
        }

        # Knowledge base
        self.knowledge = {
            'programming': {
                'patterns': [r'\b(python|java|javascript|code|programming|developer)\b'],
                'responses': [
                    "Programming is fascinating! Are you learning to code?",
                    "I love talking about programming! What language interests you?",
                    "Code is poetry! What would you like to know about programming?"
                ]
            },
            'ai': {
                'patterns': [r'\b(ai|artificial intelligence|machine learning|neural|deep learning)\b'],
                'responses': [
                    "AI is the future! It's amazing how machines can learn.",
                    "Artificial Intelligence is evolving rapidly. What aspect interests you?",
                    "I'm an example of AI in action! What would you like to know?"
                ]
            },
            'weather': {
                'patterns': [r'\b(weather|rain|sunny|cloud|temperature)\b'],
                'responses': [
                    "I don't have real-time weather data, but I hope it's nice where you are!",
                    "Weather can really affect our mood! Is it nice outside?",
                    "I wish I could check the weather for you! Try a weather app for accurate info."
                ]
            }
        }

    def load_memory(self):
        """Load learned responses from file"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    self.learned_responses = data.get('learned_responses', {})
                    self.context = data.get('context', {})
                    self.user_name = self.context.get('user_name', None)
            except:
                self.learned_responses = {}
                self.context = {}

    def save_memory(self):
        """Save learned responses to file"""
        data = {
            'learned_responses': self.learned_responses,
            'context': self.context,
            'last_updated': datetime.now().isoformat()
        }
        with open(self.memory_file, 'w') as f:
            json.dump(data, f, indent=2)

    def extract_name(self, text):
        """Extract user's name from text"""
        patterns = [
            r'my name is (\w+)',
            r'i am (\w+)',
            r'i\'m (\w+)',
            r'call me (\w+)',
            r'this is (\w+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).capitalize()
        return None

    def calculate_math(self, expression):
        """Safely evaluate mathematical expressions"""
        try:
            # Remove any non-math characters
            expression = re.sub(r'[^0-9\+\-\*\/\(\)\.\s]', '', expression)
            result = eval(expression)
            return f"The answer is {result}"
        except:
            return "Sorry, I couldn't calculate that. Please check your expression."

    def get_time(self):
        """Return current time"""
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}"

    def get_date(self):
        """Return current date"""
        return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}"

    def detect_emotion(self, text):
        """Detect emotional content in text"""
        for emotion, data in self.emotions.items():
            for pattern in data['patterns']:
                if re.search(pattern, text, re.IGNORECASE):
                    return random.choice(data['responses'])
        return None

    def check_knowledge_base(self, text):
        """Check if text matches knowledge base topics"""
        for topic, data in self.knowledge.items():
            for pattern in data['patterns']:
                if re.search(pattern, text, re.IGNORECASE):
                    return random.choice(data['responses'])
        return None

    def learn_from_conversation(self, user_input, bot_response):
        """Learn new patterns from conversations"""
        # Extract key words from user input (3+ characters)
        keywords = re.findall(r'\b\w{3,}\b', user_input.lower())

        if len(keywords) >= 2:
            # Create a pattern from the first few keywords
            pattern = '|'.join(keywords[:3])

            # Store if it's a unique enough pattern
            if pattern not in self.learned_responses:
                self.learned_responses[pattern] = bot_response
                return True
        return False

    def generate_response(self, user_input):
        """Main logic to generate responses"""
        text = user_input.lower().strip()

        # Update conversation count
        self.conversation_count += 1

        # Check if user is teaching the bot something
        teach_match = re.search(
            r'(?:remember|learn|when i say) ["\']?(.+?)["\']? (?:you say|respond with|answer) ["\']?(.+?)["\']?$', text,
            re.IGNORECASE)
        if teach_match:
            pattern = teach_match.group(1).lower()
            response = teach_match.group(2)
            self.learned_responses[pattern] = response
            self.save_memory()
            return f"Got it! I'll remember that. When you say '{pattern}', I'll respond with '{response}'."

        # Check for name in input
        name = self.extract_name(text)
        if name:
            self.user_name = name
            self.context['user_name'] = name
            self.save_memory()
            return f"Nice to meet you, {name}! I'll remember that."

        # Use user's name if we know it
        greeting_suffix = f", {self.user_name}" if self.user_name else ""

        # Check greetings
        for pattern in self.greetings['patterns']:
            if re.search(pattern, text):
                return random.choice(self.greetings['responses']) + greeting_suffix

        # Check farewells
        for pattern in self.farewells['patterns']:
            if re.search(pattern, text):
                return random.choice(self.farewells['responses'])

        # Check wellbeing
        if re.search(self.wellbeing['patterns'][0], text):
            return random.choice(self.wellbeing['responses'])

        # Check name questions
        for pattern in self.name_questions['patterns']:
            if re.search(pattern, text):
                return random.choice(self.name_questions['responses'])

        # Check thanks
        for pattern in self.thanks['patterns']:
            if re.search(pattern, text):
                return random.choice(self.thanks['responses'])

        # Check for joke request
        if re.search(r'\b(joke|funny|laugh)\b', text):
            return random.choice(self.jokes)

        # Check memory stats
        if re.search(r'\b(memory|what do you remember|what have you learned)\b', text):
            stats = f"📊 Memory Stats:\n"
            stats += f"• Conversations: {self.conversation_count}\n"
            stats += f"• Learned responses: {len(self.learned_responses)}\n"
            if self.user_name:
                stats += f"• Your name: {self.user_name}\n"
            if self.learned_responses:
                stats += f"\n🧠 I remember these topics:\n"
                for pattern in list(self.learned_responses.keys())[:5]:
                    stats += f"  - {pattern}\n"
            return stats

        # Check for math
        math_match = re.search(self.math_patterns, text, re.IGNORECASE)
        if math_match:
            return self.calculate_math(math_match.group(2))

        # Check for time
        if re.search(self.time_patterns[0], text):
            return self.get_time()

        # Check for date
        if re.search(self.time_patterns[1], text):
            return self.get_date()

        # Check emotions
        emotion_response = self.detect_emotion(text)
        if emotion_response:
            return emotion_response

        # Check knowledge base
        knowledge_response = self.check_knowledge_base(text)
        if knowledge_response:
            return knowledge_response

        # Check learned responses
        for pattern, response in self.learned_responses.items():
            if re.search(pattern, text, re.IGNORECASE):
                return response

        # Question detection
        if '?' in user_input:
            responses = [
                "That's an interesting question! I'm still learning, but I'll do my best to help.",
                "Hmm, let me think about that. Could you provide more details?",
                "Great question! I don't have all the answers, but I'm here to chat about it.",
                "I'm not entirely sure, but I'd love to explore that topic with you!"
            ]
            return random.choice(responses)

        # Default responses with context
        default_responses = [
            "That's interesting! Tell me more.",
            "I see. What else is on your mind?",
            "Fascinating! Can you elaborate on that?",
            "I'm listening. Please continue.",
            "Interesting perspective! What made you think of that?",
            "I understand. Is there something specific you'd like to know?",
            "That's worth thinking about. What's your take on it?"
        ]

        return random.choice(default_responses)


def main():
    """Main chatbot loop"""
    bot = AIchatbot()

    print("=" * 70)
    print(" " * 20 + "🤖 AI CHATBOT 🤖")
    print("=" * 70)
    print(f"Welcome! I'm {bot.name}, your intelligent conversation partner.")
    print("I can:")
    print("  • Chat naturally with you")
    print("  • Solve math problems (try: 'calculate 25 * 4 + 10')")
    print("  • Tell jokes (just ask!)")
    print("  • Tell you the time and date")
    print("  • Remember your name")
    print("  • Respond to your emotions")
    print("\nType 'quit', 'exit', or 'bye' to end our conversation.")
    print("=" * 70)
    print()

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            # Check for exit
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print(f"\n{bot.name}: " + random.choice(bot.farewells['responses']))
                bot.save_memory()
                break

            # Generate and display response
            response = bot.generate_response(user_input)
            print(f"\n{bot.name}: {response}\n")

            # Auto-learn from this conversation (every 5 interactions)
            if bot.conversation_count % 5 == 0:
                bot.save_memory()
                # Optional: show learning indicator
                # print("💾 [Memory saved]")

        except KeyboardInterrupt:
            print(f"\n\n{bot.name}: Goodbye! Thanks for chatting!")
            bot.save_memory()
            break
        except Exception as e:
            print(f"\n{bot.name}: Oops, I encountered an error. Let's continue!\n")


if __name__ == "__main__":
    main()
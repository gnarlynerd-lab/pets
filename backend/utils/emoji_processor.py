"""
Emoji processing utilities
"""
from typing import Dict, List
import re

class EmojiProcessor:
    """Process and analyze emoji sequences"""
    
    # Basic emotion mappings for common emojis
    EMOJI_EMOTIONS = {
        "😊": {"happiness": 0.8, "friendliness": 0.7},
        "😃": {"happiness": 0.9, "excitement": 0.8},
        "😄": {"happiness": 1.0, "excitement": 0.9},
        "😁": {"happiness": 0.9, "playfulness": 0.8},
        "😆": {"happiness": 1.0, "excitement": 1.0},
        "😂": {"happiness": 1.0, "amusement": 1.0},
        "🤣": {"happiness": 1.0, "amusement": 1.0},
        "😍": {"love": 1.0, "happiness": 0.9},
        "🥰": {"love": 0.9, "happiness": 0.8},
        "😘": {"love": 0.8, "playfulness": 0.7},
        "😗": {"affection": 0.7, "friendliness": 0.6},
        "😙": {"affection": 0.7, "happiness": 0.6},
        "😚": {"affection": 0.8, "shyness": 0.5},
        "☺️": {"happiness": 0.7, "contentment": 0.8},
        "🙂": {"contentment": 0.6, "friendliness": 0.5},
        "🤗": {"friendliness": 0.9, "warmth": 0.9},
        "🤩": {"excitement": 1.0, "amazement": 0.9},
        "🤔": {"curiosity": 0.8, "thoughtfulness": 0.7},
        "🤨": {"skepticism": 0.7, "curiosity": 0.5},
        "😐": {"neutrality": 0.8, "indifference": 0.6},
        "😑": {"annoyance": 0.5, "indifference": 0.7},
        "😶": {"silence": 0.8, "neutrality": 0.6},
        "🙄": {"annoyance": 0.7, "skepticism": 0.6},
        "😏": {"smugness": 0.7, "playfulness": 0.5},
        "😣": {"frustration": 0.7, "distress": 0.6},
        "😥": {"sadness": 0.6, "worry": 0.7},
        "😮": {"surprise": 0.8, "shock": 0.6},
        "🤐": {"silence": 0.9, "secretiveness": 0.8},
        "😯": {"surprise": 0.7, "amazement": 0.6},
        "😪": {"tiredness": 0.8, "sadness": 0.4},
        "😫": {"exhaustion": 0.9, "frustration": 0.7},
        "😴": {"tiredness": 1.0, "sleepiness": 1.0},
        "😌": {"contentment": 0.8, "relief": 0.7},
        "😛": {"playfulness": 0.8, "silliness": 0.7},
        "😜": {"playfulness": 0.9, "mischief": 0.8},
        "😝": {"playfulness": 0.9, "silliness": 0.9},
        "🤤": {"desire": 0.8, "hunger": 0.9},
        "😒": {"disapproval": 0.7, "annoyance": 0.6},
        "😓": {"anxiety": 0.6, "worry": 0.7},
        "😔": {"sadness": 0.7, "disappointment": 0.8},
        "😕": {"confusion": 0.7, "concern": 0.6},
        "🙃": {"playfulness": 0.6, "irony": 0.7},
        "🤑": {"greed": 0.8, "excitement": 0.6},
        "😲": {"shock": 0.8, "surprise": 0.9},
        "☹️": {"sadness": 0.8, "disappointment": 0.7},
        "🙁": {"sadness": 0.6, "disappointment": 0.6},
        "😖": {"distress": 0.8, "frustration": 0.7},
        "😞": {"disappointment": 0.8, "sadness": 0.7},
        "😟": {"worry": 0.8, "concern": 0.7},
        "😤": {"frustration": 0.8, "anger": 0.6},
        "😢": {"sadness": 0.9, "crying": 0.9},
        "😭": {"sadness": 1.0, "crying": 1.0},
        "😦": {"concern": 0.6, "worry": 0.5},
        "😧": {"worry": 0.7, "shock": 0.6},
        "😨": {"fear": 0.7, "anxiety": 0.8},
        "😩": {"frustration": 0.8, "exhaustion": 0.7},
        "🤯": {"shock": 1.0, "amazement": 0.9},
        "😬": {"awkwardness": 0.8, "nervousness": 0.7},
        "😰": {"anxiety": 0.9, "fear": 0.7},
        "😱": {"fear": 1.0, "shock": 1.0},
        "🥵": {"heat": 0.9, "exhaustion": 0.7},
        "🥶": {"cold": 0.9, "discomfort": 0.7},
        "😳": {"embarrassment": 0.8, "surprise": 0.6},
        "🤪": {"craziness": 0.9, "playfulness": 0.8},
        "😵": {"confusion": 0.9, "dizziness": 0.9},
        "🥴": {"confusion": 0.8, "intoxication": 0.7},
        "😠": {"anger": 0.8, "frustration": 0.7},
        "😡": {"anger": 1.0, "rage": 0.9},
        "🤬": {"anger": 1.0, "rage": 1.0},
        "😷": {"sickness": 0.8, "caution": 0.7},
        "🤒": {"sickness": 0.9, "fever": 0.9},
        "🤕": {"injury": 0.9, "pain": 0.8},
        "🤢": {"nausea": 0.9, "disgust": 0.8},
        "🤮": {"disgust": 1.0, "sickness": 0.9},
        "🤧": {"sickness": 0.7, "cold": 0.8},
        "🥳": {"celebration": 1.0, "excitement": 0.9},
        "🥺": {"pleading": 0.9, "sadness": 0.5},
        "🤠": {"confidence": 0.8, "playfulness": 0.7},
        "🤡": {"silliness": 0.9, "playfulness": 0.8},
        "🤥": {"lying": 0.8, "mischief": 0.7},
        "🤫": {"silence": 0.9, "secretiveness": 0.8},
        "🤭": {"surprise": 0.6, "shyness": 0.7},
        "🧐": {"skepticism": 0.8, "curiosity": 0.7},
        "🤓": {"intelligence": 0.8, "nerdiness": 0.9},
        "😈": {"mischief": 0.9, "evil": 0.7},
        "👿": {"anger": 0.8, "evil": 0.9},
        "👹": {"fear": 0.7, "evil": 0.8},
        "👺": {"anger": 0.7, "evil": 0.7},
        "💀": {"death": 0.9, "fear": 0.6},
        "☠️": {"danger": 0.9, "death": 0.9},
        "👻": {"fear": 0.5, "playfulness": 0.6},
        "👽": {"alienation": 0.7, "strangeness": 0.8},
        "👾": {"playfulness": 0.7, "gaming": 0.8},
        "🤖": {"roboticness": 0.9, "technology": 0.8},
        "💩": {"disgust": 0.6, "humor": 0.7},
        "👋": {"greeting": 0.9, "friendliness": 0.8},
        "✋": {"stop": 0.8, "greeting": 0.5},
        "🖐️": {"greeting": 0.7, "openness": 0.6},
        "👌": {"approval": 0.8, "perfection": 0.7},
        "✌️": {"peace": 0.8, "victory": 0.7},
        "🤞": {"hope": 0.8, "luck": 0.7},
        "🤟": {"love": 0.8, "rock": 0.7},
        "🤘": {"rock": 0.9, "coolness": 0.8},
        "🤙": {"coolness": 0.8, "relaxation": 0.7},
        "👍": {"approval": 0.9, "positivity": 0.8},
        "👎": {"disapproval": 0.9, "negativity": 0.8},
        "👊": {"strength": 0.8, "aggression": 0.6},
        "✊": {"strength": 0.8, "solidarity": 0.7},
        "👏": {"applause": 0.9, "approval": 0.8},
        "🙌": {"celebration": 0.9, "praise": 0.8},
        "👐": {"openness": 0.8, "welcome": 0.7},
        "🤲": {"prayer": 0.7, "offering": 0.8},
        "🙏": {"prayer": 0.9, "gratitude": 0.8},
        "❤️": {"love": 1.0, "affection": 0.9},
        "🧡": {"warmth": 0.8, "enthusiasm": 0.7},
        "💛": {"happiness": 0.8, "friendship": 0.7},
        "💚": {"nature": 0.7, "growth": 0.6},
        "💙": {"trust": 0.8, "loyalty": 0.7},
        "💜": {"creativity": 0.7, "magic": 0.6},
        "🖤": {"darkness": 0.7, "elegance": 0.6},
        "🤍": {"purity": 0.8, "innocence": 0.7},
        "🤎": {"earthiness": 0.7, "stability": 0.6},
        "💔": {"heartbreak": 0.9, "sadness": 0.8},
        "❣️": {"love": 0.8, "exclamation": 0.7},
        "💕": {"love": 0.9, "affection": 0.8},
        "💞": {"love": 0.9, "romance": 0.8},
        "💓": {"love": 0.8, "heartbeat": 0.7},
        "💗": {"love": 0.9, "growing": 0.7},
        "💖": {"love": 0.9, "sparkle": 0.8},
        "💘": {"love": 1.0, "struck": 0.9},
        "💝": {"love": 0.8, "gift": 0.7},
        "🌟": {"excellence": 0.9, "sparkle": 0.8},
        "⭐": {"excellence": 0.8, "rating": 0.7},
        "✨": {"magic": 0.8, "sparkle": 0.9},
        "💫": {"dizziness": 0.6, "magic": 0.7},
        "🔥": {"heat": 0.9, "excitement": 0.8},
        "💥": {"explosion": 0.9, "impact": 0.8},
        "💢": {"anger": 0.8, "frustration": 0.7},
        "💯": {"perfection": 1.0, "agreement": 0.9},
        "🎉": {"celebration": 1.0, "party": 0.9},
        "🎊": {"celebration": 0.9, "festivity": 0.8},
        "🎈": {"celebration": 0.7, "lightness": 0.6},
        "🎁": {"gift": 0.8, "surprise": 0.7},
        "🎀": {"gift": 0.7, "femininity": 0.6},
        "🏆": {"victory": 1.0, "achievement": 0.9},
        "🥇": {"first": 1.0, "victory": 0.9},
        "🥈": {"second": 0.8, "achievement": 0.7},
        "🥉": {"third": 0.7, "achievement": 0.6},
        "🎯": {"target": 0.8, "precision": 0.9},
        "🎪": {"circus": 0.8, "entertainment": 0.7},
        "🎭": {"drama": 0.8, "theater": 0.7},
        "🎨": {"art": 0.9, "creativity": 0.8},
        "🎬": {"movie": 0.8, "action": 0.7},
        "🎤": {"singing": 0.8, "performance": 0.7},
        "🎧": {"music": 0.8, "listening": 0.7},
        "🎵": {"music": 0.8, "melody": 0.7},
        "🎶": {"music": 0.9, "notes": 0.8},
        "🎹": {"piano": 0.8, "music": 0.7},
        "🥁": {"drums": 0.8, "rhythm": 0.9},
        "🎷": {"jazz": 0.8, "saxophone": 0.7},
        "🎺": {"trumpet": 0.8, "fanfare": 0.7},
        "🎸": {"rock": 0.9, "guitar": 0.8},
        "🎻": {"classical": 0.8, "violin": 0.7},
        "🎮": {"gaming": 0.9, "entertainment": 0.8},
        "🕹️": {"gaming": 0.8, "arcade": 0.7},
        "🎲": {"gambling": 0.7, "chance": 0.8},
        "🎰": {"gambling": 0.8, "luck": 0.7},
        "🧩": {"puzzle": 0.8, "problem": 0.7},
        "♟️": {"chess": 0.8, "strategy": 0.9},
        "🎳": {"bowling": 0.7, "sport": 0.6},
        "🏀": {"basketball": 0.8, "sport": 0.7},
        "⚽": {"soccer": 0.8, "sport": 0.7},
        "🏈": {"football": 0.8, "sport": 0.7},
        "⚾": {"baseball": 0.8, "sport": 0.7},
        "🥎": {"softball": 0.7, "sport": 0.6},
        "🏐": {"volleyball": 0.7, "sport": 0.6},
        "🏉": {"rugby": 0.8, "sport": 0.7},
        "🎾": {"tennis": 0.8, "sport": 0.7},
        "🥏": {"frisbee": 0.7, "sport": 0.6},
        "🎱": {"billiards": 0.7, "sport": 0.6},
        "🏓": {"pingpong": 0.7, "sport": 0.6},
        "🏸": {"badminton": 0.7, "sport": 0.6},
        "🏒": {"hockey": 0.8, "sport": 0.7},
        "🏑": {"fieldhockey": 0.7, "sport": 0.6},
        "🥍": {"lacrosse": 0.7, "sport": 0.6},
        "🏏": {"cricket": 0.7, "sport": 0.6},
        "🥅": {"goal": 0.8, "target": 0.7},
        "⛳": {"golf": 0.7, "sport": 0.6},
        "🏹": {"archery": 0.8, "precision": 0.7},
        "🎣": {"fishing": 0.7, "patience": 0.8},
        "🤿": {"diving": 0.7, "underwater": 0.8},
        "🥊": {"boxing": 0.8, "fighting": 0.7},
        "🥋": {"martial_arts": 0.8, "discipline": 0.7},
        "🎿": {"skiing": 0.8, "winter": 0.7},
        "⛷️": {"skiing": 0.8, "downhill": 0.7},
        "🏂": {"snowboarding": 0.8, "winter": 0.7},
        "🤺": {"fencing": 0.7, "sport": 0.6},
        "🤸": {"gymnastics": 0.8, "flexibility": 0.7},
        "⛹️": {"basketball": 0.7, "sport": 0.6},
        "🤾": {"handball": 0.7, "sport": 0.6},
        "🏌️": {"golf": 0.7, "sport": 0.6},
        "🏇": {"horseracing": 0.8, "speed": 0.7},
        "🧘": {"meditation": 0.9, "calm": 0.8},
        "🏄": {"surfing": 0.8, "waves": 0.7},
        "🏊": {"swimming": 0.8, "water": 0.7},
        "🚣": {"rowing": 0.7, "water": 0.6},
        "🧗": {"climbing": 0.8, "challenge": 0.7},
        "🚴": {"cycling": 0.8, "exercise": 0.7},
        "🚵": {"mountainbiking": 0.8, "adventure": 0.7},
        "🏃": {"running": 0.8, "exercise": 0.7},
        "🚶": {"walking": 0.6, "movement": 0.5},
        "🧍": {"standing": 0.5, "stillness": 0.6},
        "🧎": {"kneeling": 0.6, "submission": 0.5},
        "💃": {"dancing": 0.9, "celebration": 0.8},
        "🕺": {"dancing": 0.9, "party": 0.8},
        "🕴️": {"business": 0.7, "levitation": 0.6},
        "🧖": {"spa": 0.8, "relaxation": 0.9},
        "🧑‍🦯": {"blindness": 0.6, "disability": 0.5},
        "🧑‍🦼": {"wheelchair": 0.6, "disability": 0.5},
        "🧑‍🦽": {"mobility": 0.6, "disability": 0.5},
    }
    
    def analyze_emoji_sequence(self, emoji_string: str) -> Dict[str, float]:
        """Analyze emotions in an emoji sequence"""
        emotions = {}
        emoji_count = 0
        
        # Find all emojis in the string
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002500-\U00002BEF"  # chinese char
            "\U00002702-\U000027B0"
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "\U0001f926-\U0001f937"
            "\U00010000-\U0010ffff"
            "\u2640-\u2642"
            "\u2600-\u2B55"
            "\u200d"
            "\u23cf"
            "\u23e9"
            "\u231a"
            "\ufe0f"  # dingbats
            "\u3030"
            "]+", flags=re.UNICODE
        )
        
        emojis = emoji_pattern.findall(emoji_string)
        
        # Analyze each emoji
        for emoji in emojis:
            if emoji in self.EMOJI_EMOTIONS:
                emoji_count += 1
                for emotion, score in self.EMOJI_EMOTIONS[emoji].items():
                    if emotion in emotions:
                        emotions[emotion] = (emotions[emotion] + score) / 2
                    else:
                        emotions[emotion] = score
        
        # If no recognized emojis, return neutral
        if emoji_count == 0:
            return {"neutrality": 0.5, "curiosity": 0.3}
        
        # Add a general positivity/negativity score
        positive_emotions = ["happiness", "love", "excitement", "contentment", "friendliness"]
        negative_emotions = ["sadness", "anger", "fear", "disgust", "frustration"]
        
        pos_score = sum(emotions.get(e, 0) for e in positive_emotions) / len(positive_emotions)
        neg_score = sum(emotions.get(e, 0) for e in negative_emotions) / len(negative_emotions)
        
        emotions["positivity"] = pos_score
        emotions["negativity"] = neg_score
        
        # Add surprise factor based on emotion variety
        emotions["surprise"] = min(0.9, len(emotions) * 0.1)
        
        return emotions
    
    def get_dominant_emotion(self, emotions: Dict[str, float]) -> str:
        """Get the dominant emotion from emotion scores"""
        if not emotions:
            return "neutrality"
        
        # Exclude meta-emotions
        meta_emotions = ["positivity", "negativity", "surprise"]
        filtered_emotions = {k: v for k, v in emotions.items() if k not in meta_emotions}
        
        if not filtered_emotions:
            return "neutrality"
        
        return max(filtered_emotions, key=filtered_emotions.get)
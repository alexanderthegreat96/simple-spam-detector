import json
import time
import difflib
import re

class Spam:    
    DEFAULT_SPAM_MESSAGES = [
        "Get free Discord Nitro here!",
        "Claim your free Nitro with this link!",
        "Join this server for free Nitro giveaways!",
        "Your account has been compromised! Click here to verify.",
        "You've won a prize! Visit this link to claim it.",
        "To unlock premium features, click here.",
        "Join our server for free giveaways!",
        "Looking for active members! Join now!",
        "Get exclusive benefits by joining our server!",
        "Need Discord server moderation? Our bot can help!",
        "Boost your server's engagement with our bot!",
        "Customize your server with our bot's features!",
        "Invest in our cryptocurrency for guaranteed returns!",
        "Double your money with our investment scheme!",
        "Join our trading group for expert crypto advice!",
        "Check out this amazing website!",
        "Watch free movies online!",
        "Get free gift cards here!",
        "Participate in our giveaway to win Discord Nitro!",
        "Retweet and join our server to win prizes!",
        "Tag friends and follow to enter our giveaway!",
        "Check out my nudes",
        "Nudes free",
        "Get free Discord Nitro here!",
        "Claim your free Nitro with this link!",
        "Join this server for free Nitro giveaways!",
        "Your account has been compromised! Click here to verify.",
        "You've won a prize! Visit this link to claim it.",
        "To unlock premium features, click here.",
        "Join our server for free giveaways!",
        "Looking for active members! Join now!",
        "Get exclusive benefits by joining our server!",
        "Need Discord server moderation? Our bot can help!",
        "Boost your server's engagement with our bot!",
        "Customize your server with our bot's features!",
        "Invest in our cryptocurrency for guaranteed returns!",
        "Double your money with our investment scheme!",
        "Join our trading group for expert crypto advice!",
        "Check out this amazing website! ",
        "Get free gift cards here! ",
        "Participate in our giveaway to win Discord Nitro!",
        "Retweet and join our server to win prizes!",
        "Tag friends and follow to enter our giveaway!",
        "Check out my nudes!",
        "Join my premium Snapchat for exclusive content!",
        "Looking for a sugar daddy/mommy? DM me!",
        "Hot singles in your area! Click here!",
        "Want to see more? Subscribe to my OnlyFans!",
        "Join my server for NSFW content!",
        "I sell premium adult content, DM for more info!",
    ]
    
    def __init__(self, 
                 last_messages: int = 5,
                 message_interval: float = 0.77,
                 spam_threshold_time: int = 60,
                 similarity_score: float = 0.98,
                 optional_spam_messages: list = None,
                 ) -> None:
        
        self.messages = None
        self.__optional_spam_messages = optional_spam_messages
        
        self.__last_messages = last_messages
        self.__message_interval = message_interval
        self.__spam_threshold_time = spam_threshold_time
        self.__similarity_score = similarity_score
        
    
    def set_messages(self, messages: dict = {}) -> None:
        """Set the messages to be analyzed."""
        self.messages = messages
            
    def __check_message_structure(self, messages: dict) -> bool:
        """Check if the message structure is valid."""
        status = True
        if isinstance(messages, dict) and 'messages' in messages and isinstance(messages['messages'], list):
            for message in messages['messages']:
                if not (isinstance(message, dict) and all(key in message for key in ['message_id', 'message', 'timestamp'])):
                    status = False
                    break
                if not (isinstance(message['message_id'], int) and isinstance(message['message'], str) and isinstance(message['timestamp'], float)):
                    status = False
                    break
        else:
            status = False
        return status

        
    def __check_for_spam_messages(self, message_list: list = None) -> bool:
        """Check for spam messages in the given list."""
        if len(message_list):
            if self.__optional_spam_messages:
                for message in message_list[-self.__last_messages:]:
                    for spam_message in self.__optional_spam_messages:
                        matcher = difflib.SequenceMatcher(None, message['message'].lower(), spam_message.lower())
                        if matcher.ratio() >= 0.5:
                            print("Potential spam detected:", message['message'])
                            return True
            else:
                for message in message_list[-self.__last_messages:]:
                    for spam_message in self.DEFAULT_SPAM_MESSAGES:
                        matcher = difflib.SequenceMatcher(None, message['message'].lower(), spam_message.lower())
                        if matcher.ratio() >= 0.5:
                            print("Potential spam detected:", message['message'])
                            return True
        return False
    
    def __too_fast(self, cached_messages: list) -> bool:
        """Check if messages are sent too fast."""
        last_message_timestamp = cached_messages[-1]['timestamp']
        elapsed_time = time.time() - last_message_timestamp
        if elapsed_time > self.__message_interval:
            return True
    
    def __average_similarity(self, message1: str, message_list: list) -> float:
        """Calculate the average similarity of a message with a list of messages."""
        total_similarity = 0.0
    
        if len(message_list):
            for message2 in message_list:
                matcher = difflib.SequenceMatcher(None, message1.lower(), message2.lower())
                total_similarity += matcher.ratio()
            if message_list:
                return total_similarity / len(message_list)

        return 0.0
    
    def __has_links(self, cached_messages: list) -> bool:
        """Check if the messages have links."""
        count = 0
        for message in cached_messages[-self.__last_messages:]:
            if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message['message']):
                count += 1
        return count == self.__last_messages
    
    
    def __check_spam(self, cached_messages) -> bool:
        """Check for spam patterns in the given list of messages."""
        # Ensure we have enough messages to perform meaningful similarity checks
        if len(cached_messages) < self.__last_messages:
            return False

        similarity_scores = []
        for message in cached_messages[-self.__last_messages:]:
            similarity_score = self.__average_similarity(message['message'], [msg['message'] for msg in cached_messages[-self.__last_messages:]])
            similarity_scores.append(similarity_score)

        if max(similarity_scores) >= self.__similarity_score:
            last_similar_message_time = None
            for msg in reversed(cached_messages[-self.__last_messages:]):
                if msg['message'] == cached_messages[-1]['message']:
                    last_similar_message_time = msg['timestamp']
                    break

            if last_similar_message_time is not None:
                time_difference = time.time() - last_similar_message_time
                if time_difference <= self.__spam_threshold_time:
                    print("Potential spam detected:", cached_messages[-1]['message'])
                    return True

        return False

    
    def analyze(self) -> dict:
        """Analyze the messages for spam patterns."""
        print("Cached message:", self.messages)
        
        if self.messages:
            if self.__check_message_structure(self.messages):
                contents = self.messages['messages']

                detected_spam = False
                detection_type = None
                
                if self.__too_fast(contents):
                    detected_spam = True
                    detection_type = "too_fast"
                
                if self.__check_spam(contents):
                    detected_spam = True
                    detection_type = "message_spam_duplication"
                    
                if self.__has_links(contents):
                    detected_spam = True
                    detection_type = "last_messages_were_all_links"
                
                if self.__check_for_spam_messages(contents):
                    detected_spam = True
                    detection_type = "message_contains_forbidden_phrases"

                return {
                    'detected_spam': detected_spam, 
                    'should_wipe_cache': detected_spam, 
                    'detection_type': detection_type
                }
            else:
                print('Aborting spam check. Your messages structure is invalid!')
import datetime

class MoodTracker:
    """will handle mapping moods"""

    def __init__(self, calendar_service):
        self.calendar = calendar_service

        self.mood_map = {
            "1": {"name": "Very Happy", "color": "5"},
            "2": {"name": "Sort of Happy", "color": "2"},
            "3": {"name": "Neutral", "color": "8"},
            "4": {"name": "Uninterested", "color": "6"},
            "5": {"name": "Very Uniterested", "color": "1"}
        }
    
    def display_menu(self):

        for key, mood in self.mood_map.items():
            print(f"[{key}] {mood['name']}")

    def get_uer_input(self):
        
        self.display_menu()

        choice = input("\nHow is she feeling today? (1-5): ").strip()
        if choice not in self.mood_map:
            print("Selection cancelled: Invalid input.")
            return None, None
            
        notes = input("Any specific thoughts or reasons?: ").strip()
        return choice, notes

    # def log_mood(self):

    #     choice, notes = self.get_user_input




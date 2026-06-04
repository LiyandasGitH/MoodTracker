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

    def get_user_input(self):
        
        self.display_menu()

        choice = input("\nHow is she feeling today? (1-5): ").strip()
        if choice not in self.mood_map:
            print("Selection cancelled: Invalid input.")
            return None, None
            
        notes = input("Any specific thoughts or reasons?: ").strip()
        return choice, notes

    def log_mood(self):

        choice, notes = self.get_user_input()

        if choice:
            selected_mood = self.mood_map[choice]
            event_data = self._format_event(selected_mood, notes)

            try:
                result = self.calendar.add_event(event_data)
                print(f"\nSuccessfully logged: {selected_mood['name']}")
                print(f"Link: {result.get('htmlLink')}")

            except Exception as e:
                print(f"\nFailed to log mood. Error: {e}")

    def _format_event(self, mood_data, notes):
        """
        Private helper to format the dictionary exactly 
        as the Google Calendar API expects.
        """
        today = datetime.date.today().isoformat()
        
        return {
            'summary': f"Mood: {mood_data['name']}",
            'description': notes if notes else "No notes provided.",
            'start': {'date': today},
            'end': {'date': today},
            'color': mood_data['color'],
            'transparency': 'transparent', # Sets as 'Free' so it doesn't block your schedule
            'reminders': {'useDefault': False}
        }

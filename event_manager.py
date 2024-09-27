class EventManager:
    def __init__(self):
        self.events = {}  # Dictionnaire pour stocker les événements et les callbacks associés

    def register_event(self, event_type):
        """Enregistre un nouveau type d'événement."""
        if event_type not in self.events:
            self.events[event_type] = []  # Initialise une liste vide de callbacks pour ce type d'événement

    def register_callback(self, event_type, callback):
        """Enregistre un callback pour un événement spécifique."""
        if event_type in self.events:
            self.events[event_type].append(callback)
        else:
            raise ValueError(f"Événement non enregistré : {event_type}")

    def trigger_event(self, event_type, *args, **kwargs):
        """Déclenche l'événement et appelle les callbacks associés."""
        if event_type in self.events:
            for callback in self.events[event_type]:
                callback(*args, **kwargs)  # Appelle le callback avec les arguments passés
        else:
            raise ValueError(f"Événement non enregistré : {event_type}")

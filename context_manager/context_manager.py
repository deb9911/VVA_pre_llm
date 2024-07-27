import json
import os


class ContextManager:
    def __init__(self, context_file='context.json'):
        self.context_file = context_file
        self.context = {}
        if os.path.exists(self.context_file):
            self.load_context()

    def load_context(self):
        with open(self.context_file, 'r') as file:
            self.context = json.load(file)

    def save_context(self):
        with open(self.context_file, 'w') as file:
            json.dump(self.context, file, indent=4)

    def get(self, key, default=None):
        return self.context.get(key, default)

    def set(self, key, value):
        self.context[key] = value
        self.save_context()

    def update(self, updates):
        self.context.update(updates)
        self.save_context()

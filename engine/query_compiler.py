import os

from engine.engine import Engine


class Compiled_Query:
    def query_fixer(self, query_str):
        initial_comment = "So you want to search for" + query_str
        Engine.Speak(initial_comment)
        user_confirmation = Engine.take_command()
        if user_confirmation == 'no' or user_confirmation == 'change it':
            correction_comment = "So what need to change for this query"
            Engine.Speak(correction_comment)
            corrcted_query = Engine.take_command()
            return corrcted_query
        else:
            return query_str


CQ = Compiled_Query()


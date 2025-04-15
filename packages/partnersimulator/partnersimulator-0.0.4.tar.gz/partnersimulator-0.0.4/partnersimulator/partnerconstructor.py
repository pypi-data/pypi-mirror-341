from openai import OpenAI
import polars as pl
import os

client = OpenAI(api_key='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') #leaving this as is for now but please don't abuse my kindness

class partner:
    def __init__(self, name, age, gender, mood, affection):
        self.name = name
        self.age = age
        self.gender = gender
        self.mood = mood
        self.affection = affection
        self.json_path = f'{self.name}{self.age}.json'

        if self.age < 18:
            raise RuntimeError(f'An age of {self.age} is too young!')

    def __str__(self):
        return f'{self.name}, {self.age}, {self.gender} {self.mood}, {self.affection}'

    def read_chat_history(self):
        if not os.path.exists(self.json_path):
            df = pl.DataFrame({
                'role': ['user'],
                'content': ['']
            })
            df.write_json(self.json_path)
        existing_df = pl.read_json(self.json_path)
        return existing_df

    def write_chat_history(self, prompt, message):
        history_df = self.read_chat_history()
        addendum_df = pl.DataFrame({
            'role' : ['user', 'system'],
            'content': [prompt, message]
        })
        combined_df = pl.concat([history_df, addendum_df], how='vertical_relaxed')
        combined_df.write_json(self.json_path)

    def send_message(self, prompt):
        response = client.responses.create(
            model='gpt-4.1',
            input=[
                {
                    'role': 'system',
                    'content': f'''Take on the role of a romantic partner. Your attributes are as follows:
                                name: {self.name},
                                age: {self.age} year(s) old,
                                gender: {self.gender},
                                mood {self.mood},
                                affection: {self.affection}/100.
                                Respond to the prompt according to these attributes. Make sure the style, tone, and language are in line with the attributes i gave you. Tailor the response to each attribute'''
                },
                {
                    'role': 'system',
                    'content': f'{self.read_chat_history()}'
                },
                {
                    'role': 'user',
                    'content': f'{prompt}'
                }
            ]
        )
        self.write_chat_history(prompt, response.output_text)
        return response.output_text
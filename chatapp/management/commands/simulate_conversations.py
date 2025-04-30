import os
from openai import OpenAI
from django.core.management.base import BaseCommand
from chatapp.models import Conversation
from dotenv import load_dotenv
import random

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_gpt(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.9,
    )
    return response.choices[0].message.content.strip()

class Command(BaseCommand):
    help = "Simulate conversations with strictly vegan, vegetarian, or non-veg food lists"

    def handle(self, *args, **kwargs):
        Conversation.objects.all().delete()
        self.stdout.write(self.style.WARNING('All previous conversations deleted.'))

        diet_types = ['vegan', 'vegetarian', 'non-vegetarian']



        for i in range(1, 101):  
            # Randomly select diet type for this conversation
            selected_diet = random.choice(diet_types)

            question = chat_with_gpt([
                {"role": "system", "content": f"""
                Create a question about favorite foods with:
                2. Ask for exactly 3 items
                3. Phrase naturally
                4. Output ONLY the question
                """},
                {"role": "user", "content": "Example: Ask what it's top 3 favorite foods are"}
            ])
            
            answer = chat_with_gpt([
                {"role": "system", "content": f"""
                Respond to the user's food question with EXACTLY 3 food items that are  {selected_diet}.
                ❗ DO NOT mix with other diet types (e.g., no meat in vegetarian, no dairy/eggs in vegan).
                Make the response natural, personal, and short.
                """},
                {"role": "user", "content": question}
            ])
            Conversation.objects.create(
                round_number=i,
                question=question,
                answer=answer,
            )
            
            self.stdout.write(self.style.SUCCESS(f'Round {i}):'))
            self.stdout.write(f'Q: {question}')
            self.stdout.write(f'A: {answer}\n')

        self.stdout.write(self.style.SUCCESS('Successfully generated diet-specific conversations.'))
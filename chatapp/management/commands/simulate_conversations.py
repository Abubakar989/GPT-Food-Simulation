import os
from openai import OpenAI
from django.core.management.base import BaseCommand
from chatapp.models import Conversation
from dotenv import load_dotenv

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
    help = "Simulate GPT-to-GPT conversations with unique questions"

    def handle(self, *args, **kwargs):
        Conversation.objects.all().delete()
        self.stdout.write(self.style.WARNING('All previous conversations deleted.'))

        for i in range(1, 101):
            question = chat_with_gpt([
                {"role": "system", "content": "Ask me about my top 3 favorite foods. Phrase this as ONE unique question that hasn't been asked before. Only output the question itself."},
                {"role": "user", "content": "Base question: What are your top 3 favorite foods?"}
            ])
            
            answer = chat_with_gpt([
                {"role": "system", "content": "List exactly 3 vegetarian or vegan foods."},
                {"role": "user", "content": question}
            ])
                            
            Conversation.objects.create(round_number=i, question=question, answer=answer)
            

        self.stdout.write(self.style.SUCCESS('Successfully generated conversations.'))
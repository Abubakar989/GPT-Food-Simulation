from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .models import Conversation
from .food_classifier import extract_food_names, classify_food_items


class VegVeganUserList(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Vegetarian/Vegan"],
        operation_summary="Classify and extract food names",
        operation_description="Classifies gpt response into vegan, vegetarian, or non-vegetarian and extracts relevant food names. Returns only vegetarian and vegan entries."
    )
    def get(self, request):
        conversations = Conversation.objects.all()
        results = []

        for convo in conversations:
            answer_text = convo.answer

            inferred_type = self.detect_label_from_text(answer_text)

            if inferred_type not in ["vegan", "vegetarian", "non-vegetarian"]:
                inferred_type = classify_food_items([answer_text])

            if inferred_type in ["vegan", "vegetarian"]:
                food_names = extract_food_names(answer_text)

                results.append({
                    "round": convo.round_number,
                    "question": convo.question,
                    "answer": convo.answer,
                    "foods": food_names,
                    "type": inferred_type
                })

        return Response({
            "count": len(results),
            "results": results
        })

    def detect_label_from_text(self, text):
        text = text.lower()
        if "non-vegetarian" in text:
            return "non-vegetarian"
        if "vegan" in text:
            return "vegan"
        if "vegetarian" in text:
            return "vegetarian"
        return None

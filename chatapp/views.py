from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from chatapp.models import Conversation
from chatapp.utils import extract_foods_from_text

class VegVeganUserList(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Vegetarian/Vegan"],
        operation_summary="List simulated users who mentioned vegetarian or vegan diets",
        operation_description="Filters conversation data to return users who mentioned 'vegan' or 'vegetarian' in their answers. Also extracts top 3 foods mentioned."
    )
    def get(self, request):
        conversations = Conversation.objects.all()
        results = []
        for convo in conversations:
            lower = convo.answer.lower()
            if "vegan" in lower or "vegetarian" in lower:
                foods = extract_foods_from_text(convo.answer)
                results.append({
                    "round": convo.round_number,
                    "diet_mentioned": "vegan" if "vegan" in lower else "vegetarian",
                    "top_3_foods": foods,
                    "question": convo.question,
                    "answer": convo.answer
                })
        return Response(results)

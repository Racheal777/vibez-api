from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class SignupView(APIView):

    def post(self, request):
        return Response
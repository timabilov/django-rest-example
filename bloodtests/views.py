
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.response import Response

from bloodtests.models import Test
from bloodtests.serializers import TestSerializer


# we can have the same logic here. difference will on our customized create-or-update behaviour
# class TestDetails(ModelViewSet):

#     queryset = Test
#     serializer_class = TestSerializer


# MedicalTestAPIView
class TestDetailsAPIView(views.APIView):

    def get(self, request, code):
        """Get particular test data"""
        test_instance = get_object_or_404(Test, code=code)
        serializer = TestSerializer(instance=test_instance)
        return Response(serializer.data, status=200)

    def post(self, request, code):
        """Create medical test data"""
        data = {
            **{
                'code': code
            },
            **request.data
        }
        existing = Test.objects.filter(code=code).first()

        # Current policy is update existing one. But this will work too.

        serializer = TestSerializer(data=data, instance=existing)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return JsonResponse(serializer.validated_data, status=200)

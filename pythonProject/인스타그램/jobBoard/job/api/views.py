from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from job.models import JobOffer
from job.api.serializers import JobOfferSerializer

class JobOfferListAPIView(APIView): #강의에서는 JobOfferListCreateAPIView라고 이름을 붙였는데 나는 Create를 빼는 것이 맞다고 생각한다.
    def get(self, request):
        jobs = JobOffer.objects.all() #강의에서는 .filter(available=True)로 했는데, 생각해보니 그렇게 쓰는 편이 좋겠다.
        serializer = JobOfferSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JobOfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobOfferDetailAPIView(APIView):
    def get_object(self, pk):
        job = get_object_or_404(JobOffer, pk=pk)
        return job

    def get(self, request, pk):
        job = self.get_object(pk)
        serializer = JobOfferSerializer(job)
        return Response(serializer.data)

    def put(self, request, pk):
        job = self.get_object(pk)
        serializer = JobOfferSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        job = self.get_object(pk)
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
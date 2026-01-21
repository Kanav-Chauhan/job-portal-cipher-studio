from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer
from django.db.models import Count


class JobListCreate(APIView):
    def get(self, request):
        jobs = Job.objects.all().order_by("-created_at")
        return Response(JobSerializer(jobs, many=True).data)

    def post(self, request):
        serializer = JobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class JobDetail(APIView):
    def put(self, request, id):
        job = Job.objects.get(id=id)
        serializer = JobSerializer(job, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        Job.objects.get(id=id).delete()
        return Response({"deleted": True})

class JobDuplicate(APIView):
    def post(self, request, id):
        job = Job.objects.get(id=id)
        job.id = None
        job.save()
        serializer = JobSerializer(job)
        return Response(serializer.data, status=201)



class Analytics(APIView):
    def get(self, request):
        return Response({
            "status": Job.objects.values("status").annotate(count=Count("id")),
            "city": Job.objects.values("city").annotate(count=Count("id")),
            "state": Job.objects.values("state").annotate(count=Count("id")),
        })

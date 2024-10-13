from django.shortcuts import render
from job.models import Job, ApplyJob
from .filter import JobFilter


def home(request):
    filter = JobFilter(request.GET, queryset=Job.objects.filter(is_available=True).order_by('-timestamp'))
    context = {'filter': filter}
    return render(request, 'website/home.html', context)

def job_listing(request):
    jobs = Job.objects.filter(is_available=True).order_by('-timestamp')
    context = {'jobs': jobs}
    return render(request, 'website/job_listing.html', context)
    
def job_details(request, pk):
    job = Job.objects.get(pk=pk)
    industry = job.industry
    related_jobs = Job.objects.filter(industry=industry).exclude(id=job.id).order_by('-timestamp')[:3]
    if request.user.is_authenticated:
        if ApplyJob.objects.filter(user = request.user, job = pk).exists():
           has_applied = True
        else:
           has_applied = False
        job = Job.objects.get(pk=pk)
        context = {'job':job, 'has_applied':has_applied, 'related': related_jobs}  
        return render(request, 'website/job_details.html', context)
    else:
        job = Job.objects.get(pk=pk)
        context = {'job':job, 'related': related_jobs}  
        return render(request, 'website/job_details.html', context)

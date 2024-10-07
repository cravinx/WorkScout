from django.shortcuts import render, redirect
from .models import Job, ApplyJob
from .form import CreateJobForm, UpdateJobForm
from django.contrib import messages
from django.core.mail import send_mail

#  create job
def create_job(request):
    if request.user.is_authenticated and  request.user.is_recruiter and request.user.has_company:
        if request.method == 'POST':
            form = CreateJobForm(request.POST)
            if form.is_valid():
                var = form.save(commit=False)
                var.user = request.user
                var.company = request.user.company
                var.save()
                messages.info(request, 'New job has been created')
                return redirect('dashboard')
            else:
                messages.warning(request, 'Something went wrong')
        else:
            form = CreateJobForm
            context = {'form': form}
            return render(request, 'job/create_job.html', context)
    else:
        messages.warning(request, 'Permission Denied')
        return redirect('home')
    
def update_job(request, pk):
    if request.user.is_authenticated and  request.user.is_recruiter and request.user.has_company:
        job = Job.objects.get(pk=pk)
        if request.method == 'POST':
            form = UpdateJobForm(request.POST, instance=job)
            if form.is_valid():
                form.save()
                messages.info(request, 'Job details have been updated')
                return redirect('dashboard')
            else:
                messages.warning(request, 'Something went wrong')
        else:
            form = UpdateJobForm(instance=job)
            context = {'form': form}
            return render(request, 'job/update_job.html', context)
    else:
        messages.warning(request, 'Permission Denied')
        return redirect('home')
        
def manage_jobs(request):
    if request.user.is_authenticated and  request.user.is_recruiter and request.user.has_company:
        jobs = Job.objects.filter(user = request.user, company = request.user.company).order_by('-timestamp')
        context = {'jobs':jobs}
        return render(request, 'job/manage_jobs.html', context)
    else:
        messages.warning(request, 'Permission Denied')
        return redirect('home')

def apply_email(request, pk):
     if request.user.is_authenticated and  request.user.is_applicant and request.user.has_resume:
        job = Job.objects.get(pk=pk)
        applicant = request.user.email
        employer = job.user.email

        subject = 'Application Update'
        message = {"employer":f'{applicant} just applied for {job.title}',
        "employee":f'You have successfully applied for {job.title}'}
        from_email = "unegbuprecious25@gmail.com"
        recipient_list = [{applicant}, {employer} ]

        send_mail(subject, message['employee'], from_email, recipient_list[0], fail_silently=False)
        send_mail(subject, message['employer'], from_email, recipient_list[1], fail_silently=False)

        messages.info(request, 'You have successfully applied! Please see dashboard')
        return redirect('dashboard')
     
def apply_to_job(request, pk):
    if request.user.is_authenticated and request.user.is_applicant:
        job = Job.objects.get(pk=pk)
        if ApplyJob.objects.filter(user = request.user, job = pk).exists():
            messages.warning(request, 'Permission Denied')
            return redirect('home')
        else:
            ApplyJob.objects.create(
                job = job,
                user = request.user,
                is_pending = True
            )
            # messages.info(request, 'You have successfully applied! Please see dashboard')
            return redirect(f'apply-email/{pk}')
    else:
        messages.info(request, 'Please login to continue')
        return redirect('login')
    
def all_applicants(request, pk):
    if request.user.is_authenticated and  request.user.is_recruiter and request.user.has_company:
        job = Job.objects.get(pk=pk)
        applicants = job.applyjob_set.all().order_by('-timestamp')
        context = {'job':job, 'applicants': applicants}
        return render(request, 'job/all_applicants.html', context)
    else:
        messages.warning(request, 'Permission Denied')
        return redirect('home')

def applied_jobs(request):
    if request.user.is_authenticated and request.user.is_applicant:
        jobs = ApplyJob.objects.filter(user = request.user).order_by('-timestamp')
        context = {'jobs':jobs}
        return render(request, 'job/applied_jobs.html', context)
    else:
        messages.info(request, 'Please login to continue')
        return redirect('login')

# def respond_email(request, pk):
#      if request.user.is_authenticated and  request.user.is_recruiter and request.user.has_company:
#         job = Job.objects.get(pk=pk)
#         applicants = job.applyjob_set.all().order_by('-timestamp')
#         context = {'job':job, 'applicants': applicants}
        
#         if request.method == 'POST':
#             response = request.POST.get('response') or ''
#             user = request.POST['username']
#             employer = job.user.email
#             applicant = job.applyjob_set.get(user = user).user

#             subject = 'Application Response Update'
#             message = {"employer":f'This is a confirmation and reminder that your response for {job.title} was recorded and sent to {applicant}',
#             "applicant":f'Your application to {job.title} has received the following response: {response}'}
#             from_email = "unegbuprecious25@gmail.com"
#             recipient_list = [{applicant}, {employer} ]
    
#             send_mail(subject, message['applicant'], from_email, recipient_list[0], fail_silently=False)
#             send_mail(subject, message['employer'], from_email, recipient_list[1], fail_silently=False)

#             return redirect(f'response/{pk}')
        
def response(request, pk):
    if request.user.is_authenticated and  request.user.is_recruiter and request.user.has_company:
        job = Job.objects.get(pk=pk)
        applicants = job.applyjob_set.all().order_by('-timestamp')
        context = {'job':job, 'applicants': applicants}
        
        if request.method == 'POST':
            response = request.POST.get('response') or ''
            user = request.POST['username']
            applicant = job.applyjob_set.get(user = user)
            if response == 'Accept':
                applicant.user.id = user
                applicant.is_accepted = True
                applicant.is_declined = False
                applicant.is_pending = False
                applicant.save()
                messages.info(request, 'Your reponse has been recorded and forwarded to applicant. ')
                return render(request, 'job/all_applicants.html', context)
        
            elif response == 'Decline':
                applicant.user.id = user
                applicant.is_declined = True
                applicant.is_accepted = False
                applicant.is_pending = False
                applicant.save()
                messages.info(request, 'Your reponse has been recorded and forwarded to applicant. ')
                return render(request, 'job/all_applicants.html', context)
        
            else:
                applicant.user.id = user
                applicant.is_pending = True
                applicant.is_accepted = False
                applicant.is_declined = False
                applicant.save()
                messages.info(request, 'No reponse was recorded and response is still set to pending. ')
                return render(request, 'job/all_applicants.html', context)
        else: 
            messages.info(request, 'No response recorded yet, please select a response below.')
    else:
        messages.warning(request, 'Permission Denied')
        return redirect('home')


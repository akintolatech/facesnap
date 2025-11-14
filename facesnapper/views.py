from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from facesnapper.forms import FileUploadForm
from facesnapper.models import Student, StudentClass
import pandas as pd


# Create your views here.
def onboard(request):
    return render(request, 'facesnapper/onboarding.html')

def dashboard(request):
    classes = StudentClass.objects.annotate(
        total_students=Count('student'),
        captured_students=Count('student', filter=Q(student__captured=True))
    )

    total_students = Student.objects.count()
    total_captured_students = Student.objects.filter(captured=True).count()
    total_progress_percentage = (total_captured_students / total_students * 100) if total_students > 0 else 0

    context = {
        'classes': classes,
        "total_students": total_students,
        "total_captured_students": total_captured_students,
        "total_progress_percentage": total_progress_percentage
    }
    return render(request, 'facesnapper/dashboard.html', context)


def student_list(request, class_id):
    student_class = StudentClass.objects.get(pk=class_id)
    students = Student.objects.filter(class_category=class_id)
    captured_students = students.filter(captured=True)
    uncaptured_students = students.filter(captured=False)

    total_students = students.count()
    total_captured = captured_students.count()
    progress_percentage = (total_captured / total_students * 100) if total_students else 0

    context = {
        "student_class": student_class,
        "total_students_per_class": total_students,
        "total_students_per_class_with_passport": total_captured,
        "progress_percentage": progress_percentage,
        "captured_students": captured_students,
        "uncaptured_students": uncaptured_students,
    }
    return render(request, 'facesnapper/list.html', context)



def capture(request, student_id):
    context = {
        "student": get_object_or_404(Student, pk=student_id),
    }
    return render(request, 'facesnapper/capture.html', context)


@csrf_exempt  # only if you don't use the csrf token in JS; safer to keep it and use {{ csrf_token }}
def upload_photo(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        student = get_object_or_404(Student, pk=student_id)
        photo = request.FILES.get('photo')

        if not photo:
            return JsonResponse({'status': 'error', 'message': 'No photo uploaded'})

        # Save photo to model's ImageField
        student.photo.save(f"{student.name}.jpg", photo, save=True)

        # Set captured to True
        student.captured = True

        # Save the student instance
        student.save()

        # Redirect URL
        success_url = f"/success/{student.id}/"
        return JsonResponse({'status': 'success', 'redirect_url': success_url})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def upload_success(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    return render(request, 'facesnapper/success.html', {'student': student})


def upload_students(request, class_id):
    student_class = get_object_or_404(StudentClass, pk=class_id)

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']

            # Determine file type
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:  # assume .xlsx
                df = pd.read_excel(uploaded_file)

            # Loop through each row and create Student
            for _, row in df.iterrows():
                adm_no = str(row.get('AdmissionNo', '')).strip()
                name = str(row.get('FullName', '')).strip()

                if adm_no and name:
                    Student.objects.get_or_create(
                        adm_no=adm_no,
                        name=name,
                        class_category=student_class
                    )
            return redirect('facesnapper:dashboard')
    else:
        form = FileUploadForm()

    context = {
        "upload_class": student_class,
        "upload_form": form,
    }
    return render(request, 'facesnapper/upload.html', context)

from django.shortcuts import render, redirect
from django.db.models import Avg
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
import json
from accounts.models import User
from .models import Review, Hospital, Doctor, Appointment

def home(request):
    return HttpResponse(
        "<h1>SehatSetu backend is running</h1>"
        "<p>Use <a href='/api/hospitals/'>/api/hospitals/</a> to access hospital data.</p>",
        content_type='text/html'
    )

def hospital_detail(request, hospital_id):
    hospital = Hospital.objects.get(id=hospital_id)

    reviews = Review.objects.filter(hospital=hospital)

    avg_rating = reviews.aggregate(avg=Avg('rating_overall'))['avg']
    hospital.rating_avg = round(avg_rating, 1) if avg_rating else 0

    return render(request, "hospital_detail.html", {
        "hospital": hospital,
        "reviews": reviews
    })

@require_GET
def hospitals_list(request):
    """API endpoint to get list of hospitals with optional filtering"""
    hospitals = Hospital.objects.all()

    # Filtering
    hospital_type = request.GET.get('type')
    if hospital_type in ['private', 'government']:
        hospitals = hospitals.filter(type=hospital_type)

    location = request.GET.get('location')
    if location:
        hospitals = hospitals.filter(location__icontains=location)

    # Convert to list of dicts
    hospitals_data = []
    for hospital in hospitals:
        hospitals_data.append({
            'id': hospital.id,
            'name': hospital.name,
            'location': hospital.location,
            'type': hospital.type,
            'beds': hospital.beds,
            'specialties': hospital.get_specialties_list(),
            'facilities': hospital.get_facilities_list(),
            'price_range': hospital.price_range,
            'rating': float(hospital.rating),
            'contact_number': hospital.contact_number,
            'address': hospital.address,
            'photo': hospital.photo.url if hospital.photo else None,
        })

    return JsonResponse({'hospitals': hospitals_data})

@require_GET
def compare_hospitals(request):
    """API endpoint to get data for specific hospitals for comparison"""
    hospital_ids = request.GET.getlist('ids[]')
    if not hospital_ids or len(hospital_ids) > 3:
        return JsonResponse({'error': 'Please provide 1-3 hospital IDs'}, status=400)

    try:
        hospitals = Hospital.objects.filter(id__in=hospital_ids)
        hospitals_data = []
        for hospital in hospitals:
            hospitals_data.append({
                'id': hospital.id,
                'name': hospital.name,
                'location': hospital.location,
                'type': hospital.type,
                'beds': hospital.beds,
                'specialties': hospital.get_specialties_list(),
                'facilities': hospital.get_facilities_list(),
                'price_range': hospital.price_range,
                'rating': float(hospital.rating),
                'contact_number': hospital.contact_number,
                'address': hospital.address,
                'photo': hospital.photo.url if hospital.photo else None,
            })
        return JsonResponse({'hospitals': hospitals_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_GET
def doctors_list(request):
    """API endpoint to get list of doctors with optional filtering"""
    doctors = Doctor.objects.select_related('hospital').all()

    # Filtering
    specialty = request.GET.get('specialty')
    if specialty:
        doctors = doctors.filter(specialty__icontains=specialty)

    location = request.GET.get('location')
    if location:
        doctors = doctors.filter(location__icontains=location)

    hospital_id = request.GET.get('hospital_id')
    if hospital_id:
        doctors = doctors.filter(hospital_id=hospital_id)

    # Convert to list of dicts
    doctors_data = []
    for doctor in doctors:
        doctors_data.append({
            'id': doctor.id,
            'name': doctor.name,
            'photo': doctor.photo.url if doctor.photo else None,
            'location': doctor.location,
            'experience_years': doctor.experience_years,
            'specialty': doctor.specialty,
            'hospital': {
                'id': doctor.hospital.id,
                'name': doctor.hospital.name,
                'location': doctor.hospital.location,
            },
            'contact_number': doctor.contact_number,
            'email': doctor.email,
            'qualifications': doctor.qualifications,
            'rating': float(doctor.rating),
            'available_days': doctor.available_days,
            'consultation_fee': float(doctor.consultation_fee),
        })

    return JsonResponse({'doctors': doctors_data})

@require_GET
def doctor_detail_api(request, doctor_id):
    doctor = Doctor.objects.select_related('hospital').get(id=doctor_id)
    return JsonResponse({
        'id': doctor.id,
        'name': doctor.name,
        'photo': request.build_absolute_uri(doctor.photo.url) if doctor.photo else None,
        'location': doctor.location,
        'experience_years': doctor.experience_years,
        'specialty': doctor.specialty,
        'hospital': {
            'id': doctor.hospital.id,
            'name': doctor.hospital.name,
            'location': doctor.hospital.location,
        },
        'contact_number': doctor.contact_number,
        'email': doctor.email,
        'qualifications': doctor.qualifications,
        'rating': float(doctor.rating),
        'available_days': doctor.available_days,
        'consultation_fee': float(doctor.consultation_fee),
    })


@csrf_exempt
def register(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8') if isinstance(request.body, bytes) else request.body)
    except Exception:
        data = request.POST

    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    phone_number = data.get('phone') or data.get('phone_number', '')
    city = data.get('city', '')

    if not name or not email or not password:
        return JsonResponse({'error': 'Name, email, and password are required.'}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'A user with that email already exists.'}, status=400)

    first_name, *rest = name.split()
    last_name = ' '.join(rest) if rest else ''

    try:
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type='patient',
        )
        user.phone_number = phone_number or ''
        user.city = city or ''
        user.save()
        return JsonResponse({'success': True, 'id': user.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def doctor_detail(request, doctor_id):
    doctor = Doctor.objects.select_related('hospital').get(id=doctor_id)

    return render(request, "doctor_detail.html", {
        "doctor": doctor,
    })

def add_review(request):
    if request.method == "POST":
        hospital = Hospital.objects.get(id=request.POST.get("hospital_id"))

        Review.objects.create(
            hospital=hospital,
            rating_overall=request.POST.get("rating_overall"),
            cleanliness=request.POST.get("cleanliness"),
            waiting_time=request.POST.get("waiting_time"),
            cost_transparency=request.POST.get("cost_transparency"),
            facilities=request.POST.get("facilities"),
            comment=request.POST.get("comment"),
        )

    return redirect(f"/hospital/{request.POST.get('hospital_id')}/")

@csrf_exempt
def add_hospital(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        if request.content_type and request.content_type.startswith('multipart/form-data'):
            data = request.POST
        else:
            data = json.loads(request.body)

        hospital = Hospital.objects.create(
            name=data.get('name', '').strip(),
            location=data.get('location', '').strip(),
            type=data.get('type', 'private'),
            beds=int(data.get('beds', 0) or 0),
            specialties=data.get('specialties', '').strip(),
            facilities=data.get('facilities', '').strip(),
            price_range=data.get('price_range', '').strip(),
            rating=float(data.get('rating', 0.0) or 0.0),
            contact_number=data.get('contact_number', '').strip(),
            address=data.get('address', '').strip(),
            photo=request.FILES.get('photo') if request.FILES.get('photo') else None,
        )
        return JsonResponse({'success': True, 'id': hospital.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def add_doctor(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        if request.content_type and request.content_type.startswith('multipart/form-data'):
            data = request.POST
        else:
            data = json.loads(request.body)

        hospital_id = int(data.get('hospital_id', 0) or 0)
        hospital = Hospital.objects.get(id=hospital_id)

        doctor = Doctor.objects.create(
            name=data.get('name', '').strip(),
            location=data.get('location', '').strip(),
            experience_years=int(data.get('experience_years', 0) or 0),
            specialty=data.get('specialty', '').strip(),
            hospital=hospital,
            contact_number=data.get('contact_number', '').strip(),
            email=data.get('email', '').strip(),
            qualifications=data.get('qualifications', '').strip(),
            rating=float(data.get('rating', 0.0) or 0.0),
            available_days=data.get('available_days', '').strip(),
            consultation_fee=float(data.get('consultation_fee', 0.0) or 0.0),
            photo=request.FILES.get('photo') if request.FILES.get('photo') else None,
        )
        return JsonResponse({'success': True, 'id': doctor.id})
    except Hospital.DoesNotExist:
        return JsonResponse({'error': 'Hospital ID not found.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def delete_hospital(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        if request.content_type and request.content_type.startswith('multipart/form-data'):
            data = request.POST
        else:
            data = json.loads(request.body)

        hospital_id = int(data.get('hospital_id', 0) or 0)
        hospital = Hospital.objects.get(id=hospital_id)
        hospital.delete()
        return JsonResponse({'success': True})
    except Hospital.DoesNotExist:
        return JsonResponse({'error': 'Hospital ID not found.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def delete_doctor(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        if request.content_type and request.content_type.startswith('multipart/form-data'):
            data = request.POST
        else:
            data = json.loads(request.body)

        doctor_id = int(data.get('doctor_id', 0) or 0)
        doctor = Doctor.objects.get(id=doctor_id)
        doctor.delete()
        return JsonResponse({'success': True})
    except Doctor.DoesNotExist:
        return JsonResponse({'error': 'Doctor ID not found.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def book_appointment(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        doctor_id = int(data.get('doctor_id', 0) or 0)
        doctor = Doctor.objects.get(id=doctor_id)

        appointment = Appointment.objects.create(
            doctor=doctor,
            patient_name=data.get('patient_name', '').strip(),
            patient_email=data.get('patient_email', '').strip(),
            patient_phone=data.get('patient_phone', '').strip(),
            appointment_date=data.get('appointment_date'),
            appointment_time=data.get('appointment_time'),
            reason=data.get('reason', '').strip(),
        )

        return JsonResponse({
            'success': True,
            'id': appointment.id,
            'doctor': doctor.name,
            'appointment_date': str(appointment.appointment_date),
            'appointment_time': str(appointment.appointment_time),
        })
    except Doctor.DoesNotExist:
        return JsonResponse({'error': 'Doctor ID not found.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_GET
def appointments_list(request):
    doctor_id = request.GET.get('doctor_id')
    email = request.GET.get('patient_email')
    appointments = Appointment.objects.select_related('doctor', 'doctor__hospital').all()

    if doctor_id:
        appointments = appointments.filter(doctor_id=doctor_id)
    if email:
        appointments = appointments.filter(patient_email__iexact=email)

    result = []
    for apt in appointments:
        result.append({
            'id': apt.id,
            'doctor': {
                'id': apt.doctor.id,
                'name': apt.doctor.name,
            },
            'hospital': {
                'id': apt.doctor.hospital.id,
                'name': apt.doctor.hospital.name,
            },
            'patient_name': apt.patient_name,
            'patient_email': apt.patient_email,
            'patient_phone': apt.patient_phone,
            'appointment_date': str(apt.appointment_date),
            'appointment_time': str(apt.appointment_time),
            'reason': apt.reason,
            'status': apt.status,
            'created_at': apt.created_at.isoformat(),
        })

    return JsonResponse({'appointments': result})
    
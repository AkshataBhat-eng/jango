import json
import re
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from myapp.models import Profile
from django.views.decorators.http import require_GET, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

def hello_world(request):
    return HttpResponse("hello World !!")

def ProfileView(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        address = request.POST.get('address', '')
        mobile = request.POST.get('mobile', '')
        email = request.POST.get('email', '')
        Profile.objects.create(name=name, address=address, mobile=mobile, email=email)
        return redirect('profile')
    else:
        stored_names = Profile.objects.all()
        context = {'stored_names': stored_names}
        return render(request, 'profile.html', context)

@require_GET   
def get_profile(request, name):
    try:
        target_profile = Profile.objects.get(name__iexact =name)
        data = {
            'id': target_profile.id,
            'name': target_profile.name,
            'address': target_profile.address,
            'mobile': target_profile.mobile
        }
        if target_profile:
            return JsonResponse(data, status=200)
        else:
            return JsonResponse({"error": f"Profile '{name}' not found"}, status=400)
    except ObjectDoesNotExist:
        return JsonResponse({"error": f"Profile '{name}' not found"}, status=404)
    except MultipleObjectsReturned:
        return JsonResponse({"error": f"Multiple profiles found for '{name}'. Please provide a more specific name."}, status=409) # 409 Conflict
    except Exception as e:
        return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)


@csrf_exempt
@require_http_methods(["PUT", "POST"])
def update_email(request, name):
    try:
        body = json.loads(request.body)
        email = body.get("email","").strip()

        if not email:
            return JsonResponse({"error": "Email is required"}, status=400)
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            return JsonResponse({"error": "Invalid email format."}, status=400)
        if not name or not name.strip():
            return JsonResponse({"error": "Name in URL is required."}, status=400)
        
        profile = Profile.objects.get(name__iexact = name)
        profile.email = email
        profile.save()

        data = {
            "id": profile.id,
            "name": profile.name,
            "email": profile.email
        }

        return JsonResponse(data, status=200)
    
    except Profile.DoesNotExist:
        return JsonResponse({"error": f"Profile '{name}' not found"},status=400)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)
    

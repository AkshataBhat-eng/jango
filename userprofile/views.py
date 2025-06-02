import re
from userprofile.models import UserProfile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core import serializers
import json

@csrf_exempt
def ProfileView(request):
    """
    Profile API View

    GET: Retrieve a list of all user profiles.
    POST: Create a new user profile with name and email.
    """
    if request.method == 'GET':
        profiles = UserProfile.objects.all()
        data = [{'id': profile.id, 'name': profile.name, 'email': profile.email} for profile in profiles]
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        body = json.loads(request.body)
        name = body.get('name', '').strip()
        email = body.get('email', '').strip()
        if not name:
            return JsonResponse({'error': 'Name is required.'}, status=400)
        if not email:
            return JsonResponse({'error': 'Email is required.'}, status=400)
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            return JsonResponse({'error': 'Invalid email format.'}, status=400)

        profile = UserProfile(name=name, email=email)
        profile.save()
        serialized_obj = serializers.serialize('json', [ profile, ])
        data = json.loads(serialized_obj)
        return JsonResponse({'message': 'Profile created successfully', 'data': data[0]})
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)
    

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def ProfileDetailView(request, pk):
    """
    Profile Detail API View

    GET: Retrieve a single user profile by primary key (id).
    PUT: Update the name and/or email of an existing profile by primary key.
    DELETE: Delete the profile by primary key.
    """
    try:
        profile = UserProfile.objects.get(id=pk)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': f'Profile not found with id {pk}'}, status=404)

    if request.method == 'GET':
        data = {
            'id': profile.id,
            'name': profile.name,
            'email': profile.email
        }
        return JsonResponse(data, status=200)

    elif request.method == 'PUT':
        try:
            body = json.loads(request.body)
            name = body.get('name', '').strip()
            email = body.get('email', '').strip()

            if not name and not email:
                return JsonResponse({'error': 'At least one of name or email is required to update.'}, status=400)

            if email:
                email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if not re.match(email_regex, email):
                    return JsonResponse({'error': 'Invalid email format.'}, status=400)
                profile.email = email

            if name:
                profile.name = name

            profile.save()

            updated_data = {
                'id': profile.id,
                'name': profile.name,
                'email': profile.email
            }
            return JsonResponse({'message': 'Profile updated successfully.', 'data': updated_data}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON body.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)
        
    elif request.method == 'DELETE':
        profile.delete()
        return JsonResponse({'message': f'Profile with id {pk} deleted successfully.'}, status=200)

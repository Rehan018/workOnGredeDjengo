import requests
from django.http import JsonResponse, HttpResponseBadRequest
from .models import User

def user_search(request):
    first_name = request.GET.get('first_name')
    

    if not first_name:
        return HttpResponseBadRequest('The "first_name" parameter is required.')

    matching_users = User.objects.filter(first_name__istartswith=first_name)
    if matching_users.exists():
        users_data = [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'age': user.age,
            'gender': user.gender,
            'email': user.email,
            'phone': user.phone,
            'birth_date': user.birth_date.strftime('%Y-%m-%d')
        } for user in matching_users]
    else:

        url = f'https://dummyjson.com/users/search?q={first_name}'
        response = requests.get(url)
        response_data = response.json()

        if isinstance(response_data, dict) and 'data' in response_data:
            users_data = response_data['data']
        else:
            users_data = []

        if not users_data:
            return JsonResponse({
                'users': [],
                'total': 0,
                'skip': 0,
                'limit': 0
            })

        # Save the new users to the database
        for user_data in users_data:
            User.objects.create(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                age=user_data['age'],
                gender=user_data['gender'],
                email=user_data['email'],
                phone=user_data['phone'],
                birth_date=user_data['birth_date']
            )

    return JsonResponse({'users': users_data}, safe=False)

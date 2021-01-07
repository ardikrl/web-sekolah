from django.contrib.auth import get_user_model

from .models import Staff


def staff_processor(request):
    UserModel = get_user_model()
    data = {}
    path_info = request.META["PATH_INFO"]
    if ("admin/" in path_info) and (request.user.is_staff):
        try:
            staff = Staff.objects.get(user=request.user)
            data["typestaff"] = staff.type_staff
        except Staff.DoesNotExist:
            data["typestaff"] = 'teu aya'

    return data

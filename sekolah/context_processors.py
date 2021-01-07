from django.contrib.auth import get_user_model

from .models import Staff, Guru


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


def guru_processor(request):
    UserModel = get_user_model()
    data = {}
    path_info = request.META["PATH_INFO"]
    if ("admin/" in path_info and request.user.is_authenticated):
        try:
            guru = Guru.objects.get(user=request.user)
            data["isguru"] = True
        except Guru.DoesNotExist:
            data["isguru"] = False

    return data

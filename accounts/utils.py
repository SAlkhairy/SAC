from django.core.exceptions import ObjectDoesNotExist

def get_user_ar_full_name(user):
    try:
        return user.profile.get_ar_full_name()
    except (ObjectDoesNotExist, AttributeError):
        return

def get_user_ar_short_name(user):
    try:
        return user.profile.get_ar_short_name()
    except (ObjectDoesNotExist, AttributeError):
        return

def get_user_en_full_name(user):
    try:
        return user.profile.get_en_full_name()
    except (ObjectDoesNotExist, AttributeError):
        return

def get_user_en_short_name(user):
    try:
        return user.profile.get_en_short_name()
    except (ObjectDoesNotExist, AttributeError):
        return

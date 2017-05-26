import StringIO
import qrcode
import qrcode.image.svg
from django.db import models
import operator

BASIC_SEARCH_FIELDS = ['user__username', 'user__email',
                       'user__profile__en_first_name',
                       'user__profile__en_middle_name',
                       'user__profile__en_last_name',
                       'user__profile__ar_first_name',
                       'user__profile__ar_middle_name',
                       'user__profile__ar_last_name',
                       'user__profile__student_id',
                       'user__profile__mobile_number']

def get_ticket(user):
    qrcode_output = StringIO.StringIO()
    qrcode.make(user.pk, image_factory=qrcode.image.svg.SvgImage, version=3).save(qrcode_output)
    qrcode_value = str(user.pk).join(qrcode_output.getvalue().split('\n')[1:])
    return qrcode_value

def get_search_queryset(queryset, search_fields, search_term):
    # Based on the Django app search functionality found in the
    # function get_search_results of django/contrib/admin/options.py.
    if search_term:
        orm_lookups = [search_field + '__icontains'
                       for search_field in search_fields]
        for bit in search_term.split():
            or_queries = [models.Q(**{orm_lookup: bit})
                          for orm_lookup in orm_lookups]
            queryset = queryset.filter(reduce(operator.or_, or_queries))

    return queryset


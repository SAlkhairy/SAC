from voting.models import SACYear


def sac_year(request):
    return {'sac_year': SACYear.objects.get_current()}

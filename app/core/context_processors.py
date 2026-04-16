import logging

from django.db.utils import DatabaseError, OperationalError

from core.models import ClubSettings

logger = logging.getLogger(__name__)


def branding(_request):
    try:
        settings_obj = ClubSettings.get_solo()
    except (DatabaseError, OperationalError) as exc:
        logger.warning('No se pudo cargar ClubSettings en context processor: %s', exc)
        settings_obj = ClubSettings()

    return {
        'club_settings': settings_obj,
    }

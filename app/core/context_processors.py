import logging
from django.db.utils import DatabaseError, OperationalError
from core.models import ClubSettings

logger = logging.getLogger(__name__)


def branding(_request):
    try:
        cfg = ClubSettings.get_solo()
    except (DatabaseError, OperationalError) as exc:
        logger.warning('No se pudo cargar ClubSettings en context processor: %s', exc)
        cfg = ClubSettings()

    try:
        theme_vars = cfg.theme_vars
    except Exception:
        from core.models import THEMES
        theme_vars = THEMES['literario_cafe']

    return {
        'club_settings': cfg,
        'theme_vars': theme_vars,
    }
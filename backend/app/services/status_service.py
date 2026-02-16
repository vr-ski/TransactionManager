"""
Status service.

Provides enriched status information including code, color, and
localized display name.
"""

from app.domain.value_objects import StatusOption, StatusPresentation
from app.repositories.status_repo import StatusRepository


class StatusService:
    """Service for retrieving and presenting transaction status metadata."""

    def __init__(self, status_repo: StatusRepository):
        self.status_repo = status_repo

    def get_presentation(self, status_id: int, lang: str = "en"):
        """
        Return a combined status presentation object containing:
        - code
        - display label (localized)
        - color
        """
        status = (
            self.status_repo.get_by_id(status_id)
            if hasattr(self.status_repo, "get_by_id")
            else None
        )

        if not status:
            return None

        color = self.status_repo.get_color(status_id)
        translation = self.status_repo.get_translation(status_id, lang)

        return StatusPresentation(
            code=status.code,
            display_name=translation.display_name if translation else status.code,
            color=color.color if color else "gray",
        )

    def get_all_options(self, lang: str = "en") -> list[StatusOption]:
        """
        Return all statuses with id, code, display name, and color.
        """
        statuses = self.status_repo.get_all()
        colors = {c.status_id: c.color for c in self.status_repo.get_all_colors()}
        translations = {}
        all_translations = self.status_repo.get_all_translations()
        for t in all_translations:
            if t.language_code == lang:
                translations[t.status_id] = t.display_name

        result = []
        for status in statuses:
            display_name = translations.get(status.status_id, status.code)
            color = colors.get(status.status_id, "#000000")
            result.append(
                StatusOption(
                    status_id=status.status_id,
                    code=status.code,
                    display_name=display_name,
                    color=color,
                )
            )
        return result

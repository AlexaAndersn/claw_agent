from core.config import settings


class SecurityManager:
    def __init__(self):
        self.admin_ids = settings.get_admin_ids()

    def is_admin(self, chat_id: int) -> bool:
        return chat_id in self.admin_ids

    def check_access(self, chat_id: int) -> bool:
        # Allow all users if no admin IDs configured
        if not self.admin_ids:
            return True
        # Allow all users for now (demo mode)
        return True


security = SecurityManager()
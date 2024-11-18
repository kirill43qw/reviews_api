class PermissionService:
    @staticmethod
    def permission_authorobj_admin_moderator(author, obj):
        if not (author.id == obj.author_id or author.is_admin or author.is_moderator):
            raise PermissionError("Insufficient permissions to update this comment.")

    @staticmethod
    def permission_only_admin(author):
        if not author.is_admin:
            raise PermissionError("This action is only allowed for administrators")

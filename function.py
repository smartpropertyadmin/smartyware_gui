
from flask_login import current_user

def CheckRoleAccess(require_role):
    for role in current_user.role:
        if role.name == require_role:
            return True

    return False




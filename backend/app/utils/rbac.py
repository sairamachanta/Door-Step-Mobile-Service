from fastapi import Depends, HTTPException, status
from typing import List, Callable
from .dependencies import get_current_active_user
from ..models import User


def has_role(required_roles: List[str]) -> Callable:
    """
    Dependency factory that checks if the current user has one of the required roles.
    Roles: 'admin' (superadmin), 'technician', 'customer'
    """
    async def role_checker(current_user: User = Depends(get_current_active_user)):
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {required_roles}"
            )
        return current_user

    return role_checker


# Reusable role dependencies
# DB roles: admin (superadmin tier), technician, customer
admin_only = has_role(["admin"])
technician_or_higher = has_role(["admin", "technician"])
all_authenticated = has_role(["admin", "technician", "customer"])

# Legacy aliases for backward compat
admin_or_higher = admin_only
super_admin_only = admin_only

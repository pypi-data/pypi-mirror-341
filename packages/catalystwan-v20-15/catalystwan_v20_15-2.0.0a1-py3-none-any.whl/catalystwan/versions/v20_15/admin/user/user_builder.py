# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .active_sessions.active_sessions_builder import ActiveSessionsBuilder
    from .admin.admin_builder import AdminBuilder
    from .lock_user.lock_user_builder import LockUserBuilder
    from .password.password_builder import PasswordBuilder
    from .profile.profile_builder import ProfileBuilder
    from .remove_sessions.remove_sessions_builder import RemoveSessionsBuilder
    from .reset.reset_builder import ResetBuilder
    from .role.role_builder import RoleBuilder
    from .user_auth_type.user_auth_type_builder import UserAuthTypeBuilder


class UserBuilder:
    """
    Builds and executes requests for operations under /admin/user
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get all users
        GET /dataservice/admin/user

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/admin/user", return_type=List[Any], **kw
        )

    def post(self, payload: Any, **kw):
        """
        Create a user
        POST /dataservice/admin/user

        :param payload: User
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/admin/user", payload=payload, **kw
        )

    def put(self, user_name: str, payload: Any, **kw):
        """
        Update user
        PUT /dataservice/admin/user/{userName}

        :param user_name: User name
        :param payload: User
        :returns: None
        """
        params = {
            "userName": user_name,
        }
        return self._request_adapter.request(
            "PUT", "/dataservice/admin/user/{userName}", params=params, payload=payload, **kw
        )

    def delete(self, user_name: str, **kw):
        """
        Delete user
        DELETE /dataservice/admin/user/{userName}

        :param user_name: User name
        :returns: None
        """
        params = {
            "userName": user_name,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/admin/user/{userName}", params=params, **kw
        )

    @property
    def active_sessions(self) -> ActiveSessionsBuilder:
        """
        The activeSessions property
        """
        from .active_sessions.active_sessions_builder import ActiveSessionsBuilder

        return ActiveSessionsBuilder(self._request_adapter)

    @property
    def admin(self) -> AdminBuilder:
        """
        The admin property
        """
        from .admin.admin_builder import AdminBuilder

        return AdminBuilder(self._request_adapter)

    @property
    def lock_user(self) -> LockUserBuilder:
        """
        The lockUser property
        """
        from .lock_user.lock_user_builder import LockUserBuilder

        return LockUserBuilder(self._request_adapter)

    @property
    def password(self) -> PasswordBuilder:
        """
        The password property
        """
        from .password.password_builder import PasswordBuilder

        return PasswordBuilder(self._request_adapter)

    @property
    def profile(self) -> ProfileBuilder:
        """
        The profile property
        """
        from .profile.profile_builder import ProfileBuilder

        return ProfileBuilder(self._request_adapter)

    @property
    def remove_sessions(self) -> RemoveSessionsBuilder:
        """
        The removeSessions property
        """
        from .remove_sessions.remove_sessions_builder import RemoveSessionsBuilder

        return RemoveSessionsBuilder(self._request_adapter)

    @property
    def reset(self) -> ResetBuilder:
        """
        The reset property
        """
        from .reset.reset_builder import ResetBuilder

        return ResetBuilder(self._request_adapter)

    @property
    def role(self) -> RoleBuilder:
        """
        The role property
        """
        from .role.role_builder import RoleBuilder

        return RoleBuilder(self._request_adapter)

    @property
    def user_auth_type(self) -> UserAuthTypeBuilder:
        """
        The userAuthType property
        """
        from .user_auth_type.user_auth_type_builder import UserAuthTypeBuilder

        return UserAuthTypeBuilder(self._request_adapter)

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, RootModel, constr

from .base import Pagination


class User(BaseModel):
    id: str = Field(
        ..., description='A unique identifier for the user. Cannot be edited.'
    )
    creation_date: int = Field(..., description='Unix Epoch in seconds')
    friendly_name: Optional[str] = Field(
        None,
        description='A shorter name for the user than the id. Used in some places in the UI.\n',
    )
    email: Optional[str] = Field(
        None,
        description='The email address of the user.\n',
    )


class CurrentUser(BaseModel):
    user: User


class UserCreation(BaseModel):
    id: str = Field(..., description='a unique identifier for the user.')
    invite_user: Optional[bool] = None


class UserList(BaseModel):
    pagination: Pagination
    results: List[User]


class Group(BaseModel):
    id: str
    name: Optional[str] = None
    description: Optional[str] = None
    creation_date: int = Field(..., description='Unix Epoch in seconds')


class GroupList(BaseModel):
    pagination: Pagination
    results: List[Group]


class GroupCreation(BaseModel):
    id: str
    description: Optional[str] = None


class RBAC(Enum):
    none = 'none'
    simplified = 'simplified'
    internal = 'internal'
    external = 'external'


class LoginUrlMethod(Enum):
    none = 'none'
    redirect = 'redirect'
    select = 'select'


class LoginConfig(BaseModel):
    rbac: Optional[RBAC] = Field(None, alias='RBAC')
    username_ui_placeholder: Optional[str] = None
    password_ui_placeholder: Optional[str] = None
    login_url: str = Field(..., description='Primary URL to use for login.')
    login_url_method: Optional[LoginUrlMethod] = None
    login_failed_message: Optional[str] = None
    fallback_login_url: Optional[str] = None
    fallback_login_label: Optional[str] = None
    login_cookie_names: List[str] = Field(..., description='Cookie names used to store JWT')
    logout_url: str = Field(..., description='URL to use for logging out.')


class State(Enum):
    initialized = 'initialized'
    not_initialized = 'not_initialized'


class SetupState(BaseModel):
    state: Optional[State] = None
    comm_prefs_missing: Optional[bool] = Field(
        None, description='true if the comm prefs are missing.'
    )
    login_config: Optional[LoginConfig] = None


class AccessKeyCredentials(BaseModel):
    access_key_id: constr(min_length=1) = Field(
        ...,
        description='access key ID to set for user for use in integration testing.',
        example='AKIAIOSFODNN7EXAMPLE',
    )
    secret_access_key: constr(min_length=1) = Field(
        ...,
        description='secret access key to set for user for use in integration testing.',
        example='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    )


class Setup(BaseModel):
    username: str = Field(..., description='an identifier for the user (e.g. jane.doe)')
    key: Optional[AccessKeyCredentials] = None
    firstName: Optional[str] = Field(None, description='the provided first name')
    lastName: Optional[str] = Field(None, description='the provided last name')
    email: Optional[str] = Field(None, description='the provided email')
    companyName: Optional[str] = Field(None, description='the provided company name')
    featureUpdates: Optional[bool] = Field(
        None, description='user preference to receive feature updates'
    )
    securityUpdates: Optional[bool] = Field(
        None, description='user preference to receive security updates'
    )


class CommPrefsInput(BaseModel):
    firstName: Optional[str] = Field(None, description='the provided first name')
    lastName: Optional[str] = Field(None, description='the provided last name')
    email: Optional[str] = Field(None, description='the provided email')
    companyName: Optional[str] = Field(None, description='the provided company name')
    featureUpdates: bool = Field(..., description='user preference to receive feature updates')
    securityUpdates: bool = Field(..., description='user preference to receive security updates')


class Credentials(BaseModel):
    access_key_id: str
    creation_date: int = Field(..., description='Unix Epoch in seconds')


class CredentialsList(BaseModel):
    pagination: Pagination
    results: List[Credentials]


class CredentialsWithSecret(BaseModel):
    access_key_id: str
    secret_access_key: str
    creation_date: int = Field(..., description='Unix Epoch in seconds')


class LoginInformation(BaseModel):
    access_key_id: str
    secret_access_key: str


class ExternalLoginInformation(BaseModel):
    token_expiration_duration: Optional[int] = None
    identityRequest: Dict[str, Any]


class StsAuthRequest(BaseModel):
    code: str
    state: str
    redirect_uri: str
    ttl_seconds: Optional[int] = Field(
        None,
        description='The time-to-live for the generated token in seconds. Default is 3600 seconds (1 hour).\n',
    )


class AuthenticationToken(BaseModel):
    token: str = Field(
        ..., description='a JWT token that could be used to authenticate requests'
    )
    token_expiration: Optional[int] = Field(None, description='Unix Epoch in seconds')


class AuthCapabilities(BaseModel):
    invite_user: Optional[bool] = None
    forgot_password: Optional[bool] = None


class PolicyCondition(RootModel[Optional[Dict[str, List[str]]]]):
    pass


class Effect(Enum):
    allow = 'allow'
    deny = 'deny'


class Statement(BaseModel):
    effect: Effect
    resource: str
    action: List[str] = Field(..., min_length=1)
    condition: Optional[Dict[str, PolicyCondition]] = Field(
        None, description='Optional conditions for when this statement applies.'
    )


class Policy(BaseModel):
    id: str
    creation_date: Optional[int] = Field(None, description='Unix Epoch in seconds')
    statement: List[Statement] = Field(..., min_length=1)


class PolicyList(BaseModel):
    pagination: Pagination
    results: List[Policy]


class ACL(BaseModel):
    permission: str = Field(
        ...,
        description='Permission level to give this ACL. "Read", "Write", "Super" and "Admin" are all supported.\n',
    )


class ExternalPrincipalSettings(RootModel[Optional[Dict[str, str]]]):
    pass


class Settings(BaseModel):
    pass


class ExternalPrincipalCreation(BaseModel):
    settings: Optional[Union[List[ExternalPrincipalSettings], Settings]] = None


class Settings1(BaseModel):
    pass


class ExternalPrincipal(BaseModel):
    id: str = Field(
        ...,
        description='A unique identifier for the external principal i.e aws:sts::123:assumed-role/role-name',
    )
    user_id: str = Field(
        ..., description='lakeFS user ID to associate with an external principal.\n'
    )
    settings: Optional[Union[List[ExternalPrincipalSettings], Settings1]] = None


class ExternalPrincipalList(BaseModel):
    pagination: Pagination
    results: List[ExternalPrincipal]

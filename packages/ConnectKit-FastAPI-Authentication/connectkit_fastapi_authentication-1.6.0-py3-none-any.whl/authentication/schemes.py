import re
from datetime import datetime
from typing import Optional, List, Annotated, Dict, Any

from pydantic import BaseModel as PydanticBaseModel, ConfigDict, AfterValidator

from authentication.settings import settings


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True,
                              str_strip_whitespace=True)


_login_rule = re.compile("^[a-z][-_a-z0-9]{2,31}$")
_password_rule_space = re.compile(r"\s")
_password_rule_digit = re.compile("[0-9]")
_password_rule_lower = re.compile("[a-z]")
_password_rule_upper = re.compile("[A-Z]")
_password_rule_special = re.compile(r"[-~!@#$%№^&*(){}\[\]|/\\<>?_+=]")


def login_rules(login: str):
    match = _login_rule.fullmatch(login)
    if match is None:
        raise ValueError(f"Invalid login format")
    return login


def password_rules(password: str):
    if len(password) < 8:
        raise ValueError(f"Password must be at least 8 characters long")
    if _password_rule_space.search(password) is not None:
        raise ValueError("Password must not contain spaces")
    if _password_rule_lower.search(password) is None:
        raise ValueError(f"Password must contain at least one lowercase letter")
    if _password_rule_upper.search(password) is None:
        raise ValueError(f"Password must contain at least one uppercase letter")
    if _password_rule_special.search(password) is None:
        raise ValueError(f"Password must contain at least one special character")
    if _password_rule_digit.search(password) is None:
        raise ValueError(f"Password must contain at least one digit character")
    return password


login_type = Annotated[str, AfterValidator(login_rules)]
password_type = Annotated[str, AfterValidator(password_rules)]


class CSRFRequest(BaseModel):
    login: login_type


class CSRFPayload(BaseModel):
    required_login: str
    uuid: str
    used: bool = False
    failed_count: int = 0
    until_date: datetime


class CSRFReturn(BaseModel):
    csrf: str


class AccountCredentials(BaseModel):
    login: login_type
    password: password_type
    csrf: str
    remember_me: Optional[bool] = False


class Refresh(BaseModel):
    refresh: str
    wait_otp: bool


class GetSession(BaseModel):
    id: int
    fingerprint: str
    invalid_after: datetime


class GetSessions(BaseModel):
    current: GetSession
    other: List[GetSession]


class NewAccount(BaseModel):
    login: login_type
    password: password_type
    properties: Optional[Dict[str, Any]] = None
    active: Optional[bool] = False


class UserInfo(BaseModel):
    login: str
    active: bool
    properties: Dict[str, Any]


class NewPassword(BaseModel):
    old_password: password_type
    new_password: password_type


class PasswordVerify(BaseModel):
    password: password_type


if settings.SECURE_OTP_ENABLED:
    class SetupOTP(BaseModel):
        secret: str
        install_link: str


    class OTPCodes(BaseModel):
        codes: List[str]


    class OTPCode(BaseModel):
        code: str

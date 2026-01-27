from typing import Optional, Dict, Any, Tuple, List, Literal
from datetime import datetime
from pydantic import BaseModel, Field


class ServiceInfo(BaseModel):
    name: str
    version: Optional[str] = None
    environment: str


class HostInfo(BaseModel):
    hostname: Optional[str] = None
    ip: Optional[str] = None


class LogMeta(BaseModel):
    logger: Optional[str] = None
    thread: Optional[str] = None


class TraceInfo(BaseModel):
    trace_id: str = Field(..., description="Distributed trace ID")
    span_id: Optional[str] = None
    parent_span_id: Optional[str] = None


class HttpInfo(BaseModel):
    method: Optional[str] = None
    path: Optional[str] = Field(description="The path of the request, excluding query parameters. This field may occasionally contain an NER labelled entity.")
    status_code: Optional[int] = None
    client_ip: Optional[str] = None
    user_agent: Optional[str] = None
    latency_ms: Optional[int] = None


class UserInfo(BaseModel):
    id: Optional[str] = None
    role: Optional[str] = None


class ErrorInfo(BaseModel):
    type: Optional[str] = None
    message: Optional[str] = None
    stacktrace: Optional[str] = None


class EventInfo(BaseModel):
    type: Optional[str] = None
    outcome: Optional[str] = None
    entity: Optional[str] = None
    entity_id: Optional[str] = None


class SecurityInfo(BaseModel):
    auth_method: Optional[str] = None
    mfa: Optional[bool] = None


class LogRecord(BaseModel):
    timestamp: datetime
    level: str

    service: ServiceInfo
    host: Optional[HostInfo] = None
    log: Optional[LogMeta] = None

    trace: Optional[TraceInfo] = None
    correlation_id: Optional[str] = None

    http: Optional[HttpInfo] = None
    user: Optional[UserInfo] = None

    event: Optional[EventInfo] = None
    security: Optional[SecurityInfo] = None

    data_classification: Optional[str] = None

    message: str = Field(description="The log message. If there is a label it may be contained here.")

    # Escape hatch for forward compatibility
    extra: Optional[Dict[str, Any]] = None

    class Config:
        extra = "allow"



Label = Literal[
    "PASSWORD",
    "PERSON",
    "NAME",
    "LOCATION",
    "DATE_OF_BIRTH",
    "NINO",
    "NHS_NUMBER",
    "NATIONAL_INSURANCE_NUMBER",
    "PHONE_NUMBER",
    "BANK_SORT_CODE",
    "BANK_ACCOUNT_NUMBER",
    "CREDIT_CARD_NUMBER",
    "ADDRESS",
    "POSTCODE",
    "VEHICLE_REGISTRATION",
    "EMAIL_ADDRESS",
]
Text = str


class Entity(BaseModel):
    """
    Represents an NER entity extracted from a log line, with a label and associated text.
    """
    label: Label
    text: Text = Field(description="The text of the entity. This is normally only a small number of tokens"
    )

class LogLine(BaseModel):
    """
    Represents all the NER entities in a log line.
    """
    entities: List[Entity] = Field(description="A list of NER labelled entities within this log line. 1/3 log lines should have entities")

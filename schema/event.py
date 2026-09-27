from typing import Optional
from pydantic import BaseModel, Field


class Source(BaseModel):
    type: str
    host: Optional[str] = None
    ip: Optional[str] = None


class Event(BaseModel):
    id: Optional[int] = None
    type: str
    action: Optional[str] = None
    status: Optional[str] = None
    category: Optional[str] = None


class User(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None


class Network(BaseModel):
    src_ip: Optional[str] = None
    src_port: Optional[int] = None
    dst_ip: Optional[str] = None
    dst_port: Optional[int] = None
    protocol: Optional[str] = None


class Process(BaseModel):
    name: Optional[str] = None
    pid: Optional[int] = None
    command_line: Optional[str] = None


class NormalizedLog(BaseModel):
    timestamp: str

    source: Source

    event: Event

    user: User = Field(
        default_factory=User
    )

    network: Network = Field(
        default_factory=Network
    )

    process: Process = Field(
        default_factory=Process
    )

    message: Optional[str] = None

    raw_log: Optional[str] = None
from typing import Any, Literal

from pydantic import BaseModel, Field, HttpUrl


class StoreAuditRequest(BaseModel):
    url: HttpUrl
    business_type: str | None = None

class Opportunity(BaseModel):
    title: str
    problem: str
    solution: str
    evidence: list[str] = Field(default_factory=list)
    score: float = Field(ge=0, le=1)
    reversible: bool = True
    requires_approval: bool = False

class Offer(BaseModel):
    subject: str
    message: str
    service: str
    next_step: str
    evidence: list[str] = Field(default_factory=list)

class Mission(BaseModel):
    objective: str
    status: Literal["planned","running","completed","blocked"] = "planned"
    actions: list[str] = Field(default_factory=list)
    opportunities: list[Opportunity] = Field(default_factory=list)
    offers: list[Offer] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

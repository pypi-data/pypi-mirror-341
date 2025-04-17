# this file is @generated
import typing as t
from datetime import datetime

from .common import BaseModel
from .connector_kind import ConnectorKind


class TemplateOut(BaseModel):
    created_at: datetime

    description: str

    feature_flag: t.Optional[str] = None

    filter_types: t.Optional[t.List[str]] = None

    id: str
    """The TransformationTemplate's ID."""

    instructions: str

    instructions_link: t.Optional[str] = None

    kind: ConnectorKind

    logo: str

    name: str

    org_id: str
    """The Organization's ID."""

    transformation: str

    updated_at: datetime

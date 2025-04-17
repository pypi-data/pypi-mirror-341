from pydantic import BaseModel
from uuid import UUID

class JobInboxGetPayload(BaseModel):
    accountId: UUID

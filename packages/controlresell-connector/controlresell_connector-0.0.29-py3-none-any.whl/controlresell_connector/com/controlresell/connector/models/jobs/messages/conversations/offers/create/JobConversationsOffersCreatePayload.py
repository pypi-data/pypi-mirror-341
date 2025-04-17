from pydantic import BaseModel
from uuid import UUID

class JobConversationsOffersCreatePayload(BaseModel):
    accountId: UUID
    transactionId: str
    conversationId: str
    price: float
    currency: str

from pydantic import BaseModel
from controlresell_connector.com.controlresell.connector.models.jobs.messages.conversations.offers.JobConversationOffer import JobConversationOffer

class JobConversationsOffersCreateResponse(BaseModel):
    offer: JobConversationOffer

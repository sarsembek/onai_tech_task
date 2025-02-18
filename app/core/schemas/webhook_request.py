from pydantic import BaseModel, HttpUrl

class WebhookRequestSchema(BaseModel):
    message: str
    callback_url: HttpUrl

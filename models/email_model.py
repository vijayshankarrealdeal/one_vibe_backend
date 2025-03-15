from pydantic import BaseModel, EmailStr


class EmailSchema(BaseModel):
    email: EmailStr

class OTPVerifySchema(BaseModel):
    username: str
    email: EmailStr
    otp: str
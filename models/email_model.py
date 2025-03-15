from pydantic import BaseModel, EmailStr


class EmailSchema(BaseModel):
    email: EmailStr

class OTPVerifySchema(BaseModel):
    email: EmailStr
    otp: str
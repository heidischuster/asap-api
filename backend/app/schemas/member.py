from typing import Optional
from datetime import datetime
from random import random
import re
import uuid

from pydantic import BaseModel, Field, ValidationError, validator
from cryptography.fernet import Fernet


# Instance the Fernet class with the key
fernet = Fernet(b'nNjpIl9Ax2LRtm-p6ryCRZ8lRsL0DtuY0f9JeAe2wG0=')
separator = "|"
validate = "asap"
regularExpression = re.compile('\w{8}-\w{4}-\w{4}-\w{4}-\w{12}')

# Shared properties
class Member(BaseModel):
    first_name: str
    last_name: str
    dob: str
    country: str = Field(max_length=2, description="2 digit country code")
    member_id: Optional[str] = None

    @validator('dob')
    def dob_must_be_date(cls, v):
        if v != datetime.strptime(v, "%m/%d/%Y").strftime('%m/%d/%Y'):
            raise ValueError('Date of Birth must be in MM/DD/YYYY')
        return v.title()

    def generate_id(self):
        message = self.first_name.lower() + separator + self.last_name.lower() + separator + self.dob + separator \
                  + self.country.upper() + separator + str(random())
        self.member_id = str(uuid.uuid5(uuid.NAMESPACE_URL, message))
        return self

    def validate_id(self, member_id):
        return regularExpression.match(member_id)

    def generate_id_decryptable(self):
        message = self.first_name.lower() + separator + self.last_name.lower() + separator + self.dob + separator \
                  + self.country.upper() + separator + validate
        self.member_id = fernet.encrypt(message.encode())
        return self

    def decode_id(self, member_id):
        try:
            id = fernet.decrypt(member_id).decode()
        except:
            raise ValueError("The string can not be decoded")
        fields = id.split(separator)
        if len(fields) < 5:
            raise ValueError("The decoded string does not have enough fields")
        if fields[4] != validate:
            raise ValueError("The decoded member id is missing the validation string: " + id)
        if len(fields[3]) > 2:
            raise ValueError("Country is too long: " + fields[3] + "  " + id)
        try:
            if fields[2] != datetime.strptime(fields[2], "%m/%d/%Y").strftime('%m/%d/%Y'):
                raise ValueError
        except ValueError:
            raise ValueError("Date of Birth is in the wrong format:  " + fields[2] + "  " + id)

        self.first_name = fields[0]
        self.last_name = fields[1]
        self.dob = fields[2]
        self.country = fields[3]
        self.member_id = id
        return self



from typing import Optional
from datetime import datetime
from random import random
import re
import uuid
from pydantic import BaseModel, Field, ValidationError, validator
from cryptography.fernet import Fernet


# Instance the Fernet class with the key
# There is a second implementation that encrypts the member attributes in a way they can be decrypted back
# It would guarantee that the String comes from this system and the same user would get the same ID but
# they are very long and ugly strings
fernet = Fernet(b'nNjpIl9Ax2LRtm-p6ryCRZ8lRsL0DtuY0f9JeAe2wG0=')
separator = "|"
validate = "asap"

# This is the fregular expression for the format validation
regularExpression = re.compile('\w{8}-\w{4}-\w{4}-\w{4}-\w{12}')

# Our member class with pydantic validators. All attributes are required and the country code can't be
# longer than 2 characters. Also enforcing the date format as MM/DD/YYYY
class Member(BaseModel):
    first_name: str
    last_name: str
    dob: str
    country: str = Field(max_length=2, description="2 digit country code")
    member_id: Optional[str] = None

    # custom validator for date format
    @validator('dob')
    def dob_must_be_date(cls, v):
        if v != datetime.strptime(v, "%m/%d/%Y").strftime('%m/%d/%Y'):
            raise ValueError('Date of Birth must be in MM/DD/YYYY')
        return v.title()

    # The generated ID is a hash key from the attributes with a random number added
    def generate_id(self):
        message = self.first_name.lower() + separator + self.last_name.lower() + separator + self.dob + separator \
                  + self.country.upper() + separator + str(random())
        self.member_id = str(uuid.uuid5(uuid.NAMESPACE_URL, message))
        return self

    # can only to format validation since you can't dehash
    def validate_id(self, member_id):
        return regularExpression.match(member_id)







    # this generates an ID that can be decoded back to attributes
    def generate_id_decryptable(self):
        message = self.first_name.lower() + separator + self.last_name.lower() + separator + self.dob + separator \
                  + self.country.upper() + separator + validate
        self.member_id = fernet.encrypt(message.encode())
        return self



    # decoding the id back to values
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



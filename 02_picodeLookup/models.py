from pydantic import BaseModel, field_validator, Field, StringConstraints
from typing import Annotated

class PincodeRequest(BaseModel):
    pincode: str

    #pincode must be exactly 6 digits
    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls, value):
        if len(value) != 6 or not value.isdigit():
            raise ValueError("Pincode must be exactly 6 digit")
        return value

class LocationResponse(BaseModel):
    pincode: str
    city: str
    state: str
    district: str

## `@field_validator` : If you prefer writing custom validation logic or want a specific error message if any individual pincode fails,
# class BulkRequest(BaseModel):
#     pincodes: list[str]

#     @field_validator("pincodes")
#     @classmethod
#     def validate_pincodes(cls, values):
#         if len(values) == 0:
#             raise ValueError("At least one pincode is required")
#         if len(values) > 20:
#             raise ValueError("Maximu 20 pincodes allowed per request")

#         for code in values:
#             if len(code) != 6 or not code.isdigit():
#                 raise ValueError("Each pincode must be exactly 6 digit or may be you have passed alphabetic picodes")
#         return values
                
class BulkRequest(BaseModel):
    # Each string in the list must be exactly 6 digits (using regex pattern)
    pincodes: list[
        Annotated [str, StringConstraints(pattern=r"^\d{6}$")]
        ] = Field(...,min_length=1,max_length=20)

class BulkResponse(BaseModel):
    status: str = "success"
    found: int
    not_found: int
    results: list[LocationResponse]
    missing: list[str]
    
from pydantic import BaseModel, Field

class ApplicationSchema(BaseModel):
    application_id: int     =   Field(default=None)
    name:           str     =   Field(...)
    status:         str     =   Field(...)
    claim:          int     =   Field(...)
    description:    str     =   Field(...)

    class Config:
        schema_extra = {
            "example": {
                'name': 'testname',
                'status': 'на диагностике',
                'claim': 0,
                'description': 'testdescription'
            }
        }

    def to_dict(self) -> dict:
        return {
            'name':         self.name,
            'status':       self.status,
            'claim':        self.claim,
            'description':  self.description
        }

class UserApplicationRelaionSchema(BaseModel):
    application_id: int = Field(...)
    user_id: int = Field(...)
    user_role: str = Field(...)

    def to_dict(self) -> dict:
        return {
            'case_id': self.application_id,
            'user_id': self.user_id,
            'user_role': self.user_role
        }

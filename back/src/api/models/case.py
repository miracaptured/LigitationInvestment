from pydantic import BaseModel, Field

class CaseSchema(BaseModel):
    case_id:        int     =   Field(default=None)
    initiator_id:   int     =   Field(...)
    name:           str     =   Field(...)
    status:         str     =   Field(...)
    claim:          int     =   Field(...)
    initiator_role: str     =   Field(...)
    description:    str     =   Field(...)

    class Config:
        schema_extra = {
            "example": {
                'name': 'testname',
                'initiator_id': 1,
                'status': 'на диагностике',
                'claim': 0,
                'initiator_role': 'истец',
                'description': 'testdescription'
            }
        }

    def to_dict(self) -> dict:
        return {
            'name':         self.name,
            'initiator_id': self.initiator_id,
            'status':       self.status,
            'claim':        self.claim,
            'initiator_role': self.initiator_role.lower(),
            'description':  self.description
        }

class UserCaseRelaionSchema(BaseModel):
    case_id: int = Field(...)
    user_id: int = Field(...)
    user_role: str = Field(...)

    def to_dict(self) -> dict:
        return {
            'case_id': self.case_id,
            'user_id': self.user_id,
            'user_role': self.user_role
        }

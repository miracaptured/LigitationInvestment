from pydantic import BaseModel, Field

class CaseSchema(BaseModel):
    case_id:        int     =   Field(default=None)
    name:           str     =   Field(...)
    status:         int     =   Field(...)
    claim:          int     =   Field(...)
    description:    str     =   Field(...)

    class Config:
        schema_extra = {
            "example": {
                'name': 'testname',
                'status': 1,
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
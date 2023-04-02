from pydantic import BaseModel, Field, AnyHttpUrl

class DocumentSchema(BaseModel):
    doc_id:     int     =   Field(default=None)
    case_id:    int     =   Field(...)
    name:       str     =   Field(...)
    link:       str     =   Field(...)

    class Config:
        schema_extra = {
            "example": {
                'case_id': 1,
                'name': 'testdoc',
                'link': 'testlink'
            }
        }

    def to_dict(self) -> dict:
        return {
            'case_id':  self.case_id,
            'name':     self.name,
            'link':     self.link
        }
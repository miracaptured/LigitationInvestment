from dataaccess.crud import db_funcs
from dataaccess.models.user import User
from dataaccess.models.case import Case
from dataaccess.models.document import Document

db_funcs.add_case(Case(1, 'testcase', 1, 1, ''))
db_funcs.add_document(Document(1, 1, 'testdoc', 'testlink'))

docs = db_funcs.get_documents_by_case_id(1)
print(docs)


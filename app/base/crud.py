from app.database.session import Session

from app.models.capec import ExecuteFlow, Capec
from app.models.definition import Definition

ExecutionModels = ExecuteFlow

class CRUDCAPEC():
    @classmethod
    async def get_multi(self, db: Session):
        query = db.query(ExecutionModels).filter(ExecutionModels.deleted_date == None)
        return query.all()

    @classmethod
    def get_by_id(self, db: Session, filters):
        query = db.query(ExecutionModels).filter(*filters)
        return query.first()
    

    @classmethod
    async def get_capec_by_id(self, db: Session, filters):
        query = db.query(Capec).filter(*filters).first()
        if query:
            return query
        else:
            return False

class CRUDDefinition():
    @classmethod
    async def get_data(self, db: Session, filters):
        query = db.query(Definition).filter(*filters)
        return query.all()
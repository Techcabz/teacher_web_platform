from app.extensions import db

class CRUDService:
    def __init__(self, model):
        self.model = model

    def create(self, **kwargs):
        """
        Create a new record in the database.
        """
        instance = self.model(**kwargs)
        try:
            db.session.add(instance)
            db.session.commit()
            return instance
        except Exception as e:
            db.session.rollback()
            print(f"Error creating record: {e}")
            return None

    def get(self, **filters):
        """
        Get records from the database by filters.
        """
        query = self.model.query
        for field, value in filters.items():
            query = query.filter(getattr(self.model, field) == value)
        return query.all()

    def get_one(self, **filters):
        """
        Get a single record based on filters.
        """
        query = self.model.query
        for field, value in filters.items():
            query = query.filter(getattr(self.model, field) == value)
        return query.first()

    def update(self, record_id, **kwargs):
        """
        Update an existing record.
        """
        instance = self.model.query.get(record_id)
        if instance:
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            try:
                db.session.commit()
                return instance
            except Exception as e:
                db.session.rollback()
                print(f"Error updating record: {e}")
        return None

    def delete(self, record_id):
        """
        Delete a record by ID.
        """
        instance = self.model.query.get(record_id)
        if instance:
            try:
                db.session.delete(instance)
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                print(f"Error deleting record: {e}")
        return False

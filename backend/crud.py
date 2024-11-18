from sqlalchemy.orm import Session
from . import models, schemas
import os
from sqlalchemy.orm import Session
from .models import File


def create_file(db: Session, filename: str, description: str):
    db_file = models.File(filename=filename, description=description)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def get_all_files(db: Session):
    return db.query(models.File).all()

def get_file_paths(db: Session, ids: list[int] = None):
    query = db.query(models.File)
    if ids:
        query = query.filter(models.File.id.in_(ids))
    return [file.filename for file in query.all()]



def delete_file(db: Session, file_id: int, media_directory: str):
    # Fetch the file record
    file_record = db.query(File).filter(File.id == file_id).first()
    print(file_record)
    if file_record:
        # Remove the file from the directory
        file_path = os.path.join(media_directory, file_record.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Delete the file record from the database
        db.delete(file_record)
        db.commit()
        return True
    return False


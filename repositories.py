from sqlalchemy.orm import Session
from datetime import datetime

import models,schemas


def get_temptests(db: Session, skip:int=0, limit: int=100):
    return db.query(models.Temptest).offset(skip).limit(limit).all()


def get_temptest(db: Session, temptest_id: int):
    return db.query(models.Temptest).filter(models.Temptest.id == temptest_id).first()


def delete_temptest(db: Session, todo_id: int):
    return db.query(models.Temptest).filter(models.Temptest.id == temptest_id).delete()


def update_temptest(db: Session, update_temptest: models.Temptest, temptest_id: int):
    temptest = get_temptest(db, temptest_id)
    if temptest is not None:
        temptest.tempreg = update_temptest.tempreg if update_temptest.tempreg != None else temptest.tempreg
        temptest.status = update_temptest.status if update_temptest.status != None else temptest.status
        temptest.updated_at = datetime.now()
        db.commit()
        db.refresh(temptest)
        return temptest
    else:
        return None

def create_temptest(db: Session, temptest:schemas.Temptest):
    db_temptest = models.Temptest(tempreg=temptest.tempreg,
                          status=temptest.status,
                          created_at=datetime.now(),
                          updated_at=datetime.now())
    db.add(db_temptest)
    db.commit()
    db.refresh(db_temptest)
    return db_temptest


# NOTE :
# - To perform CRUD need to add object instance to the database session.
# - do commit changes
# - do refresh your instance to contain new data from the database.

from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from database import Base, SessionLocal
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session

import models,schemas, repositories
import logging

#create FastAPI application instance
app = FastAPI()


def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()


# Create routers for different route groups
temptest_router_v1 = APIRouter(prefix="/temptest", tags=["temptest v1"])

'''
 -  Here we injected schemas / serializer from TodoRead to response since this can
    show more than one todo result we put use list
 -  We create a simple repository to perform database process here
 -  Last we put proper http status using status_code decorator.
    Common status codes in the status module:
    status.HTTP_200_OK (default for successful responses)
    status.HTTP_201_CREATED
    status.HTTP_204_NO_CONTENT
    status.HTTP_400_BAD_REQUEST
    status.HTTP_404_NOT_FOUND
    status.HTTP_500_INTERNAL_SERVER_ERROR
'''


@temptest_router_v1.get("", summary="List all temperature registers", status_code=status.HTTP_200_OK, response_model=list[schemas.TemptestRead])
async def get_temptest_v1(db:Session=Depends(get_db)):
    return repositories.get_temptests(db)


'''
 -  We use response from TodoRead schema so it'll show all 4 properties of the record.
 -  Incoming request uses Todo schema. According to the schema two parameters are mandatory
    it'll act as a validation as well
'''
@temptest_router_v1.post("", summary="Create a new temperature register", status_code=status.HTTP_201_CREATED, response_model=schemas.TemptestRead)
async def post_temptest_v1(temptest:schemas.Temptest, db:Session=Depends(get_db)):
    return repositories.create_temptest(db, temptest)


'''
 -  To get todo detail we only need one parameter to fetch a todo based on its id
 -  Throw http exception if record is not found
'''
@temptest_router_v1.get("/{temptest_id}", summary="Get temp register detail", status_code=status.HTTP_200_OK, response_model=schemas.TemptestRead)
async def patch_temptest_v1(temptest_id: str, db:Session=Depends(get_db)):
    temptest = repositories.get_temptest(db, temptest_id)
    if temptest is not None:
        return temptest
    else:
        raise HTTPException(status_code=400, detail="ERROR: register not found")


'''
 -  Patch is only partial update therefore we use TodoPatch schemas which we put optional parameter
    for title & status. If any of these parameters are added then the value of these parameters will
    be updated
 '''
@temptest_router_v1.patch("/{temptest_id}", summary="Partial update of register", status_code=status.HTTP_200_OK, response_model=schemas.TemptestRead)
async def patch_temptest_v1(temptest_id: str, update_temptest:schemas.TemptestPatch, db:Session=Depends(get_db)):
    temptest = repositories.get_temptest(db, temptest_id)
    if temptest is not None:
        repositories.update_temptest(db, update_temptest, temptest_id)
        db.commit()
        db.refresh(temptest)

        return temptest
    else:
        raise HTTPException(status_code=400, detail="ERROR: register not found")


'''
 -  Put request means all update according to the REST best practice. On this case
    the required parameters are identical with post so we use the same schema for
    incoming request with post which is Todo
'''
@temptest_router_v1.put("/{temptest_id}", summary="Update register",status_code=status.HTTP_200_OK, response_model=schemas.TemptestRead)
async def put_temptest_v1(temptest_id: str, update_temptest:schemas.Temptest, db:Session=Depends(get_db)):
    temptest = repositories.get_temptest(db, temptest_id)
    if temptest is not None:
        repositories.update_temptest(db, update_temptest, temptest_id)
        db.commit()
        db.refresh(temptest)

        return temptest
    else:
        raise HTTPException(status_code=400, detail="ERROR: register not found")


@temptest_router_v1.delete("/{temptest_id}",status_code=status.HTTP_204_NO_CONTENT, summary="Delete register")
async def delete_temptest_v1(temptest_id: str, db:Session=Depends(get_db)):
    temptest = repositories.get_temptest(db, temptest_id)
    if temptest is not None:
        db.delete(temptest)
        db.commit()
        return
    else:
        raise HTTPException(status_code=400, detail="ERROR: register not found")


# Create versioning for API endpoint by incorporating todo_router_v1 into FastAPI application instance
app.include_router(temptest_router_v1, prefix="/v1")

from sqlalchemy import select, update
from sqlalchemy.orm import Session
from ..database import dbschema
from ..database.db import Base, engine, get_db
import asyncio






async def expireHeartBeat(db: Annotated[Session, Depends(get_db)]):
    while True:
        db.execute(
            update(computerInfo)
            .where(datetime.now() - computerInfo.last_heartbeat >= 150)
            .values(is_alive=False)
        )
        await asyncio.sleep(50)



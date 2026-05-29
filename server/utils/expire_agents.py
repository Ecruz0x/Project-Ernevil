from sqlalchemy import select, update
from sqlalchemy.orm import Session
from ..database import dbschema
from ..database.db import Base, engine, get_db
import asyncio






async def expireHeartBeat(db: Annotated[Session, Depends(get_db)]):
    while True:
        for k in computers:
            duration = datetime.now() - k["lastHB"]
            if duration.total_seconds() >= 150:
                k["is_alive"] = False
        await asyncio.sleep(50)
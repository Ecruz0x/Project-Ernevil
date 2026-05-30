from sqlalchemy import select, update
from sqlalchemy.orm import Session
from ..database import dbschema
from ..database.db import Base, engine, get_db, sessionlocal
import asyncio
from typing import Annotated
from fastapi import Depends
from datetime import datetime, timedelta





async def expireHeartBeat():
    while True:
        with sessionlocal() as db:
            threshold = datetime.now() - timedelta(seconds=150)

            stmt = (
                update(dbschema.ComputerInfo)
                .where(dbschema.ComputerInfo.last_heartbeat <= threshold)
                .values(is_alive=False)
            )

            db.execute(stmt)
            db.commit()

        await asyncio.sleep(10)



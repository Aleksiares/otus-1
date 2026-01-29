from sqlalchemy.ext.asyncio import AsyncEngine


class Query:
    def __init__(self, engine: AsyncEngine):
        self._engine = engine

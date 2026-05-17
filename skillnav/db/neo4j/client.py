from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from neo4j import AsyncDriver, AsyncGraphDatabase, AsyncSession


class Neo4jClient:
    """Client asynchrone Neo4j AuraDB. Utiliser comme context manager ou appeler close() manuellement."""

    def __init__(self, uri: str, user: str, password: str) -> None:
        self._driver: AsyncDriver = AsyncGraphDatabase.driver(
            uri,
            auth=(user, password),
        )

    async def verify_connectivity(self) -> None:
        """Vérifie que la connexion au cluster AuraDB est opérationnelle."""
        await self._driver.verify_connectivity()

    async def close(self) -> None:
        await self._driver.close()

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._driver.session() as s:
            yield s

    async def run(self, query: str, **params: Any) -> list[dict[str, Any]]:
        """Exécute une requête Cypher et retourne les résultats sous forme de liste de dicts."""
        async with self.session() as s:
            result = await s.run(query, **params)
            return [record.data() async for record in result]

    async def run_write(self, query: str, **params: Any) -> None:
        """Exécute une requête Cypher en écriture (CREATE / MERGE / DELETE)."""
        async with self.session() as s:
            await s.run(query, **params)

    async def __aenter__(self) -> "Neo4jClient":
        await self.verify_connectivity()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        await self.close()


def make_neo4j_client() -> Neo4jClient:
    """Factory — crée un Neo4jClient depuis les variables d'environnement (.env)."""
    from skillnav.config import settings

    return Neo4jClient(
        uri=settings.neo4j_uri,
        user=settings.neo4j_user,
        password=settings.neo4j_password,
    )

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Neo4j AuraDB
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = ""

    # MongoDB Atlas
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "skillnav"

    # Elasticsearch Cloud
    elastic_cloud_id: str = ""
    elastic_api_key: str = ""

    # AI / Scraping
    anthropic_api_key: str = ""
    apify_token: str = ""
    firecrawl_api_key: str = ""

    # Scraper behaviour
    scraper_user_agent: str = "SkillnavBot/1.0 (Academic; M242 ENSA-Tetouan)"
    scraper_rate_limit_seconds: float = 5.0


settings = Settings()

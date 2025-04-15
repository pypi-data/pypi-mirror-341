from .settings import settings

def configure(domain: str):
    domain = domain.rstrip("/")
    settings.DOMAIN = domain
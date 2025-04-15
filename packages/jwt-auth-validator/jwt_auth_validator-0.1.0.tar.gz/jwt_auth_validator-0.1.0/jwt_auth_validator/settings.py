class Settings:
    DOMAIN = None
    JWKS_PATH = "/.well-known/jwks.json"

    @property
    def JWKS_URL(self):
        if not self.DOMAIN:
            raise ValueError("DOMAIN is not set. Use `configure(domain)` to set it.")
        return f"{self.DOMAIN}{self.JWKS_PATH}"

settings = Settings()
from cubicweb.entities import AnyEntity, fetch_config, adapters
from cubicweb.predicates import is_instance


class AuthToken(AnyEntity):
    __regid__ = "AuthToken"
    fetch_attrs, cw_fetch_order = fetch_config(["id", "enabled", "expiration_date"])


class AuthTokenDublinCoreAdapter(adapters.IDublinCoreAdapter):
    __select__ = is_instance("AuthToken")

    def title(self):
        return self.id

    def description(self, format="text/plain"):
        return (
            f"{self.id} ({self.enabled and 'enabled' or 'disabled'}) "
            f"expires on {self.expiration_date}"
        )

from nexadataset.services.auth import login_sync


def login(key: str, secret: str) -> None:
    login_sync(key, secret)

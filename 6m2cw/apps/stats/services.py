from django.core.cache import cache


def get_stats():
    stats = cache.get("site_stats")

    if stats is None:
        stats = {
            "users_count": 1000,
            "active_orders": 42,
        }
        cache.set("site_stats", stats, timeout=60)

    return stats
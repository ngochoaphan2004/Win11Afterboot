import sys
sys.path.insert(0, ".")
from app.core.app_registry import APPS
zalo = next(a for a in APPS if a["id"] == "zalo")
print("Zalo OK:", zalo["name"])
print("URL:", zalo["url"])
print("Checked default:", zalo["checked_default"])
print("Total apps:", len(APPS))
for a in APPS:
    print(f"  - {a['name']} ({a['category']})")

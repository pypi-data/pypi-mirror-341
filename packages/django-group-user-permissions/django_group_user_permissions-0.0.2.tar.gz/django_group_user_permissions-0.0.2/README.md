# DJANGO GROUP_USER_PERMISSIONS

## 🔍 Overview

This package was developed because Django REST Framework (DRF) does not provide a built-in solution to check **both user-level and group-level permissions** in one place.

`django-group-user-permissions` is a custom DRF permission class that combines permissions assigned directly to a user and those inherited from the user’s groups. It simplifies permission handling in DRF-based APIs by dynamically checking permissions based on the request method and the model associated with the view.

---

## 📦 Installation

```bash
pip install django-group-user-permissions
```

⚙️ Configuration
1. Add to INSTALLED_APPS in settings.py:
```base

INSTALLED_APPS = [
    
    "django-group-user-permissions",
]

```

2. Import the permission class in your views:

```base

from django_group_user_permissions.group_user_permissions import GroupUserPermissions

```

3. 🚀 Usage in Views
```base

permission_classes = [GroupUserPermissions]

```

✅ What It Does
Maps HTTP methods to Django permission codenames:

GET → view_<modelname>

POST → add_<modelname>

PUT / PATCH → change_<modelname>

DELETE → delete_<modelname>

Checks if the user has required permission either:

Directly assigned to the user

Through any group the user belongs to
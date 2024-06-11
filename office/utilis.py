
from django.contrib.auth.models import Permission
from .models import Company, CompanyRole


def create_company_role_and_permissions(company):
    # Define roles and permissions
    default_roles = {
        "admin":[
        "view_employee", "add_employee", "change_employee", "delete_employee",
        "view_officeunit", "add_officeunit", "change_officeunit", "delete_officeunit",
        "view_office", "add_office", "change_office", "delete_office",
        "view_companyrole", "add_companyrole", "change_companyrole", "delete_companyrole",
        ],
        "backend": [],
        "social-worker": []    
    }

    # Create admin group
    print(Permission.objects.all().values_list('codename', flat=True))
    for role, permissions in default_roles.items():
        
        company_role = CompanyRole.objects.create(name=role, company=company)

        # Assign permissions to the admin group
        for permission_name in permissions:
            permission = Permission.objects.get(codename=permission_name)
            company_role.permission.add(permission)

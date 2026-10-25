import collections

# Define available actions for different resource types
RESOURCE_ACTIONS = {
    "Virtual Machine": ["read", "write", "delete", "start", "stop"],
    "Storage Account": ["read", "write", "delete", "list_keys"],
    "SQL Database": ["read", "write", "delete", "backup"]
}

# Define roles and their associated permissions
# Each permission is a tuple: (resource_type, action)
ROLES = {
    "Reader": [
        ("Virtual Machine", "read"),
        ("Storage Account", "read"),
        ("SQL Database", "read")
    ],
    "Contributor": [
        ("Virtual Machine", "read"), ("Virtual Machine", "write"), ("Virtual Machine", "delete"), ("Virtual Machine", "start"), ("Virtual Machine", "stop"),
        ("Storage Account", "read"), ("Storage Account", "write"), ("Storage Account", "delete"), ("Storage Account", "list_keys"),
        ("SQL Database", "read"), ("SQL Database", "write"), ("SQL Database", "delete"), ("SQL Database", "backup")
    ],
    "VM Operator": [
        ("Virtual Machine", "read"),
        ("Virtual Machine", "start"),
        ("Virtual Machine", "stop")
    ],
    "Storage Blob Data Contributor": [
        ("Storage Account", "read"),
        ("Storage Account", "write")
    ]
}

# Define users and their assigned roles
USERS = {
    "ali": ["Reader"],
    "ayse": ["Contributor"],
    "can": ["VM Operator", "Storage Blob Data Contributor"],
    "deniz": [] # No roles assigned
}

# --- RBAC Logic Simulation ---

def check_permission(user: str, resource_type: str, action: str) -> bool:
    """
    Checks if a given user has permission to perform an action on a resource type.
    This simulates Azure's Role-Based Access Control (RBAC).
    """
    if user not in USERS:
        print(f"Error: User '{user}' not found.")
        return False

    # Get the roles assigned to the user
    user_roles = USERS[user]
    
    # Iterate through each role the user has
    for role_name in user_roles:
        if role_name not in ROLES:
            print(f"Warning: Role '{role_name}' assigned to '{user}' is not defined.")
            continue
        
        # Get the permissions associated with the current role
        role_permissions = ROLES[role_name]
        
        # Check if the desired (resource_type, action) is in the role's permissions
        # This is the core RBAC check: does any assigned role grant the permission?
        if (resource_type, action) in role_permissions:
            return True  # Permission granted by this role
            
    return False # No assigned role grants the permission

# --- Demonstration --- 
if __name__ == "__main__":
    print("--- Azure RBAC Simulation ---")
    print("This script simulates how Role-Based Access Control (RBAC) works in Azure.")
    print("It demonstrates assigning roles to users and checking their permissions based on those roles.")
    print("-------------------------------\n")

    test_cases = [
        ("ali", "Virtual Machine", "read"),         # Ali (Reader) should read VM -> True
        ("ali", "Virtual Machine", "write"),        # Ali (Reader) should NOT write VM -> False
        ("ayse", "Storage Account", "delete"),      # Ayse (Contributor) should delete Storage -> True
        ("can", "Virtual Machine", "start"),        # Can (VM Operator) should start VM -> True
        ("can", "Storage Account", "list_keys"),    # Can (Storage Blob Data Contributor) should NOT list keys -> False
        ("can", "Storage Account", "read"),         # Can (Storage Blob Data Contributor) should read Storage -> True
        ("deniz", "SQL Database", "backup"),        # Deniz (No roles) should NOT backup DB -> False
        ("ayse", "SQL Database", "backup")          # Ayse (Contributor) should backup DB -> True
    ]

    for user, resource, action in test_cases:
        has_access = check_permission(user, resource, action)
        status = "GRANTED" if has_access else "DENIED"
        print(f"User '{user}' attempting to '{action}' on '{resource}': Access {status}")

    print("\n--- End of Simulation ---")
    print("This example illustrates how Azure RBAC helps manage access by assigning roles, ")
    print("rather than managing individual permissions for each user on every resource.")



def detectUser(user):
    if user.role == 1:
        return 'shopperdashboard'
    elif user.role == 2:
        return 'custdashboard'
    elif user.role is None and user.is_superadmin:
        return '/admin'
    return 'login'
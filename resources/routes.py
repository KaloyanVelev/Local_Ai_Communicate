from resources.user import UserRegisterResource, UserLogInResource, UserPrivateInfoResource, UserPlanUpgradeResource, ShowUsersResource, TestResource
routes = [
    (UserRegisterResource, '/register'),
    (UserLogInResource, '/login'),
    (UserPrivateInfoResource, '/secret'),
    (UserPlanUpgradeResource, '/planUpgrade'),
    (ShowUsersResource, '/showusers'),
    (TestResource, '/'),
]

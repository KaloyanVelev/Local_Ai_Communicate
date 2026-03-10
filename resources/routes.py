from resources.ai import AIChatResource, ChatHistoryResource
from resources.user import UserRegisterResource, UserLogInResource, UserPrivateInfoResource, UserPlanUpgradeResource, ShowUsersResource, TestResource
routes = [
    (UserRegisterResource, '/register'),
    (UserLogInResource, '/login'),
    (UserPrivateInfoResource, '/secret'),
    (UserPlanUpgradeResource, '/planUpgrade'),
    (ShowUsersResource, '/showUsers'),
    (AIChatResource, '/ai/chat'),
    (ChatHistoryResource, '/ai/history/all'),
    (TestResource, '/'),
]

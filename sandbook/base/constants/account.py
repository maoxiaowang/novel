from general.core.settings import defaults

# User & Groups
WORK_MANAGER_GROUP_ID = 11
USER_MANAGER_GROUP_ID = 12
COMMON_USER_GROUP_ID = 15

BUILTIN_GROUPS = [
    {'id': WORK_MANAGER_GROUP_ID, 'name': '作品管理员', 'description': '管理作品，如审核，屏蔽，解封，删除等。'},
    {'id': USER_MANAGER_GROUP_ID, 'name': '用户管理员', 'description': '管理用户，如禁言，封号，删除评论等。'},
    {'id': COMMON_USER_GROUP_ID, 'name': '普通用户', 'description': '-'},
]
BUILTIN_GROUP_NAMES = [item['name'] for item in BUILTIN_GROUPS]
MANAGEMENT_GROUP_IDS = [WORK_MANAGER_GROUP_ID, USER_MANAGER_GROUP_ID]

SYSTEM_ROBOT_ID = 101

BUILTIN_USERS = [
    {
        'id': SYSTEM_ROBOT_ID, 'username': 'system', 'nickname': '机器人一号',
        'email': 'robot1@%s' % defaults.get('domain_name'), 'is_robot': True,
        'password': 'gRnV7fq1cAVa', 'avatar': 'default/avatars/system.jpg',
    },
    {
        'id': 1000, 'username': 'test', 'nickname': '测试账号',
        'email': 'test@%s' % defaults.get('domain_name'), 'is_robot': True,
        'password': 'gRnV7fq1cAVa', 'avatar': 'default/avatars/system.jpg'
    },
    {
        'id': 1, 'username': 'admin', 'nickname': '大Boss',
        'email': 'big_boss@%s' % defaults.get('domain_name'), 'is_robot': False,
        'password': 'admin@sandbook', 'avatar': 'default/avatars/system.jpg',
        'groups': [WORK_MANAGER_GROUP_ID, USER_MANAGER_GROUP_ID]
    },
    {
        'id': 2, 'username': 'novel_admin', 'nickname': '小说审核',
        'email': 'novel@%s' % defaults.get('domain_name'), 'is_robot': False,
        'password': 'admin@sandbook', 'avatar': 'default/avatars/system.jpg',
        'groups': [WORK_MANAGER_GROUP_ID]
    },
{
        'id': 3, 'username': 'user_admin', 'nickname': '用户管理',
        'email': 'big_boss@%s' % defaults.get('domain_name'), 'is_robot': False,
        'password': 'admin@sandbook', 'avatar': 'default/avatars/system.jpg',
        'groups': [USER_MANAGER_GROUP_ID]
    },
]

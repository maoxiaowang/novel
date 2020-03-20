from general.core.settings import defaults

# User & Groups

BUILTIN_GROUPS = [
    {'id': 11, 'name': '作品管理员', 'description': '管理作品，如审核，屏蔽，解封，删除等。'},
    {'id': 12, 'name': '用户管理员', 'description': '管理用户，如禁言，封号，删除评论等。'},
    {'id': 15, 'name': '普通用户', 'description': '-'},
]
BUILTIN_GROUP_NAMES = [item['name'] for item in BUILTIN_GROUPS]
MANAGEMENT_GROUP_IDS = [11, 12]

SYSTEM_ROBOT_ID = 101
BUILTIN_USERS = [
    {
        'id': SYSTEM_ROBOT_ID, 'username': 'system', 'nickname': '机器人一号',
        'email': 'robot1@%s' % defaults.get('domain_name'), 'is_robot': True,
        'password': 'gRnV7fq1cAVa', 'avatar': 'default/avatars/system.jpg'
    },
    {
        'id': 1000, 'username': 'test', 'nickname': '测试账号',
        'email': 'test@%s' % defaults.get('domain_name'), 'is_robot': True,
        'password': 'gRnV7fq1cAVa', 'avatar': 'default/avatars/system.jpg'
    },
]

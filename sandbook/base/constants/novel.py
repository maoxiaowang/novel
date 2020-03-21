import copy


# Novel

DEFAULT_COVER = 'default/covers/default.png'
NOVEL_STATUS_UNAPPROVED = 1  # 未审核
NOVEL_STATUS_ACTIVE = 2  # 连载中
NOVEL_STATUS_FINISHED = 3  # 已完结
NOVEL_STATUS_BLOCKED = 4


# Category

CATEGORY_FANTASY_ID = 1
BUILTIN_CATEGORIES = [
    {'id': CATEGORY_FANTASY_ID, 'name': '奇幻', 'description': '奇幻'}
]
BUILTIN_SUBCATEGORIES = [
    {'id': 1, 'name': '剑与魔法', 'category_id': 1, 'description': '剑与魔法'},
    {'id': 2, 'name': '史诗奇幻', 'category_id': 1, 'description': '史诗奇幻'},
    {'id': 3, 'name': '魔幻深渊', 'category_id': 1, 'description': '魔幻深渊'},
    {'id': 4, 'name': '科幻奇幻', 'category_id': 1, 'description': '科幻奇幻'},
    {'id': 5, 'name': '女巫与火', 'category_id': 1, 'description': '女巫与火'},
    {'id': 6, 'name': '奇幻之歌', 'category_id': 1, 'description': '奇幻之歌'},
]
ALL_CATEGORIES = copy.deepcopy(BUILTIN_CATEGORIES)
for _c in ALL_CATEGORIES:
    _c['sub'] = list()
    for _s in BUILTIN_SUBCATEGORIES:
        if _s['category_id'] == _c['id']:
            _c['sub'].append(_s)


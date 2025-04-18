# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drftokit', 'drftokit.only']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2', 'djangorestframework>=3.11']

setup_kwargs = {
    'name': 'drftokit',
    'version': '0.1.5',
    'description': 'DRF tokit.',
    'long_description': '## Usage Examples\n\n### view\n```\n# Example usage in a DRF ViewSet:\nclass UserViewSet(OrmOnlyViewMixin, ModelViewSet):\n    queryset = User.objects.all()\n    serializer_class = UserSerializer\n\n    def get_queryset(self):\n        qs = super().get_queryset()\n        return self.hook_orm_fields(qs)\n```\n\n### orm service\n\n```\nimport json\nimport logging\nfrom common.init.init_django import initialize_django\n\ninitialize_django()\nfrom common.serializers.only import OrmOnlyServiceMixin\nfrom apps.user.srv import UserSrv\nfrom apps.user.serializers import UserSerializer\n\n\nlogger = logging.getLogger(\'debug\')\n\n\ndef main():\n    # 在 ORM 查询中使用 only，并取出第一个对象用于序列化\n    qs = UserSrv.queryset.filter(pk__lt=10)\n    qs_o = OrmOnlyServiceMixin.only(serializer_class=UserSerializer, qs=qs)\n    logger.info(f"qs_o_query: {qs_o.query}")\n    """\n    qs_o_query: \n    SELECT \n        `user`.`id`, `user`.`username`, `user`.`nickname`, `user`.`avatar` \n    FROM `user` \n    WHERE (`user`.`deleted` = False AND `user`.`id` < 10) ORDER BY `user`.`id` DESC \n    """\n\n    # s_a = OrmOnlySrv(s=UserSerializer, qs=qs)\n    # logger.info(f"data {s_a.data_list}")\n    #\n    # s_o = OrmOnlySrv(s=UserSerializer, qs=qs)\n    # logger.info(f"data {s_o.data}")\n    return\n\n\nif __name__ == \'__main__\':\n    main()\n```\n\n### drf list serializer\n\n* orm_only_fields\n\n```\nclass TplListSerializer(UpdateInfoSerializer, CreatorInfoSerializer, TplSerializer):\n    """\n    列表: 简化字段，避免复杂逻辑\n    """\n    class Meta:\n        model = Tpl\n        orm_only_fields = True\n        fields = [\n            "id",\n            "name",\n        ]\n```\n\n```\nclsass Viewxxx(OrmOnlyViewMixin):\n    def get_queryset(self):\n        queryset = self._get_queryset()\n        queryset = self.hook_orm_fields(qs=queryset)\n        return queryset\n```',
    'author': 'pytools',
    'author_email': 'hyhlinux@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)

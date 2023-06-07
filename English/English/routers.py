from rest_framework import routers


class ReadOnlyRouter(routers.SimpleRouter):
    routes = [
        routers.Route(
            url="^{prefix}$",
            mapping={"get": "list"},
            name="{basename}-list",
            detail=False,
            initkwargs={"suffix": "List"}
        ),
        routers.Route(
            url="^{prefix}/{lookup}$",
            name='{basename}-detail',
            detail=True,
            mapping={"get": "retrieve"},
            initkwargs={"suffix": "Detail"}
        ),
        routers.DynamicRoute(
            url=r"^{prefix}/{lookup}/{url_path}$",
            name="{basename}--{url_name}",
            detail=True,
            initkwargs={}
        )
    ]


class ComfortRouter(routers.SimpleRouter):
    routes = [
        routers.Route(
            url="^{prefix}$",
            mapping={"get": "list"},
            name="{basename}-list",
            detail=False,
            initkwargs={"suffix": "List"}
        ),
        routers.Route(
            url="^{prefix}$",
            mapping={'post': "create"},
            name="{basename}-create",
            detail=False,
            initkwargs={"suffix": "Create"}
        ),
        routers.Route(
            url="^{prefix}/{lookup}$",
            name='{basename}-detail',
            detail=True,
            mapping={"get": "retrieve"},
            initkwargs={"suffix": "Detail"}
        ),
        routers.DynamicRoute(
            url=r"^{prefix}/{url_path}$",
            name="{basename}--{url_name}",
            detail=True,
            initkwargs={}
        )
    ]


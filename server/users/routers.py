from rest_framework import routers


class AccountRouter(routers.DefaultRouter):
    routes = [
        routers.Route(
            url="^{prefix}$",
            mapping={
                "get": "list",
                "post": "create",
                "delete": "destroy",
                "patch": "partial_update"
            },
            name="{basename}",
            detail=False,
            initkwargs={"suffix": "List"}
        ),
        routers.DynamicRoute(
            url=r"^{prefix}/{url_path}$",
            name="{basename}__{url_name}",
            detail=True,
            initkwargs={}
        )
    ]

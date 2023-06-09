from rest_framework import routers


class AccountRouter(routers.DefaultRouter):
    routes = [
        routers.Route(
            url="^{prefix}{trailing_slash}$",
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
            url=r"^{prefix}/{url_path}{trailing_slash}$",
            name="{basename}_{url_name}",
            detail=False,
            initkwargs={}
        )
    ]

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .serializer import ServerSerializer, ChannelSerializer

server_list_docs = extend_schema(
    responses=ServerSerializer(many=True),
    parameters=[
        OpenApiParameter(
            name="category",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Category of servers to retrieve",
        ),
        OpenApiParameter(
            name="qty",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Quantity of servers to retrieve"
        ),
        OpenApiParameter(
            name="user_id",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="Filter's servers by current authenticated user's id"
        ),
        OpenApiParameter(
            name="server_id",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Filters servers by provided id"
        ),
        OpenApiParameter(
            name="with_num_members",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="Shows number of memebers in each server if true"
        )
    ]
)
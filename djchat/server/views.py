from django.shortcuts import render
from rest_framework import viewsets
from .models import Server
from .serializer import ServerSerializer, ChannelSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.db.models import Count
from .schema import server_list_docs
# Create your views here.

class ServerListViewSet(viewsets.ViewSet):

    queryset = Server.objects.all()


    @server_list_docs
    def list(self, request):
        """Retrieves a list of servers based on various filter parameters.
        This method processes an HTTP GET request and returns a list of server objects.
        The list can be filtered by category, quantity, user ID, server ID, and whether the number of members should be included.
        It raises an AuthenticationFailed exception if a user-specific query is made without authentication.
        It also raises a ValidationError if the server ID is not found or invalid.

        Parameters:
        - request (HttpRequest): The HTTP request object containing query parameters.

        Query Parameters:
        - category (str): Filter servers by the given category name.
        - qty (int): Limit the number of servers returned.
        - user_id (bool): If 'true', filter servers by the authenticated user's ID.
        - server_id (str): Filter servers by the given server ID.
        - with_num_members (bool): If 'true', include the number of members in each server.

        Returns:
        - Response: A Django REST framework Response object containing serialized server data.
        """
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("user_id") == "true"
        by_server = request.query_params.get("server_id")
        with_num_members = request.query_params.get("with_num_members") == "true"

        if by_user and not request.user.is_authenticated:
            raise AuthenticationFailed(detail="You must be logged in order to use this action.")

        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user and request.user.is_authenticated:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)
        else:
            raise AuthenticationFailed("Unauthorized")

        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        if by_server:
            if not request.user.is_authenticated:
                raise AuthenticationFailed()
            
            try:
                self.queryset = self.queryset.filter(id=by_server)
                if not self.queryset.exists():
                    raise ValidationError(detail=f"Server with id {by_server} not found")
            except ValueError:
                    raise ValidationError(detail=f"Server value error")


        if qty:
            self.queryset = self.queryset[:int(qty)]

        serializer = ServerSerializer(self.queryset, many=True, context={"num_members": with_num_members})
        return Response(serializer.data)

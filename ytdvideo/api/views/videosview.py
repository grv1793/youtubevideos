from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

from api.authentication import ApiKeyAuthentication

from api.controllers import VideoController


class VideoView(generics.ListCreateAPIView):
    authentication_classes = (ApiKeyAuthentication, )

    def get(self, request):
        controller = VideoController(
            request=request
        )
        response_data = controller.get_response_data()
        return Response(data=response_data, status=status.HTTP_200_OK)



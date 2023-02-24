from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Image
from .serializers import ImageSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
import time
from rest_framework import generics, permissions
from .serializers import ImageHistorySerializer
from .models import ImageHistory


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class ImageRatingView(APIView):
    """
    API endpoint to rate images.
    """
    def __init__(self):
        self.images = Image.objects.all()
        self.image_index = 0
        self.start_time = time.time()

    def get(self, request):
        # get next image or return "thank you" message
        if self.image_index < len(self.images):
            serializer = ImageSerializer(self.images[self.image_index])
            return Response(serializer.data)
        else:
            return Response({"message": "Thank you!"})

    def post(self, request):
        # check if 5 seconds have elapsed since last interaction
        if time.time() - self.start_time >= 5:
            # reset start time and move to next image
            self.start_time = time.time()
            self.image_index += 1

            # check if all images have been rated
            if self.image_index >= len(self.images):
                return Response({"message": "Thank you!"})

            # show missed image message and return next image
            return Response({"message": f"You missed image {self.images[self.image_index-1].name}.",
                             "image": ImageSerializer(self.images[self.image_index]).data})

        # handle user action
        image_id = request.data.get('image_id')
        action = request.data.get('action')

        if action == 'reject':
            # show reject message and move to next image
            self.start_time = time.time()
            self.image_index += 1
            if self.image_index < len(self.images):
                serializer = ImageSerializer(self.images[self.image_index])
                return Response({"message": f"You rejected image {self.images[self.image_index-1].name}.",
                                 "image": serializer.data})
            else:
                return Response({"message": "Thank you!"})

        elif action == 'accept':
            # show accept message and move to next image
            self.start_time = time.time()
            self.image_index += 1
            if self.image_index < len(self.images):
                serializer = ImageSerializer(self.images[self.image_index])
                return Response({"message": f"You rejected image {self.images[self.image_index-1].name}.",
                                 "image": serializer.data})
                


class ImageHistoryList(generics.ListAPIView):
    serializer_class = ImageHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ImageHistory.objects.filter(user=user).order_by('-timestamp')
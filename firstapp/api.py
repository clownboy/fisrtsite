from .models import Comment,Userinfo
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view


class CommentSerializer(serializers.ModelSerializer):

    talker = serializers.SerializerMethodField()
    talkerhead = serializers.SerializerMethodField()
    def get_talker(self, obj):
        if obj.talker:
           talker=obj.talker.nickname
           return talker
    def get_talkerhead(self, obj):
         talkerhead = str(obj.talker.headlogo)
         return talkerhead

    class Meta:
        model = Comment
        fields = "__all__"
        depth = 1

@api_view(['GET'])
def getcomment(request):
   artical = request.GET['id']
   if request.method =='GET':
     comment = Comment.objects.filter(artical=artical)
     serializer = CommentSerializer(comment,many=True)
     return Response(serializer.data)

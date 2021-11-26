from django.shortcuts import render
from django.contrib.auth.models import User


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from api.models import Comment
from api.serializers import CommentSerializer

# Create your views here.


class CommentListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = CommentSerializer(Comment.objects.all() ,many = True)
        return Response(serializer.data , status = status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CommentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status = status.HTTP_201_CREATED)
        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)



class CommentDetailApiView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self , pk):
        try:
            return Comment.objects.get(pk = pk)
        except Comment.DoesNotExist:
            return None
    
    def get(self,request , pk):
        comment = self.get_object(pk)
        if not comment :
            return Response({'Not Found' : 'Object does not exist'} , status = status.HTTP_400_BAD_REQUEST)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    def put(self , request , pk):
        comment = self.get_object(pk)
        if not comment :
            return Response({'Not Found' : 'Object does not exist'} , status = status.HTTP_400_BAD_REQUEST)
        
        serializer = CommentSerializer(comment , data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request , pk):
        comment = self.get_object(pk)
        if not comment :
            return Response({'Not Found' : 'Object does not exist'} , status = status.HTTP_400_BAD_REQUEST)
        
        data = request.data
        
        comment.msg = data.get('msg' , comment.msg)
        comment.user = User.objects.get(id = data.get('user')) if data.get('user') else comment.user
        comment.created_on = data.get('created_on' , comment.created_on)
        
        comment.save()
        serializer = CommentSerializer(comment)
        
        return Response(serializer.data)
        
    def delete(self , request , pk):
        comment = self.get_object(pk)
        
        if not comment :
            return Response({'Not Found' : 'Object does not exist'} , status = status.HTTP_400_BAD_REQUEST)
        else:
            comment.delete()
            return Response(
                {'success' : 'Object deleted successfully !'},
                status = status.HTTP_200_OK
            )
        
        
        
from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from notes_app.serializers import RegisterSerializer,NotesSerializer,TaskSerializer
from notes_app.models import NotesDb,TaskDb
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User
from rest_framework import serializers



# Create your views here.
class RegistrationView(APIView):

    def post(self,request):

        serializer_instance = RegisterSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data={
                "Message":"Registration Successful......"
            })
        else:
            return Response(data=serializer_instance.errors)

    def get(self,request):

        qs = User.objects.all()
        serializer = RegisterSerializer(qs,many=True)
        return Response(data=serializer.data)

class NotesListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):

        notes = NotesDb.objects.filter(user=request.user)
        serializer_instance = NotesSerializer(notes,many=True)
        return Response(data=serializer_instance.data)

    def post(self,request):

        serializer_instance = NotesSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save(user=request.user)
            return Response(data=
                            {
                                "Message":"The Notes added successfully...",
                                'Notes Details': serializer_instance.data
                            })
        return Response(data=serializer_instance.errors)


class NotesRetrieveUpdateDeleteView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request,id):

        notes = get_object_or_404(NotesDb,id=id)
        if notes.user == request.user:
            serializer_instance = NotesSerializer(notes)
            return Response(data=serializer_instance.data)
        raise PermissionDenied("Access Denied....!!")

    def put(self,request,id):

        notes = get_object_or_404(NotesDb,id=id)
        if notes.user != request.user:
            raise PermissionDenied("Access Denied....!")
        serializer_instance = NotesSerializer(data=request.data,instance=notes)
        if serializer_instance.is_valid():
            serializer_instance.save(user=request.user)
            return Response(data=
                            {
                                "Message":"The Notes added successfully...",
                                'Notes Details': serializer_instance.data
                            })
        return Response(data=serializer_instance.errors)

    def delete(self,request,id):
        notes = get_object_or_404(NotesDb,id=id)
        if notes.user != request.user:
            raise PermissionDenied("Access Denied....!")
        else:
            notes.delete()
            return Response(data={"Message":"Note Deleted Successfully....."})

class LogOutView(APIView):

    permission_classes = [IsAuthenticated]
    def post(self,request):

        request.user.auth_token.delete()
        return Response({
            "Message":"Logout Success"
        })

#task related views

class TaskCreateListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):

        tasks = TaskDb.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks,many=True)
        return Response(serializer.data)
    
    def post(self,request):

        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {"Message":"task added",
                 "task":serializer.data
                 })
        return Response(serializer.errors)

class TaskRetrieveUpdateDeleteView(APIView):

    permission_classes = [IsAuthenticated]
    
    def get_task(self,request,task_id):
        
        return get_object_or_404(TaskDb,id=task_id,user=request.user)

    def get(self,request,task_id):
        
        task = self.get_task(request,task_id)
        serializer = TaskSerializer(task,many=True)
        return Response(data=serializer.data)

    def put(self,request,task_id):

        task = self.get_task(request,task_id)
        if task.user != request.user:
            raise serializers.ValidationEroor("Access Denied....!!!")
        
        serializer_instance = TaskSerializer(data=request.data,instance=task)
        
        if serializer_instance.is_valid():
            serializer_instance.save(user=request.user)
            return Response({
                "Message":"Task updated successfully...",
                "Updated task": serializer_instance.data
            })
        return Response(serializer_instance.errors)

    def delete(self,request,task_id):

        task = self.get_task(request,task_id)
        if task.user != request.user: 
            raise serializers.ValidationEroor("Access Denied....!!!")
        task.delete()
        return Response({"Messae":"Task deleted successfully...."})






    

    
    


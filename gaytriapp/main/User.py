from django.contrib.auth.models import User 

def CreateUser():
 user1 = User.objects.create_user("nixon","niaoasd@gamil.com","hello")
 user1.first_name = 'nixon'
 user1.last_name = 'nelson'
 user1.save()
def DeleteUser():
    pass
def EditUser():
    pass
def EditPermission():
    pass
def RemovePermission():
    pass

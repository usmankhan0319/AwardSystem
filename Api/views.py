from ntpath import join
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
import Api.usable as uc
from .models import *
from passlib.hash import django_pbkdf2_sha256 as handler
import jwt 
import datetime
from decouple import config
from django.db.models import F

# ADMIN AND EMPLOYEE LOGIN API
class account(APIView):
    def post (self,request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            fetcAccount = Account.objects.filter(email=email).first()
            if fetcAccount:
                if handler.verify(password,fetcAccount.password):
                    if fetcAccount.role == "admin":
                        access_token_payload = {
                                'id': fetcAccount.id,
                                'name':fetcAccount.username,
                                'email':fetcAccount.email, 
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=22),
                                'iat': datetime.datetime.utcnow(),

                        }

                        access_token = jwt.encode(access_token_payload,config('adminkey'),algorithm = 'HS256')

                        data = {'username':fetcAccount.username,'email':fetcAccount.email,}
                        return Response({"status":True,"message":"Login Successlly","token":access_token,"admindata":data},200)
                    else:
                        access_token_payload = {
                                'id': fetcAccount.id,
                                'name':fetcAccount.username,
                                'email':fetcAccount.email, 
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=22),
                                'iat': datetime.datetime.utcnow(),

                        }

                        access_token = jwt.encode(access_token_payload,config('employeekey'),algorithm = 'HS256')

                        data = {'username':fetcAccount.username,'email':fetcAccount.email,}
                        return Response({"status":True,"message":"Login Successlly","token":access_token,"employeedata":data},200)
                
                else:
                    return Response ({"status":False,"message":"Invalid crediatials"},200)
            else:
                return Response ({"status":False,"message":"Account doesnot access"},200)


        except Exception as e:
            
            message = {'status':'Error','message':str(e)}
            return Response(message)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# PASSWORD ENCRYPT API
class encryptpass(APIView):
    def post(self,request):
        try:    
            passw = handler.hash(request.data.get('passw'))


            return HttpResponse(passw)

        except Exception as e:
            
            message = {'status':'Error','message':str(e)}
            return Response(message)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ADMIN ADD EMPLOYEEE API
class admindataadd(APIView):
    def get(self,request):
        try:
            my_token = uc.tokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                data = Account.objects.filter(role = "employee").values('id','username','email','password').order_by('-id')
                return Response({"status":True,"data":data},200)
        except Exception as e:
            
            message = {'status':'Error','message':str(e)}
            return Response(message)


    def post(self,request):
        try:
            my_token = uc.tokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                username = request.data.get('username')
                email = request.data.get("email")
                password = request.data.get("password") 


                if uc.checkemailforamt(email):
                    if not uc.passwordLengthValidator(password):
                        
                        return Response({"status":False,"message":"Password should not be less than 8 or greater than 20"})
    

                    checkemail = Account.objects.filter(email = email).first()
                    if checkemail:
                        return Response({"status":False,"message":"Email alreay exist"},409)
                    
                    data = Account(username= username,email = email,password = handler.hash(password)) 
                    data.save()

                    return Response({"status":True,"message":"Account Created Successfuly"},201)


                else:
                    return Response({"status":False,"message":"Email format is incorrect"},422)
            
            else:
                return Response({"status":False,"message":"Unauthorized"},status=401)
                
        except Exception as e:
            
            message = {'status':'Error','message':str(e)}
            return Response(message)

    def put(self,request):
        try:
            my_token = uc.tokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                id = request.data.get('id')
                username = request.data.get('username')
                email = request.data.get('email')
                password = request.data.get('password')

                checkaccount = Account.objects.filter(id = id).first()
                if checkaccount:
                    checkaccount.username = username
                    checkaccount.email = email
                    checkaccount.password = password

                    if password  !="nochange":
                        if not uc.passwordLengthValidator(password):
                            return Response({"status":False,"message":"Password should not be less than 8 or greater than 20"})
                        checkaccount.password = handler.hash(password)
                        checkaccount.save() 
                        return Response({"status":True,"message":"Updated Successfully"})
                    else:
                        ({"status":False,"message":"Data not found"})

        except Exception as e:
            
            message = {'status':'Error','message':str(e)}
            return Response(message)


    def delete(self,request):
        try:

            my_token = uc.tokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                id = request.GET['id']
                data = Account.objects.filter(id=id).first()
                if data:
                    data.delete()
                    return Response({"status":True,"message":"Data deleted successfully"})
                else:
                    return Response({"status":False,"message":"Data not found"})

        except Exception as e:
            
            message = {'status':'Error','message':str(e)}
            return Response(message)

class specificdata(APIView):
    def get (self,request):
        try:
            my_token = uc.tokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                id = request.GET['id']
                data = Account.objects.filter(id = id ).values('id','username','email','password')
                if data:
                    return Response ({"status":True,"data":data},200)
                else:
                    return Response({"status":False,"message":"Data not found"})

        except Exception as e:
            
            message = {'status':'Error','message':str(e)}
            return Response(message)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ADMIN ADD QUESTIONS
class questions (APIView):
    def get(self,request):
        try:

            my_token = uc.tokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                data = Questions.objects.all().values('id','question').order_by("-id")
                return Response ({"status":True,"data":data },200)
        except Exception as e:
            
            message = {'status':'Error','message':str(e)}
            return Response(message)

    def post(self,request):
        try:
            my_token = uc.tokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                question = request.data.get("question")
                getAccouuntid = Account.objects.filter(id = my_token['id']).first()

                data = Questions(question = question, Accouuntid = getAccouuntid)
                data.save()

                return Response({"status":True,"message":"Question Created successfull"})

            
            else:
                return Response({"status":False,"message":"Unauthorized"},status=401)

        except Exception as e:
            
            message = {'status':'Error','message':str(e)}
            return Response(message)

    def put(self,request):
        try:
            my_token = uc.tokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                    id =  request.data.get('id')
                    question = request.data.get("question")
                    getAccouuntid = Account.objects.filter(id = my_token['id']).first()


                    checkquestions = Questions.objects.filter(id = id).first()
                    if checkquestions:
                        checkquestions.question = question
                        checkquestions.save()

                        return Response({"status":True,"message":"Question Successfully Updated"})

                    else:
                        return Response({"status":False,"message":"Data not found"})
        except Exception as e:
            
            message = {'status':'Error','message':str(e)}
            return Response(message)


    def delete(self,request):
        try:
            my_token = uc.tokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                id = request.GET['id']
                data = Questions.objects.filter(id = id).first()
                if data:
                    data.delete()
                    return Response({"status":True,"message":"Data Deleted Successfully"})
                else:
                    return Response({"status":False,"message":"Data not found"})
        except Exception as e:
            
            message = {'status':'Error','message':str(e)}
            return Response(message)


class getSpecificquestion(APIView):
    def get(self,request):
        try:
            my_token = uc.tokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                id = request.GET['id']
                data = Questions.objects.filter(id = id).values("id","question").first()
                if data:
                    return Response({"status":True,"data":data},200)
                else:
                    return Response({"status":False,"message":"Data not found"})
        
        except Exception as e:
            
            message = {'status':'Error','message':str(e)}
            return Response(message)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# EMPLOYEE ANSWER
class addanswer(APIView):

    def get(self,request):
        try:
            my_token = uc.employeetokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                data = Answer.objects.all().values('id','answer').order_by("-id")
                return Response({"status":True,"data":data},200)

        except Exception as e:
            
            message = {'status':'Error','message':str(e)}
            return Response(message)

    def post(self,request):
        try:
            my_token = uc.employeetokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                answer = request.data.get("answer")
                Questionid = request.data.get('Questionid')
                
                getAccouuntid = Account.objects.filter(id = my_token['id']).first()
                getQid = Questions.objects.filter(id = Questionid).first()
                
                if getQid:

            
                    data = Answer(answer = answer , Accouuntid = getAccouuntid ,Qid = getQid)
                    data.save()
                    return Response({"status":True,"messsage":"Answer Can be successsfuuly added"})

                else:
                    return Response({"status":False,"message":"Data not found"})
            else:
                return Response({"status":False,"message":"Unauthorized"},status=401)
        except Exception as e:
            
            message = {'status':'Error','message':str(e)}
            return Response(message)


    def put(self,request):
        try:
            my_token = uc.employeetokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                    
                id = request.data.get("id")
                answer = request.data.get("answer")
                Questionid = request.data.get('Questionid')

                
                getAccouuntid = Account.objects.filter(id = my_token['id']).first()
                getQid = Questions.objects.filter(id = Questionid).first()
            
                checkanswers = Answer.objects.filter(id = id ).first()
                if checkanswers:
                    checkanswers.answer = answer
                    checkanswers.save() 
                
                return Response({"status":True,"message":"Answer Updated Successfully"})

            else:
                return Response({"status":False,"message":"Unauthorized"},status=401)

        except Exception as e:
            
            message = {'status':'Error','message':str(e)}
            return Response(message)


    def delete(self,request):
        try:
            my_token = uc.employeetokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                id = request.GET["id"]
                data = Answer.objects.filter(id = id).first()
                if data:
                    data.delete()
                    return Response({"status":True,"message":"Data deleted successfully"})
                
                else:
                    return Response({"status":False,"message":"Data not found"})


            else:
                return Response({"status":False,"message":"Unauthorized"},status=401)

        except Exception as e:
            
            message = {'status':'Error','message':str(e)}
            return Response(message)



class getspecificanswerdata(APIView):
    def get(self,request):
        try:
            my_token = uc.employeetokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                id = request.GET['id']
                data = Answer.objects.filter(id = id).values('id','answer').first()
                if data:
                    return Response({"status":True,"data":data},200)
                
                else:
                    return Response({"status":False,"message":"Data not found"})


            else:
                return Response({"status":False,"message":"Unauthorized"},status=401)
        
        except Exception as e:
            
            message = {'status':'Error','message':str(e)}
            return Response(message)



class employeeealldata(APIView):
    def get (self,request):
        my_token = uc.tokenauth(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:

            id = request.GET['id'] 
            data = Answer.objects.filter(Accouuntid__id = id).values('answer',Question=F('Qid__question'),username=F('Accouuntid__username'))
            return Response ({"status":True,'data':data},200)

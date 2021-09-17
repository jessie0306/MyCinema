from django.shortcuts import render
import MySQLdb
from django.http.response import HttpResponseRedirect
from mycinema.models import Members, Nonmembers, TicketsNm, Tickets
from django.db.models import Max
import numpy as np
import datetime


config = {
    'host':'127.0.0.1',
    'user':'root',
    'password':'123',
    'database':'dbmember',
    'port':3306,
    'charset':'utf8',
    'use_unicode':True
}
# Create your views here.
def logoutFunc(request):
    request.session.clear() # 모든 세션 지우기
    return  render(request, 'main3.html') 


def MainFunc(request):
    if "id" in request.session:
        id = request.session['id']
        return  render(request, 'aftermain2.html',{"id":id})  #로그인 후 메인
    else:
        return  render(request, 'main3.html') 


def LoginFunc(request):
    return render(request, 'login.html')

def AftermainFunc(request):
    memid = request.POST.get('id')
    print(memid)
    request.session['id'] = memid
    id = request.session['id']
    pw = request.POST.get('pw')
    print(pw)
    sql = "select * from `3team`.members where member_id='{}' and member_pw='{}'".format(memid,pw)
    conn = MySQLdb.connect(**config)
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    #print(data)
    if data != None:
        return render(request, 'aftermain.html', {'id':id})
    else:
        return render(request, 'login.html') 
    
def NomemberFunc(request):
    return render(request, 'nomember.html')

def NomembercheckFunc(request):
    yy = request.POST.get('yy')
    print(yy)
    mm = request.POST.get('mm')
    print(mm)
    dd = request.POST.get('dd')
    print(dd)
    newtel = request.POST.get('newtel')
    nm_id = Nonmembers.objects.values('nm_id').get(nm_tel = newtel) # nm_tel = newtel는 겹치는 변수, values는 겹치는 것중에 Nonmembers에서 nm_id만 뽑아낸 변수
    nm_id = nm_id['nm_id']
    print(nm_id)  
    all = TicketsNm.objects.all().filter(nm_id = nm_id) # TicketsNm의 nm_id와 Nonmembers nm_id가 같은 것중에 TicketsNm 모두 가져옴
    pw = request.POST.get('pw')   
    sql = "select * from `3team`.Nonmembers where nm_birth=\"{}-{}-{}\" and nm_tel=\"{}\" and nm_pw={}".format(yy,mm,dd,newtel,pw)
    conn = MySQLdb.connect(**config) 
    cursor = conn.cursor() 
    cursor.execute(sql)  
    data = cursor.fetchone()
    #print(data)
    request.session['nm_id'] = nm_id
    if data != None:  
        return render(request, 'nomembercheck.html', {'all':all})
    else:
        return render(request, 'nomember.html')
    
def Nomember2Func(request):
    return render(request, 'nomember2.html')

def Nomembercheck2Func(request):
    yy = request.POST.get('yy')
    print(yy)
    mm = request.POST.get('mm')
    print(mm)
    dd = request.POST.get('dd')
    print(dd)
    newtel = request.POST.get('newtel')
    pw = Nonmembers.objects.values('nm_pw').get(nm_tel = newtel) #nm_pw는 dict 1개 일 때 읽어주기
    pwd = []
    for val in pw.values(): 
        pwd.append(val)
        print(pwd)
    sql = "select * from `3team`.Nonmembers where nm_birth=\"{}-{}-{}\" and nm_tel=\"{}\"".format(yy,mm,dd,newtel)
    conn = MySQLdb.connect(**config)
    cursor = conn.cursor() 
    cursor.execute(sql)
    data = cursor.fetchone() 
    #print(data) 
    if data != None: 
        return render(request, 'nomembercheck2.html', {'yy':yy, 'mm':mm, 'dd':dd, 'newtel':newtel, 'pwd':pwd})
    else: 
        return render(request, 'nomemberpwfind.html')  
    
def NomembercreateFunc(request):
    return render(request, 'Nomembercreate.html')

def Nomembercreate2Func(request):
    yy = request.POST.get('yy')
    print(yy)
    mm = request.POST.get('mm')
    print(mm)
    dd = request.POST.get('dd')
    print(dd)
    newtel = request.POST.get('newtel')
    pw = request.POST.get('pw')
    nm_id = Nonmembers.objects.all().aggregate(Max('nm_id'))['nm_id__max'] + 1
    print(nm_id)
    Nonmembers(
            nm_id = nm_id,
            nm_birth = str(yy) + "-" + str(mm) + "-" + str(dd),
            nm_tel = newtel,
            nm_pw = pw           
        ).save()
    sql = "select * from `3team`.Nonmembers where nm_birth=\"{}-{}-{}\" and nm_tel=\"{}\" and nm_pw={}".format(yy,mm,dd,newtel,pw)
    conn = MySQLdb.connect(**config)
    cursor = conn.cursor() 
    cursor.execute(sql)
    data = cursor.fetchone() 
    #print(data)
    request.session['nm_id'] = nm_id   
    if data != None: 
        return render(request, 'nomembercreate2.html',{'nm_id':nm_id})
    else: 
        return render(request, 'nomembercreate.html')
    
def NomembermainFunc(request):
    return render(request, 'Nomembermain.html')




def PaymentFunc(request):
    id2 = request.session['id2']['id'] # 회원
    print(id2)
    seat2 = Tickets.objects.values('seat').get(ticket_id = id2)
    print(seat2) # 딕트 key값 알아내기
    seat2= seat2['seat'] # 딕트 value값 출력
    seat2= seat2.split(",") # 딕트 리스트화로 ,로 구분하기
    seat2= len(seat2) # 리스트 갯수
    print("-----------------")
    print(seat2)
    
    seat2 = np.multiply(seat2,10000)
    if 'id' in request.session:
        memid = request.session['memid']
        return render(request, 'payment.html', {'seat2':seat2,'id':memid})
    else:
        return render(request, 'nopayment.html', {'seat2':seat2})

def NopaymentFunc(request): 
    nm_id = request.session['nm_id']['nm_id'] # 비회원
    print(nm_id)
    seat3 = Tickets.objects.values('seat').get(ticket_id = nm_id)
    print(seat3)
    seat3= seat3['seat']
    seat3= seat3.split(",")
    seat3= len(seat3)
    seat3= np.multiply(seat3,10000)
    memid = '비회원'  
    return render(request, 'nopayment.html', {'seat3':seat3, 'id':memid,})
 
def PaymentresultFunc(request):
    if 'id' in request.session:
        ticket_id = Tickets.objects.all().aggregate(Max('ticket_id'))['ticket_id__max'] + 1
        date =  request.session['ticketInform']['date']
        print(date)
        house =  request.session['ticketInform']['house']
        time =  request.session['ticketInform']['time']
        print(time)
        cine_name =  request.session['ticketInform']['cine']
        seat =  request.session['seat']
        movie_id =  request.session['ticketInform']['movie_id']
        movie_name =  request.session['ticketInform']['movie_name']
        member_id = request.session['id']
        ticket_date = date + " " + time + ":00"  
        Tickets(
                ticket_id = ticket_id,
                ticket_date = datetime.datetime.strptime(ticket_date, '%Y-%m-%d %H:%M:%S') ,
                cine_name = cine_name + " " + house,             
                seat = seat,            
                movie_id = movie_id,             
                movie_name = movie_name,           
                member_id = member_id            
            ).save()
        return render(request, 'paymentresult.html') 
    else:
        ticket_id = TicketsNm.objects.all().aggregate(Max('ticket_id'))['ticket_id__max'] + 1
        date =  request.session['ticketInform']['date']
        print(date)
        house =  request.session['ticketInform']['house']
        time =  request.session['ticketInform']['time']
        print(time)
        cine_name =  request.session['ticketInform']['cine']
        seat =  request.session['seat']
        movie_id =  request.session['ticketInform']['movie_id']
        movie_name =  request.session['ticketInform']['movie_name']
        nm_id = request.session['nm_id']
        ticket_date = date + " " + time + ":00"  
        TicketsNm( 
                ticket_id = ticket_id,
                ticket_date = datetime.datetime.strptime(ticket_date, '%Y-%m-%d %H:%M:%S') ,
                cine_name = cine_name + " " + house,             
                seat = seat,            
                movie_id = movie_id,             
                movie_name = movie_name,           
                nm_id = nm_id            
            ).save()
        return render(request, 'paymentresult.html') 


def Aftermain2Func(request):
    memid = request.session['memid']
    return render(request, 'Aftermain2.html',{'id':memid})

def NopaymentresultFunc(request):
    return render(request, 'nopaymentresult.html')

def TicketingcancelFunc(request):
    nm_id = request.session['nm_id']
    print(nm_id)
    sql = "delete from `3team`.tickets_nm where nm_id = {}".format(nm_id)
    conn = MySQLdb.connect(**config)
    cursor = conn.cursor() 
    cursor.execute(sql) 
    conn.commit()
    data = cursor.fetchone()  
    #print(data)  
    if data != None: 
        return render(request, 'ticketingcancel.html')
    else: 
        return render(request, 'nomembercheck.html')  
    

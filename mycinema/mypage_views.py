
# Create your views here.
from django.shortcuts import render
from datetime import datetime, timezone, timedelta
from mycinema.models import Members, Tickets, Movies, Cinemas
import pandas as pd
import json
import MySQLdb
from django.http.response import HttpResponseRedirect

config = {
    'host':'127.0.0.1',
    'user':'root',
    'password':'123',
    'database':'3team',
    'port':3306,
    'charset':'utf8',
    'use_unicode':True
}


 

def ListFunc(request):
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
    print(data)
    if data != None:
        return HttpResponseRedirect('/') 
    else:
        return render(request, 'login.html') 


# Create your views here.
def MainFunc(request):
    request.session['id'] = None
    return  render(request, 'main.html')


def AftermainFunc2(request):   #if문으로 로그인여부확인해서 메인 다르게 줌 
    if "id" in request.session:
        id = request.session['id']
        return  render(request, 'aftermain2.html',{"id":id})  #로그인 후 메인
    else:
        return  render(request, 'main3.html')   #로그인 전 메인
        

def LoginCheck(request):
    if "id" in request.session:
        mem_id = request.session['id']
 
        return MyList(request)
    else:
        return render(request, 'login.html')
        
 

def MyList(request):
    #예매내역
    ##회원이름
    mem_id = request.session['id']
    name = Members.objects.values('member_name').filter(member_id=mem_id)[0]['member_name']
    
    ##DB에서 예매내역 가져오기
    ticket = Tickets.objects.filter(member_id=mem_id).order_by('-ticket_date')
    
    ##예매데이터 저장
    watched = []     #본 영화 정보 저장
    willwatch = []   #볼 영화 정보 저장
    mov_id = []      #봤거나 볼 영화 아이디 저장
    for t in ticket:
        if (t.ticket_date-datetime.now(timezone(timedelta(hours=9)))).days < 0:  #관림일이 현재시간보다 미래이면 볼 영화로 저장
            #print(datetime.now(timezone(timedelta(hours=9))))   #한국시간대로
            watched_dic = {}
            watched_dic['ticket_id'] = t.ticket_id
            watched_dic['ticket_date'] = t.ticket_date
            watched_dic['cine_name'] = t.cine_name
            watched_dic['seat'] = t.seat
            watched_dic['movie_id'] = t.movie_id
            watched_dic['movie_name'] = t.movie_name
            watched_dic['member_id'] = t.member_id
            mov_id.append(t.movie_id)
            watched.append(watched_dic)
        else:
            willwatch_dic = {}
            willwatch_dic['ticket_id'] = t.ticket_id
            request.session['willwatch_ticket_id'] = t.ticket_id  #관람예정 예매아이디 세션에 저장
            willwatch_dic['ticket_date'] = t.ticket_date
            willwatch_dic['cine_name'] = t.cine_name
            willwatch_dic['seat'] = t.seat
            willwatch_dic['movie_id'] = t.movie_id
            willwatch_dic['movie_name'] = t.movie_name
            willwatch_dic['member_id'] = t.member_id
            mov_id.append(t.movie_id)
            willwatch.append(willwatch_dic)
    watched = watched[:5]  #최신순 5개만 보여줌. DB에서 날짜순으로 추출했으므로 위에서부터 5건만 가져오면됨
    
    return preferList(request, name, watched, willwatch, mov_id)  #preferList 함수 호출


def preferList(request, name, watched, willwatch, mov_id):    
    #선호장르 선호배우
    ##ticket과 달리 중복되는 영화가 있으면 1건만 출력됨 가져와서 따로 처리를 해야한다.         
    ##한 영화를 여러번 본 경우에도 count에 포함하려면 이렇게
    prefer = []
    for mid in mov_id:
        prefer.extend(Movies.objects.filter(movie_id=mid)) #append로하면 중첩리스트로 저장됨

    genre = []  #선호장르 저장
    actor = []  #선호배우 저장
    ##각 컬럼에 복수개의 장르, 배우가 하나의 문자열로 저장되어 있기 때문에 append로 하면 중첩리스트로 저장됨 -> extend 사용
    for m in prefer:   
        for g,a in zip([m.genre],[m.actor]):
            genre.extend(g.split(','))   #','를 기준으로 문자열 분리
            actor.extend(a.split(','))

    ##선호장르 이름, 순위, 개수 
    ## -> DataFrame으로 저장하여 순위와 개수를 구한 후 3위까지만 저장한다. (등수 중복가능)
    genre_cnt = pd.DataFrame(genre, columns=['genre'])['genre'].value_counts()
    genre_rank = genre_cnt.rank(method='dense', ascending=False)
    genre_df = pd.concat([genre_rank,genre_cnt], axis=1).reset_index()[:3]
    genre_df.columns=['genre','rank','cnt']

    genre_label = list(genre_df['genre'])  
    genre_rank = list(genre_df['rank'])
    genre_percent = list(round((genre_df['cnt']/genre_df['cnt'].sum())*100))  #장르 백분율
    
    #genre_cnt = list(genre_df['cnt'])
    
    ##그래프를 작성하기 위한 데이터셋. 이 데이터 셋들을 JSON으로 만들고 html에 넘김
    genre_datas = {
        'labels': genre_label,
        'datasets': [{
            'label': '관람횟수',
            'data': genre_percent,
            'backgroundColor': [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)'
        ],
        'borderColor': [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)'
        ],
        'borderWidth': 1
        }]
    }
    genre_json = json.dumps(genre_datas)

    ##선호배우 이름, 순위, 개수  선호장르와 동일함
    actor_cnt = pd.DataFrame(actor, columns=['actor'])['actor'].value_counts()
    actor_rank = actor_cnt.rank(method='dense', ascending=False)
    actor_df = pd.concat([actor_rank,actor_cnt], axis=1).reset_index()[:5]
    actor_df.columns=['actor','rank','cnt']
    
    actor_label = list(actor_df['actor'])
    actor_rank = list(actor_df['rank'])
    actor_cnt = list(actor_df['cnt'])  
    
    actor_datas = {
        'labels': actor_label,
        'datasets': [{
            'label': '관람횟수',
            'data': actor_cnt,
            'backgroundColor': [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)'
        ],
        'borderColor': [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)'
        ],
        'borderWidth': 1
        }]
    }
    actor_json = json.dumps(actor_datas)
    
    return recommendFunc(request, name, watched, willwatch, mov_id,  
                         genre_label, genre_json, actor_json)  #recommendFunc 함수 호출
    

def recommendFunc(request, name, watched, willwatch, mov_id, genre_label,
                   genre_json, actor_json):
    #영화 추천
    ##장르가 하나의 문자열로 묶여있기 때문에 in 연산자로 자료 추출 불가
    ##모든 영화를 가져와서 비교하고 선호장르와 일치하는 영화 중 3개만 추출한다. 봤거나 볼 영화는 제외
    movieList = Movies.objects.exclude(movie_id__in=mov_id).order_by('movie_id') #나중에 최신순으로 변경
    recommend = []
    for m in movieList:
        m.genre = m.genre.split(',')  #문자열로 묶인 장르 ','를 기준으로 분리
        for i in m.genre:
            if i in genre_label: 
                recommend_dic = {}
                recommend_dic['mname'] = m.movie_name
                recommend_dic['msrc'] = m.poster_src
                recommend.append(recommend_dic)  
                #영화의 장르가 선호장르에 있으면 recommend 리스트에 추가하고 반복문 탈출
                break   
    recommend = recommend[:3] #최신순 3개만 보여줌
    
    context = {'name':name, 'watched':watched, 'willwatch':willwatch, 'genre_json':genre_json,
               'actor_json':actor_json,'recommend':recommend}  #html로 넘겨줄 변수들 저장

    return render(request, 'mypage.html', context)


def watchList(request):
    if 'id' in request.session:
        mem_id = request.session['id']
    else:
        return render(request, 'login.html')
    
    #mem_id = request.POST['mem_id']
    tickets = Tickets.objects.filter(member_id=mem_id).order_by('-ticket_date')
    
    watched = []     #본 영화 정보 저장
    for t in tickets:
        if (t.ticket_date-datetime.now(timezone(timedelta(hours=9)))).days < 0:  #관림일이 현재시간보다 미래이면 볼 영화로 저장
            watched_dic = {}
            watched_dic['ticket_id'] = t.ticket_id
            watched_dic['ticket_date'] = t.ticket_date
            watched_dic['cine_name'] = t.cine_name
            watched_dic['seat'] = t.seat
            watched_dic['movie_id'] = t.movie_id
            watched_dic['movie_name'] = t.movie_name
            watched_dic['member_id'] = t.member_id
            watched.append(watched_dic)
    
    return render(request, 'watchList.html', {'watchList':watched})


def cancelCheck(request):

    return render(request, 'cancelCheck.html')


def cancelOk(request):
    try:
        mem_id = request.session['id']
        cancel_pw = request.POST['cancelpw']
        cantic_id = request.session['willwatch_ticket_id']
        
        mem_pw = Members.objects.values('member_pw').get(member_id=mem_id)['member_pw']
        print(mem_pw)
        print(cancel_pw)
        delRec = Tickets.objects.get(ticket_id=cantic_id)
        
        if cancel_pw == mem_pw:
            delRec.delete()
            return render(request, 'cancelOk.html')
        else:
            return render(request, 'cancelerror.html')
    except:
        return render(request, 'cancelerror.html')

     
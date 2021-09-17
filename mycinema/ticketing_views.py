from django.shortcuts import render
from mycinema.models import Cinemas, MovieSchedules
from django.http.response import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

def ticketlogin(request):
    if "id" in request.session:
        mem_id = request.session['id']
        return selectLoction(request)
    elif "nm_id" in request.session:
        mem_id = request.session['nm_id']
        return selectLoction(request)
    else:
        return render(request, 'login.html')



def selectLoction(request):  #바로예매 버튼을 누르면 예매화면으로
    cine = Cinemas.objects.all().order_by('location')
    
    # 지역별로 저장
    cine_seoul = []
    cine_gyeonggi = []
    cine_daegu = []
    cine_busan = []
    cine_gangwon = []
    cine_incheon = []
    cine_jeolla = []
    cine_jeju = []
    
    for c in cine:
        cine_dic = {}
        cine_dic['cine_name'] = c.cine_name
        cine_dic['location'] = c.location
        cine_dic['current_movies'] = c.current_movies
        if cine_dic['location'] == '서울':
            cine_seoul.append(cine_dic)
        elif cine_dic['location'] == '경기':
            cine_gyeonggi.append(cine_dic)
        elif cine_dic['location'] == '대구':
            cine_daegu.append(cine_dic)
        elif cine_dic['location'] == '부산':
            cine_busan.append(cine_dic)
        elif cine_dic['location'] == '강원':
            cine_gangwon.append(cine_dic)
        elif cine_dic['location'] == '인천':
            cine_incheon.append(cine_dic)
        elif cine_dic['location'] == '전라':
            cine_jeolla.append(cine_dic)
        elif cine_dic['location'] == '제주':
            cine_jeju.append(cine_dic)

    context = {'cine_seoul':cine_seoul, 'cine_gyeonggi':cine_gyeonggi, 'cine_daegu':cine_daegu,
               'cine_busan':cine_busan, 'cine_gangwon':cine_gangwon, 'cine_incheon':cine_incheon,
               'cine_jeolla':cine_jeolla, 'cine_jeju':cine_jeju}

    return render(request, 'ticketing.html', context)
     

@csrf_exempt
def selectCineMovies(request):
    data = MovieSchedules.objects.all()
    #print(data)
    
    data_list = []
    for d in data:
        data_dic = {}
        data_dic['schedule_id'] = d.schedule_id
        data_dic['cine_id'] = d.cine_id
        data_dic['cine_name'] = d.cine_name
        data_dic['movie_id'] = d.movie_id
        data_dic['movie_name'] = d.movie_name
        data_dic['house_num'] = d.house_num
        data_dic['movie_time'] = d.movie_time
        data_dic['movie_date'] = str(d.movie_date)
        
        data_list.append(data_dic)

    schedule = json.dumps(data_list)
    
    return HttpResponse(schedule, content_type="application/json")


@csrf_exempt
def ticketCheck(request):
    if request.method == 'POST':
        ticketInform = {}
        ticketInform['cine'] = request.POST['cine']
        ticketInform['movie_name'] = request.POST['movie_name']
        ticketInform['movie_id'] = request.POST['movie_id']
        ticketInform['date'] = request.POST['date']
        ticketInform['house'] = request.POST['time'].split('\u2002')[0]
        ticketInform['time'] = request.POST['time'].split('\u2002')[1]
        request.session['ticketInform'] = ticketInform
        #print(ticketInform) 
        
        return JsonResponse({ 'success': True })
    
    
from django.shortcuts import render
from mycinema.models import Tickets, TicketsNm
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def goSeating(request):  # 예매화면에서 좌석선택으로   
    ticket = request.session['ticketInform']
    ticket['poster_src'] = ticket['movie_id'] + '.png'
    #print(ticket)
    
    # 예매화면에서 선택한 극장,영화,날짜,상영관,시간이 같은 기존의 예매내역(회원기준)
    data1 = Tickets.objects.filter(cine_name__contains = ticket['cine'])\
                                    .filter(cine_name__contains = ticket['house'])\
                                    .filter(ticket_date__contains = ticket['date'])\
                                    .filter(ticket_date__contains = ticket['time'])\
                                    .filter(movie_id = int(ticket['movie_id']))\
                                    .values("seat")   
                                    # 필터 결과 중 "seat"칼럼의 값을 dict로                  
    print(data1)  # <QuerySet [{'seat': 'E12,E13'}]>
    
    # 예매화면에서 선택한 극장,영화,일자,상영관,시간이 같은 기존의 예매내역(비회원기준)
    data2 = TicketsNm.objects.filter(cine_name__contains = ticket['cine'])\
                                    .filter(cine_name__contains = ticket['house'])\
                                    .filter(ticket_date__contains = ticket['date'])\
                                    .filter(ticket_date__contains = ticket['time'])\
                                    .filter(movie_id = int(ticket['movie_id']))\
                                    .values("seat") 
    #print(data2)  #<QuerySet [{'seat': 'D11'}]>
    
    seat_occupied = ''
    try:
        for d in data1:
            seat_occupied += d['seat'] + ','
        for d in data2:
            seat_occupied += d['seat'] + ','
        #print(seat_occupied)
    except:
        seat_occupied = ''
    
    return render(request, 'seating.html', {'seat_occupied':seat_occupied, 'ticket':ticket})

@csrf_exempt
def seatCheck(request):
    if request.method == 'POST':
        request.session['seat'] = request.POST['seat']
        request.session['price'] = request.POST['price']
        
        return JsonResponse({ 'success': True })


def goPay(request):
    price = request.session['price']
    if 'id' in request.session:
        memid = request.session['id']  
        return render(request, 'payment.html',{'price': price, 'memid' : memid})
    else: 
        return render(request, 'payment.html',{'price': price})





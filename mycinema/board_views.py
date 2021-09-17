from django.shortcuts import render
from mycinema.models import  Voc, MymovieRe


from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from datetime import datetime
from django.http.response import HttpResponseRedirect
 

def B_MainFunc(request):
    if "id" in request.session:
        id = request.session['id']
        return render(request, "board_main2.html",{"id":id})
    else:
        return  render(request, 'login.html') 

    

# 고객의 소리 누르면 여기로
def VocFunc(request):# 고객의 소리 넣으면 문의작성이 제일 먼저 뜨게
    member_id = request.session['id']
    return render(request, "voc_insert.html"  , {"member_id": member_id})

def Voc_insertokFunc(request):# 내용을 db에 넣어준다.
    if request.method == "POST":
        try:
            # group 번호 얻기
            gbun = 1    # 그룹번호
            datas = Voc.objects.all()  #자료를 읽고
            print(datas)
            
            if datas.count() != 0:  # 자료가있다면
                gbun = Voc.objects.latest('post_id').post_id +1  # 아이디 번호를 읽고 1를 추가
            
            Voc(
                member_id = request.POST.get("member_id"),
                voc_pw = request.POST.get("voc_pw"),
                voc_type = request.POST.get("voc_type"),
                title = request.POST.get("title"),
                cont = request.POST.get("cont"),    
                bip = request.META['REMOTE_ADDR'],
                bdate =   datetime.now(),
                readcnt = 0,
                gnum = gbun,
                onum = 0,
                nested = 0  # 마지막 , 는 있어도 되고 없어도 되고
                ).save()
        except Exception as e:
            print('추가 오류 : ', e)
            
    return HttpResponseRedirect('/Voclist')  # 추가후 목록보기


def Voc_ListFunc(request):# voc 목록이 보이는곳
    member_id = request.session['id']
    datas = Voc.objects.all().order_by("-gnum","onum")    # 댓글이 있는 경우
    # 페이징 처리
    paginator = Paginator(datas, 5) # 한화면에 5행씩 출력
    try: 
        page = request.GET.get("page")#  해당 페이지를 받아 들어옴
    except:
        page = 1    # 페이지 저장안하면 1페이지로
    
    
    try:
        data = paginator.page(page)# 해당 페이지를 받아서 출력
        
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)# 현재 페이지에 남기
    return render(request, "voc_list.html", {"data": data, "member_id":member_id})


def Voc_ContentFunc(request):
    member_id = request.session['id']
    data = Voc.objects.get(post_id = request.GET.get('post_id'))
    data.readcnt = int(data.readcnt) +1 # 조회수증가
    data.save() # 수정이된것
    page = request.GET.get("page")  # 페이지 읽고                                                            
    return render(request, "voc_content.html", { "data_one":data  ,"page": page, "member_id": member_id})  # 넘겨줌
    
    
    
def Voc_UpdateFunc(request):    # 수정대상 자료 보기
    try:
        member_id = request.session['id']
        data = Voc.objects.get(post_id = request.GET.get("post_id")) # post_id를 읽어서 해당자료 가지고옴
    except Exception as e:
        print("Voc_UpdateFunc err :",e)
        
    return render(request, "voc_update.html", {  'data_one': data ,"member_id": member_id })



def Voc_UpdateokFunc(request):    # 수정
    upRec = Voc.objects.get(post_id = request.POST.get("post_id"))   # 수정할 자료를 꺼내온다.
    if upRec.voc_pw == request.POST.get("up_voc_pw"):    # 입력된 up_voc_pw와 실제 비번이 맞으면 수정수행
        upRec.member_id = request.POST.get("member_id")
        upRec.voc_type = request.POST.get("up_voc_type")
        upRec.title = request.POST.get("up_title")
        upRec.cont= request.POST.get("up_cont")
        upRec.save()
    else:
        return render(request, "voc_error.html")
    return HttpResponseRedirect('/Voclist' )  # 수정후 목록보기



def Voc_DeleteFunc(request):    # 삭제할거냐 질문 페이지
    try:
        member_id = request.session['id']
        data = Voc.objects.get(post_id= request.GET.get("post_id")) # 아이디가 일치하는 놈 데이터에 넣어
    except Exception as e:
        print("Voc_DeleteFunc er: ", e)
        
    return render(request, "voc_delete.html", { "data_one": data ,"member_id": member_id })


def Voc_DeleteokFunc(request):    # 삭제
    member_id = request.session['id']   
    delRec = Voc.objects.get(post_id = request.POST.get("post_id"))
    if delRec.voc_pw == request.POST.get("del_voc_pw"):
        delRec.delete()
        return HttpResponseRedirect("/Voclist")   # 삭제후 목록보기
    else:
        return render(request, "voc_error.html",  {  "member_id": member_id })
 



def Voc_contentpwckFunc(request):    # 내용 볼거냐 질문페이지
    try:
        member_id = request.session['id']
        page = request.GET.get("page")  # 페이지 읽고                                                            
        data = Voc.objects.get(post_id= request.GET.get("post_id")) # 아이디가 일치하는 놈 데이터에 넣어
    except Exception as e:
        print("Voc_contentpwckFunc er: ", e)
        
    return render(request, "voc_content_pwcheck.html", { "data_one": data ,"page": page ,"member_id": member_id })




def Voc_contentpwchokFunc(request):    # 비번맞으면 요청소환,
    member_id = request.session['id']
    data = Voc.objects.get(post_id = request.POST.get("post_id"))
    if data.voc_pw == request.POST.get("voc_pw"):
        data.readcnt = int(data.readcnt) +1 # 조회수증가
        data.save()
        page = request.GET.get("page")
        
        return render(request, "voc_content.html", { "data_one":data  ,"page": page, "member_id": member_id })  # 넘겨줌    
    else:
        return render(request, "voc_error.html",  {  "member_id": member_id })

    

def Voc_Search2Func(request):    # 검색
    if request.method == "GET":
        s_type = request.GET.get("s_type")
        s_value= request.GET.get("s_value")
        #print(s_type, '  ',s_value )    # title    ssss
        if s_type == "title":
            datas = Voc.objects.filter(title__contains =s_value).order_by("-post_id")
        elif s_type == "member_id":
            datas = Voc.objects.filter(member_id=s_value).order_by("-post_id")
        elif s_type == "voc_type":
            datas = Voc.objects.filter(voc_type =s_value).order_by("-post_id")
        
        paginator = Paginator(datas, 5) # 한화면에 5행씩 출력
        page = request.GET.get("page")
            
        try:
            member_id = request.session['id']
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)           
        return render(request, "voc_searchlist.html", {'data':data, "s_type":s_type,"s_value": s_value, "member_id": member_id})
    else:
        return HttpResponseRedirect("/Voclist")



 

def Voc_SearchFunc(request):    # 검색
    if request.method == "POST":
        s_type = request.POST.get("s_type")
        s_value= request.POST.get("s_value")
        #print(s_type, '  ',s_value )    # title    ssss
        if s_type == "title":
            datas = Voc.objects.filter(title__contains =s_value).order_by("-post_id")
        elif s_type == "member_id":
            datas = Voc.objects.filter(member_id=s_value).order_by("-post_id")
        elif s_type == "voc_type":
            datas = Voc.objects.filter(voc_type =s_value).order_by("-post_id")
        
        paginator = Paginator(datas, 5) # 한화면에 5행씩 출력
        page = request.GET.get("page")
            
        try:
            member_id = request.session['id']

            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)           
        return render(request, "voc_searchlist.html", {'data':data, "s_type":s_type,"s_value": s_value, "member_id": member_id})
    else:
        return HttpResponseRedirect("/Voclist")


def Voc_replyFunc(request):    # 댓글
    try:
        data = Voc.objects.get(post_id = request.GET.get("post_id")) # 댓글 대상 원글 읽기
        member_id = request.session['id']
    except Exception as e:
        print("ReplyFunc err : ", e)
    return render(request, "voc_reply.html", {'data_one':data , "member_id":member_id})

def Voc_replyokFunc(request):
    if request.method == "POST":
        try:
            regnum = int(request.POST.get("gnum"))  # 그룹넘버
            reonum = int(request.POST.get("onum"))  # 그룹넘버밑에잇는거
            
            tempRec = Voc.objects.get(post_id = request.POST.get("post_id"))
            old_gnum = tempRec.gnum
            old_onum = tempRec.onum
            
            if old_onum >= reonum and old_gnum == regnum:   # 같은 그룹이고 올드오넘이 더커 그러면 오넘 갱신
                old_onum = old_onum +1  # onum 갱신
                
            # 댓글 저장
            Voc(
                member_id = request.POST.get("member_id"),
                voc_pw = request.POST.get("voc_pw"),
                voc_type = request.POST.get("voc_type"),
                title = request.POST.get("title"),
                cont = request.POST.get("cont"),    
                bip = request.META['REMOTE_ADDR'],
                bdate =   datetime.now(),
                readcnt = 0,
                gnum = regnum,
                onum = old_onum,
                nested = int(request.POST.get("nested")) +1 # int로 타입바꾸고 +1

                ).save()
            
        except Exception as e:
            print("ReplyokFunc err : ", e)

    return HttpResponseRedirect("/Voclist")
 


from mycinema.models import  Voc, MymovieRe

# 내영화추천
def MMRFunc(request):# 내영화추천누르면 리스트가 나오게
    # 검색값이 없을경우
    member_id = request.session['id']

    datas = MymovieRe.objects.all().order_by("-gnum","onum")  
    paginator = Paginator(datas, 5) # 한화면에 5행씩 출력
    try: 
        page = request.GET.get("page")#  해당 페이지를 받아 들어옴
    except:
        page = 1    # 페이지 저장안하면 1페이지로
    
    
    try:
        data = paginator.page(page)# 해당 페이지를 받아서 출력
        
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)# 현재 페이지에 남기
    return render(request, "mmr_list.html", {"data": data ,  "member_id": member_id}) 




def MMR_Search2Func(request):    # 검색
    if request.method == "GET":
        s_type = request.GET.get("s_type")
        s_value= request.GET.get("s_value")
        #print(s_type, '  ',s_value )    # title    ssss
        if s_type == "title":
            datas = MymovieRe.objects.filter(title__contains =s_value).order_by("-post_id")
        elif s_type == "member_id":
            datas = MymovieRe.objects.filter(member_id=s_value).order_by("-post_id")
        elif s_type == "like_genre":
            datas = MymovieRe.objects.filter(like_genre =s_value).order_by("-post_id")
        
        paginator = Paginator(datas, 5) # 한화면에 5행씩 출력
        page = request.GET.get("page")
            
        try:
            member_id = request.session['id']
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)           
        return render(request, "mmr_searchlist.html", {'data':data, "s_type":s_type,"s_value": s_value ,  "member_id": member_id})
    else:
        return HttpResponseRedirect("/MMR")




def MMR_SearchFunc(request):    # 검색
    if request.method == "POST":
        s_type = request.POST.get("s_type")
        s_value= request.POST.get("s_value")
        #print(s_type, '  ',s_value )    # title    ssss
        if s_type == "title":
            datas = MymovieRe.objects.filter(title__contains =s_value).order_by("-post_id")
        elif s_type == "member_id":
            datas = MymovieRe.objects.filter(member_id=s_value).order_by("-post_id")
        elif s_type == "like_genre":
            datas = MymovieRe.objects.filter(like_genre =s_value).order_by("-post_id")
        
        paginator = Paginator(datas, 5) # 한화면에 5행씩 출력
        page = request.GET.get("page")
            
        try:
            member_id = request.session['id']
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)           
        return render(request, "mmr_searchlist.html", {'data':data, "s_type":s_type,"s_value": s_value,  "member_id": member_id})
    else:
        return HttpResponseRedirect("/MMR")
 
 



def MMR_insertFunc(request):# 글추가 페이지로 가기 
    member_id = request.session['id']
    return render(request, "mmr_insert.html", {"member_id": member_id})



# MymovieRe

def MMR_insertokFunc(request):# db에 글저장
    if request.method == "POST":
        try:
            # group 번호 얻기
            gbun = 1    # 그룹번호
            datas = MymovieRe.objects.all()  #자료를 읽고
            print(datas)
            
            if datas.count() != 0:  # 자료가있다면
                gbun = MymovieRe.objects.latest('post_id').post_id +1  # 아이디 번호를 읽고 1를 추가
            print(request.POST.get("member_id"))

            MymovieRe(
                member_id = request.POST.get("member_id"),
                re_pw = request.POST.get("re_pw"),
                like_genre = request.POST.get("like_genre"),
                title = request.POST.get("title"),
                cont = request.POST.get("cont"),    
                bip = request.META['REMOTE_ADDR'],
                bdate =   datetime.now(),
                readcnt = 0,
                gnum = gbun,
                onum = 0,
                nested = 0  # 마지막 , 는 있어도 되고 없어도 되고
                ).save()# 직접넘기는거
                
        except Exception as e:
            print('추가 오류 : ', e)
            
    return HttpResponseRedirect('/MMR')  # 추가후 목록보기

# MymovieRe


def MMR_contentFunc(request):
    member_id = request.session['id']
    data = MymovieRe.objects.get(post_id = request.GET.get('post_id'))
    data.readcnt = int(data.readcnt) +1 # 조회수증가
    data.save() # 수정이된것
    page = request.GET.get("page")  # 페이지 읽고                                                            
    return render(request, "mmr_content.html", { "data_one":data  ,"page": page,  "member_id": member_id})  # 넘겨줌






def MMR_DeleteFunc(request):    # 수정대상 자료 보기
    try:
        member_id = request.session['id']
        data = MymovieRe.objects.get(post_id= request.GET.get("post_id")) # 아이디가 일치하는 놈 데이터에 넣어
    except Exception as e:
        print("MMR_DeleteFunc er: ", e)
        
    return render(request, "mmr_delete.html", { "data_one": data, "member_id": member_id })

# MymovieRe

def MMR_DeleteokFunc(request):    # 삭제
    member_id = request.session['id']
    delRec = MymovieRe.objects.get(post_id = request.POST.get("post_id"))
    if delRec.re_pw == request.POST.get("del_re_pw"):
        delRec.delete()
        return HttpResponseRedirect("/MMR")   # 삭제후 목록보기
    else:
        return render(request, "voc_error.html",  {  "member_id": member_id })
 

     

def MMR_UpdateFunc(request):    # 수정대상 자료 보기
    try:
        member_id = request.session['id']
        data = MymovieRe.objects.get(post_id = request.GET.get("post_id")) 
        
    except Exception as e:
        print("MMR_UpdateFunc err :",e)
        
    return render(request, "mmr_update.html", {  'data_one': data, "member_id": member_id})



def MMR_UpdateokFunc(request):    # 수정
    upRec = MymovieRe.objects.get(post_id = request.POST.get("post_id"))   # 수정할 자료를 꺼내온다.
    if upRec.re_pw == request.POST.get("up_re_pw"):    # 입력된 up_voc_pw와 실제 비번이 맞으면 수정수행
        upRec.member_id = request.POST.get("member_id")
        upRec.like_genre = request.POST.get("up_like_genre")
        upRec.title = request.POST.get("up_title")
        upRec.cont= request.POST.get("up_cont")
        upRec.save()
    else:
        return render(request, "mmr_error.html")
    return HttpResponseRedirect('/MMR' )  # 수정후 목록보기





 
def MMR_replyFunc(request):    # 댓글
    try:
        data = MymovieRe.objects.get(post_id = request.GET.get("post_id")) # 댓글 대상 원글 읽기
        member_id = request.session['id']
    except Exception as e:
        print("ReplyFunc err : ", e)
    return render(request, "mmr_reply.html", {'data_one':data,"member_id":member_id })

def MMR_replyokFunc(request):
    if request.method == "POST":
        try:
            regnum = int(request.POST.get("gnum"))  # 그룹넘버
            reonum = int(request.POST.get("onum"))  # 그룹넘버밑에잇는거
            
            tempRec = MymovieRe.objects.get(post_id = request.POST.get("post_id"))
            old_gnum = tempRec.gnum
            old_onum = tempRec.onum
            
            if old_onum >= reonum and old_gnum == regnum:   # 같은 그룹이고 올드오넘이 더커 그러면 오넘 갱신
                old_onum = old_onum +1  # onum 갱신
                
            # 댓글 저장
            MymovieRe(
                member_id = request.POST.get("member_id"),
                re_pw = request.POST.get("re_pw"),
                like_genre = request.POST.get("like_genre"),
                title = request.POST.get("title"),
                cont = request.POST.get("cont"),    
                bip = request.META['REMOTE_ADDR'],
                bdate =   datetime.now(),
                readcnt = 0,
                gnum = regnum,
                onum = old_onum,
                nested = int(request.POST.get("nested")) +1 # int로 타입바꾸고 +1

                ).save()
            
        except Exception as e:
            print("ReplyokFunc err : ", e)

    return HttpResponseRedirect("/MMR")

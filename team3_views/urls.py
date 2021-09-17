"""team3_views URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from mycinema import main_views,  mypage_views, ticketing_views, join_views, movie_views, board_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # main
    path('',main_views.MainFunc),
    path('main',main_views.MainFunc),
    path('login',main_views.LoginFunc), 
    path('logout',main_views.logoutFunc), 
    
    path('ticketingcancel',main_views.TicketingcancelFunc),
    path('aftermain',main_views.AftermainFunc), 
    path('nomember',main_views.NomemberFunc),
    path('nomembercheck',main_views.NomembercheckFunc),
    path('nomember2',main_views.Nomember2Func),
    path('nomembercheck2',main_views.Nomembercheck2Func), 
    path('nomembercreate',main_views.NomembercreateFunc), 
    path('nomembercreate2',main_views.Nomembercreate2Func), 
    path('nomembermain',main_views.NomembermainFunc), 
    path('paymentresult',main_views.PaymentresultFunc), 
     
    # mypage
    path('aftermain2', mypage_views.AftermainFunc2),

    path(r'mypage', mypage_views.LoginCheck),
    path(r'watchList', mypage_views.watchList),
    path(r'logincheck', mypage_views.ListFunc),
    path('cancelCheck', mypage_views.cancelCheck),
    path('cancelOk', mypage_views.cancelOk),
    
    # ticket
    path(r'selectSeat', mypage_views.ListFunc),
    path(r'ticketing', ticketing_views.ticketlogin),
    path('calldb', ticketing_views.selectCineMovies),
    path('ticketCheck', ticketing_views.ticketCheck),    
    path('goSeating', ticketing_views.goSeating),  # 요청명 goSeating로 변경하시면 됩니다
    path('seatCheck', ticketing_views.seatCheck),   
    path('goPay', ticketing_views.goPay),  
    
    # join
    path('join', join_views.JoinFunc),  # 나중에 합칠 때 path('join', views.JoinFunc), 으로 바꾸기
    path('joinok', join_views.JoinokFunc), 
    path('idcheck', join_views.IdcheckFunc), 
    path('telcheck', join_views.TelcheckFunc), 

    # movie
    path('movie', movie_views.MovieFunc),
    path('1', movie_views.into1Func),
    path('2', movie_views.into2Func),
    path('3', movie_views.into3Func),
    path('4', movie_views.into4Func),
    path('5', movie_views.into5Func),
    path('6', movie_views.into6Func),
    
    # board 
    ## 게시판메인
    path( r'bmain'  , board_views.B_MainFunc),
    
    ## voc
    path( r'Voc'  , board_views.VocFunc), # 시작이 insert
    path(  r'Vocinsertok', board_views.Voc_insertokFunc),
    path(  r'Voclist', board_views.Voc_ListFunc),
    path( r'Voccontent'  , board_views.Voc_ContentFunc),
    path(  r'Vocdelete', board_views.Voc_DeleteFunc),
    path( r'Vocdeleteok'  , board_views.Voc_DeleteokFunc),
    path(  r'Vocupdate', board_views.Voc_UpdateFunc),
    path(  r'Vocupdateok', board_views.Voc_UpdateokFunc),
    path( r'Vocsearch'  , board_views.Voc_SearchFunc),
    path( r'Vocsearch2'  , board_views.Voc_Search2Func),
    path( r'Vocreply'  , board_views.Voc_replyFunc),
    path( r'Vocreplyok'  , board_views.Voc_replyokFunc),
    path( r'Voccontentpwcheck'  , board_views.Voc_contentpwckFunc),
    path( r'Voccontentpwchok'  , board_views.Voc_contentpwchokFunc),
    
    
    ## mmr 
    path( r'MMR'  , board_views.MMRFunc),
    path(  r'MMRinsert', board_views.MMR_insertFunc),
    path(  r'MMRinsertok', board_views.MMR_insertokFunc),
    path(  r'MMRcontent', board_views.MMR_contentFunc),
    path(  r'MMRdelete', board_views.MMR_DeleteFunc),        
    path( r'MMRdeleteok'  , board_views.MMR_DeleteokFunc),    
    path(  r'MMRupdate', board_views.MMR_UpdateFunc),
    path(  r'MMRupdateok', board_views.MMR_UpdateokFunc),
    path( r'MMRsearch2'  , board_views.MMR_Search2Func),
    path( r'MMRsearch'  , board_views.MMR_SearchFunc),
    path( r'MMRreply'  , board_views.MMR_replyFunc),
    path( r'MMRreplyok'  , board_views.MMR_replyokFunc),
    
]

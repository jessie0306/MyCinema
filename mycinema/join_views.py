from django.shortcuts import render
from mycinema.models import Members
from django.db.models import Max 

# Create your views here.
def JoinFunc(request):
    return render(request, 'joinwithbgposter.html')

def JoinokFunc(request):
    if request.method == "POST":
        Members(
            #id = Members.objects.all().aggregate(Max('id'))['id__max'] + 1,  # Max 결과를 보면 dict 타입으로 나오므로 ['id__max']로 키를 잡아 값 구하기 +1 
            member_id = request.POST.get('newid'),
            member_pw = request.POST.get('newpwd'),
            member_name = request.POST.get('newname'),
            member_tel = request.POST.get('newtel'),
            birth = request.POST.get('yy') + '-' + request.POST.get('mm') + '-' + request.POST.get('dd'),
            resident_num = request.POST.get('newjumin1') + '-' + request.POST.get('newjumin2'),
            gender = request.POST.get('gen'),
            like_genre = ','.join(request.POST.getlist('like_genre'))  # getlist로 체크된 여러 값들을 리스트 형식으로 가져올 수 있다. 리스트의 값들을 ,를 구분자로 풀기 
        ).save()
        
        member_id = request.POST.get('newid')
        member_name = request.POST.get('newname')
        return render(request, 'joincongrats.html', {'member_id':member_id, 'member_name':member_name})

def IdcheckFunc(request):
    wanted_id = request.GET.get('wanted_id')
    isRegistered = False
    try:
        data = Members.objects.get(member_id = wanted_id)  # ORM
        if data != None:    # 이미 등록되어 있으면
            isRegistered = True
    except Exception as e:
        print('err : ', e)
    return render(request, 'idcheck.html', {'wanted_id':isRegistered})

def TelcheckFunc(request):
    wanted_tel = request.GET.get('wanted_tel')
    isRegistered = False
    try:
        data = Members.objects.get(member_tel = wanted_tel)  # ORM
        if data != None:    # 이미 등록되어 있으면
            isRegistered = True
    except Exception as e:
        print('err : ', e)
    return render(request, 'telcheck.html', {'wanted_tel':isRegistered})


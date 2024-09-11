from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import GuessNumbers
from .forms import PostForm

# Create your views here.
def index(request):

    lottos = GuessNumbers.objects.all() # GuessNumbers의 데이터베이스의 전체 행을 가져옴

    return render(request, 'lotto/default.html', {'lottos':lottos}) # 3개의 매개변수 전달해야 함(request(유저 요청), html파일, dic)


def hello(request):
    return HttpResponse("<h1 style='color:red;'>Hello, world!</h1>")


def post(request):

    if request.method == 'POST': # POST 요청이 들어온 경우
        
        form = PostForm(request.POST)

        if form.is_valid():         
            lotto = form.save(commit=False) # save()는 DB에 바로 저장, False로 지정하면 중간 저장일뿐 완전 저장은 X
            lotto.generate()
            return redirect('index') # 특정한 URL로 내보내기, URL의 별명을 매개변수로 주면 됨

    else:
        form = PostForm()
        return render(request, "lotto/form.html", {"form":form})
    

def detail(request, lottokey): # 유저가 입력한 숫자를 얻을 수 있음
    lotto = GuessNumbers.objects.get(id=lottokey) # 테이블에 있는 특정 행 꺼내오기

    return render(request, 'lotto/detail.html', {'lotto':lotto}) # html에 lotto 값 넘겨주기





# index.html
# <input type='text', name='name'></input>
# <input type='text', name='text'></input>
# User가 값을 입력하고, 전송 버튼을 클릭 -> User가 입력한 값을 가지고 HTTP POST request
# user_input_name = request.POST['name'] # html에서 name이 'name'인 input tag에 대해 USER가 입력한 값
# user_input_text = request.POST['text']
# new_row = GuessNumbers(name=user_input_name, text=user_input_text)
# print(new_row.num_lotto)
# print(new_row.name)
# new_row.name = new_row.name.upper()
# new_row.lottos = [np.randint(1, 50) for i in range(6)]
# new_row.save() # 데이터베이스에 하나의 행(레코드) 저장
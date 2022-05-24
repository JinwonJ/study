from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import RegistrationUserSerializer


# POST 로 데이터를 받을 것임을 명시해준다.
@api_view(['POST', ])
# 토큰이 없으면 페이지를 못들어온다. 때문에, 이 페이지에 관해서
# 권한을 다르게 설정해준다.
@permission_classes((permissions.AllowAny,))
def registration_view(request):
    # 요청의 메써드가 POST이면,
    if request.method == 'POST':

        # serializer를 불러와 request.data 를 집어넣는다.
        serializer = RegistrationUserSerializer(data=request.data)

        # 응답으로 보내줄 data의 초기화
        data = {}

        # serializer가 data 맛을 보고 이게 옳다 싶으면
        # .is_valid()를 True로 뱉는다.
        if serializer.is_valid():

            # serializer.save()를 거치면 저장을 한다.
            account = serializer.save()

            # 그치만, 저장이 됐는지를 응답을 해줘야 하므로 아래와 같이 응답데이터를 구성해준다.
            data['response'] = "successfully registred a new user"
            data['email'] = account.email
            data['username'] = account.username
            token = Token.objects.get(user=account).key
            data['token'] = token

        else:
            data = serializer.errors
        return Response(data)


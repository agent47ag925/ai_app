#이 코드를 실행하기 전 fastapi와 uvicorn 설치 먼저 실행해야 함
# pip install fastapi uvicorn

#이 fastapi 파일을 단독으로 실행하기 위한 코드
#uvicorn 파일이름:앱이름 --리로드옵션션
#uvicorn fastapp:app --reload

from fastapi import FastAPI
from pydantic import BaseModel #인풋데이터의 형식을 고정정
#BaseModel 상속후, 내 모델을 만듦 -> 내 모델이 인풋의 형식 고정정

#랭체인으로 답변을 받을 수 있도록 모듈화 코드를 가지고 옴
import LangModule as LM

#일반적인 채팅 형태의 인풋이 들어오는 경우
class user_input(BaseModel):
    inputs : str    #사용자가 쿼리한 내용
    history : list  #사용자의 이전 대화내역

#첨부파일(.jpg, .png같은 그림파일, .pdf)가 같이 들어오는 경우
class user_attach(BaseModel):
    inputs : str    #사용자가 쿼리한 내용
    extension : str #첨부된 파일의 확장자
    attached : str  #변환한 내용

#음성채팅을 입력한 경우
class user_voice(BaseModel):
    inputs : str    #사용자가 쿼리한 내용

class simple(BaseModel):
    text : str
    
app = FastAPI()

@app.post('/normal')
async def normal(inputs:simple):
    print(inputs.text)

#일반채팅
@app.post('/chat')
def chat(input:user_input):
    print(input)
    #input -> 유저의 질문
    #history -> main_chat[]에다 쓰려고

    #메모리가 없음
    response = LM.default_chat(input.inputs)
    print("REST RETURN :" , response)
    return response


#첨부파일을 가지고 있는 채팅
@app.post('/attached')
def attached(input:user_attach):
    #그림 파일 일때를 분리
    if input.extension == '.jpg' or input.extension == '.png':
        LM.picture_chat(input.inputs, input.attached)
    
    #pdf파일 일때를 분리
    else:
        LM.rag_chat(input.inputs, input.attached)


#음성채팅
@app.post('/voice')
def voice(input:user_voice):
    pass

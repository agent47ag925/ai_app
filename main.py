import os
from dotenv import load_dotenv
import json
import time

#웹 및 아키텍쳐를 구상하기 위한 코드 구성
import streamlit as st
import requests #fastapi와 streamlit을 합치기 위한 requests(내부에서 도는 fastapi에 요청을 보냄)
import subprocess #fastapi를 선행 실행시키기 위한 방법


#1. 메뉴 헤더
#2. 채팅(본체)
#3. 라우팅(fastapi에 연결결)
def main_app():
    # print(len(st.session_state.main_chat))
    # 입력이 된 내용을 저장
    # st.session_state.main_chat -> 나와 ai의 히스토리리
    if "main_chat" not in st.session_state:
         st.session_state.main_chat = []

    # 사이드바 설정
    #1. 메뉴 헤더
    st.sidebar.header("모드 선택")
    mode = st.sidebar.radio("", ["일반 채팅", "비주얼 채팅", "문서 채팅"])

    st.sidebar.header("채팅 모델 선택")
    model = st.sidebar.radio("", ["gpt-3.5", "모델 이름 2", "모델 이름 3"])

    # 메인 UI 설정
    # streamlit 부분 -> unsafe_allow_html=True
    #streamlit에서 html과 css 코드를 건드리려면 unsafe_allow_html을 True로 맞추어 놓아야 함함
    st.markdown(
        """
        <style>
        .main-container {
            background-color: #EAEAEA;
            padding: 20px;
            border-radius: 10px;
        }
        .input-box {
            background-color: #A0A0A0;
            padding: 10px;
            border-radius: 5px;
        }
        .send-button {
            background-color: #707070;
            color: white;
            padding: 5px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .user-message {
            background-color: #84c673;
            color = black;
            padding: 10px;
            border-radius: 10px;
            max-width: 60%;
            text-align: right;
            margin-left: auto;  /* 🔥 오른쪽 정렬 */
        }
        .bot-message {
            background-color: #73c2c6;
            color = #18484a;
            padding: 10px;
            border-radius: 10px;
            max-width: 60%;
            text-align: left;
            margin-right: auto;  /* 🔥 왼쪽 정렬 */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    
    # 채팅 내역 출력
    for chat in st.session_state.main_chat:
        if chat["sender"] == "user":
            st.markdown(f'<div class="user-message">{chat["text"]}</div>', unsafe_allow_html=True)
            st.markdown(f'\n')
        else:
            st.markdown(f'<div class="bot-message">{chat["text"]}</div>', unsafe_allow_html=True)
            st.markdown(f'\n')

    # 채팅 입력창
    user_input = st.text_area("", height=100)

    # 버튼 배치
    # 전체 html화면을 6등분해서, 3번째 컬럼(1의 비중) 
    col1, col2, col3 = st.columns([4, 1, 1])
    with col3:
        send_clicked = st.button("보내기")

    st.markdown('</div>', unsafe_allow_html=True)

    #3. fastapi와 라우팅
    # send_cliked = 사용자가 '보내기'를 눌렀을 때 
    # user_input.strip() = 실제로 텍스트 박스에 str있을 때때
    if send_clicked and user_input.strip() :
        st.session_state.main_chat.append({'sender':'user', 'text':user_input})

        #match-case
        match mode:
            case '음성 채팅':
                pass

            case '비주얼 채팅':
                pass 

            case '일반 채팅':
                #fastapi 의 정해진 포트에 신호를 보냄
                #post로 전달됨.
                #data = json.dumps({'inputs':user_input, 'history':[]})
                #fastapi에서 데이터를 받아 줄 때 '정해진 형식'
                response = requests.post(url = f"http://127.0.0.1:8000/chat", 
                                         data = json.dumps({'inputs':user_input, 'history':[]}))       
                
                #print(response -> <200>)
                st.write(f"{response.json()}")
                
                st.session_state.main_chat.append({'sender':'bot', 'text':response.json()})

    #streamlit의 화면을 재렌더링
    st.rerun()



if __name__ == '__main__':
    main_app()


    
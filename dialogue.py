import streamlit as st
from streamlit_option_menu import option_menu

def tabFirst_message():
    st.header('MBTI 보컬 이펙터 설명')
    st.write('요즘은 누군가를 만나자마자 MBTI를 물어보는 시대입니다')
    st.write('MBTI는 사람들의 성격을 16가지로 나누어 설명하는 것입니다')
    st.write('당신의 성격을 알아보는 것도 좋지만,')
    st.write('당신의 보컬을 알아보는 것도 좋지 않을까요?')
    with st.sidebar:
        selected = option_menu("Main Menu",  ["I & E", "S & N", "F & T", "J & P"], default_index=1)
        if selected == "I & E":
            st.write("당신의 보컬은 I형일까요? E형일까요?")
        else:
            st.write("당신의 보컬은 S형일까요? N형일까요?")
        
    if (st.button('자세히 알아보기!')):
        tabFirst_detail()

def tabFirst_detail():
    st.write("... 거짓말이었습니다")
    st.write("")
    st.write("사실 보컬의 MBTI가 아닌 보컬 이펙팅을 같이 알아보고자 합니다")
    st.write("프로들이 사용하는 보컬 이펙팅을 경험해보세요")
    st.write("어떻게 그들은 목소리를 더욱 더 멋지게 했을까요?")
    if (st.button('어떻게?')):
        tabFirst_detail2()

def tabFirst_detail2():
    pass




def tab1_message():
    st.header("How To Use")
    st.write("먼저 당신이 자른 샘플을 이용해 이펙트가 효과적인지 확인하세요")
    st.write("2번 탭에서 오디오의 MBTI 이펙팅을 하나씩 넣어주세요.")
    st.write("ratio에 대해서는 0과 100 사이의 값을 넣어주세요.")
    st.write("이펙트를 적용시키면서 파형과 스펙트로그램을 확인할 수 있습니다")
    st.write("이펙트를 적용시킨 결과를 들어볼 수 있습니다.")
    st.write("만족하시면 3번 탭에서 오디오를 들어보고 다운로드 받으세요")
    st.write("만족하지 않으시면 다시 2번 탭으로 돌아가서 이펙트를 조정하세요")



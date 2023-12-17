import streamlit as st

def tabFirst_message():
    st.header('MBTI 보컬 이펙터 설명')
    st.write('MBTI 컨셉을 이용해 당신의 보컬 소리에 이펙트를 넣어보세요')
    st.write('당신의 보컬을 더욱 더 멋지게 만들어줄 것입니다')
    st.button('자세히 알아보기')
    if (st.button):
        st.write('자세한 설명을 보여줄 것입니다')

def tab1():
    st.header("How To Use")
    st.write("먼저 당신이 자른 샘플을 이용해 이펙트가 효과적인지 확인하세요")
    st.write("2번 탭에서 오디오의 MBTI 이펙팅을 하나씩 넣어주세요.")
    st.write("ratio에 대해서는 0과 100 사이의 값을 넣어주세요.")
    st.write("이펙트를 적용시키면서 파형과 스펙트로그램을 확인할 수 있습니다")
    st.write("이펙트를 적용시킨 결과를 들어볼 수 있습니다.")
    st.write("만족하시면 3번 탭에서 오디오를 들어보고 다운로드 받으세요")
    st.write("만족하지 않으시면 다시 2번 탭으로 돌아가서 이펙트를 조정하세요")

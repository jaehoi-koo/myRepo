import streamlit as st

with st.sidebar:
   wv1 = st.slider("Y", 1, 10)
   wv2 = st.text_input("이름")
   wv3 = st.radio(
       "지역선택",
       ["서울", "인천", "부산"],
       captions=["2020", "2020", "2023"],
       index=None,  # 아무것도 선택되지 않도록 한다.
   )


st.title("Page 1")
st.write("**Page 1**")

st.subheader("링크")
st.page_link("pages/page1.py", label="Page 1", icon='👍')
st.page_link("pages/page2.py", label="Page 2")
st.page_link("pages/page3.py", label="Page 3")
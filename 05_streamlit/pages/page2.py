import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd

st.title("Page 2")
st.write("**Page 2**")


# MySQL 사용시
engine = create_engine('mysql://playdata:1111@localhost/test_db')

# 테이블 데이터 조회
query = "SELECT * FROM member"
df = pd.read_sql(query, engine)

# 데이터 편집 가능한 형태로 표시
edited_df = st.data_editor(df, key='data_editor')

# 데이터가 변경되었는지 확인
if st.session_state['data_editor'] is not None:
    if not edited_df.equals(df):
        # 변경된 행 찾기
        changed_df = edited_df[~edited_df.isin(df)].dropna(how='all')
        
        # SQLAlchemy를 사용한 안전한 업데이트
        with engine.connect() as conn:
            for idx, row in changed_df.iterrows():
                update_stmt = text("""
                    UPDATE member 
                    SET name = :name,
                        email = :email
                    WHERE id = :id
                """)
                conn.execute(
                    update_stmt, 
                    parameters={
                        'name': row['name'],
                        'email': row['email'],
                        'id': row['id']
                    }
                )
                conn.commit()
            
        st.success('데이터가 성공적으로 업데이트되었습니다!')




st.subheader("링크")
st.page_link("06_paging.py", label="Home", icon='🏠')
st.page_link("pages/page1.py", label="Page 1", icon='👍')
st.page_link("pages/page2.py", label="Page 2")
st.page_link("pages/page3.py", label="Page 3")
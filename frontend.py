import streamlit as st
import requests

Base_url="http://127.0.0.1:8000"

st.title("Welcome to Student Management System")
option=st.selectbox("select here",["Update","delete","fetch_detail_one","All_students_details"])
if option=="Update":
    name=st.text_input("Enter Student Name")
    roll=st.number_input("Enter Student Roll Number",step=1)
    address=st.text_input("Enter Student address")
    stm=st.text_input("Enter Student stream")
    clas=st.selectbox("Enter student class",[1,2,3,4,5,6,7,8,9,10,11,12])

    ad=st.button("Add Student")
    if ad:
        data={
            "name":name,
            "roll":roll,
           "clas":clas,
         "address":address,
         "stream": stm    }

        res = requests.post(f"{Base_url}/add_student", json=data)
        st.success(res.json()["message"])
        response_data=res.json()


if option=="delete":
    st.title("Delete Student")
    roll=st.number_input("Enter Student Roll Number",step=1)
    if st.button("Delete"):
        res=requests.delete(f"{Base_url}/delete/{roll}")
        st.warning(res.json()["message"])

if option=="fetch_detail_one":
    st.title("Fetch Student Details")
    roll=st.number_input("Enter Student Roll Number",step=1)
    if st.button("Fetch Details"):
        res=requests.get(f"{Base_url}/student_details/{roll}")
        st.json(res.json())

if option=="All_students_details":
    st.title("All Students Details")
    if st.button("Fetch Details"):
        res=requests.get(f"{Base_url}/student_all")
        st.write(res.json())



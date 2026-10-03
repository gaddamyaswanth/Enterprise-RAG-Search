import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"



st.set_page_config(
    page_title="Employee Portal",
    layout="centered"
)


st.title("🏢 Enterprise HR AI Portal")


if "employee" not in st.session_state:

    st.session_state.employee = None



# LOGIN PAGE

if st.session_state.employee is None:


    st.subheader("Employee Login")


    email = st.text_input(
        "Email"
    )


    password = st.text_input(
        "Password",
        type="password"
    )


    if st.button("Login"):


        response = requests.post(

            f"{API_URL}/login",

            json={

                "email": email,

                "password": password

            }

        )


        data = response.json()


        if "message" in data:

            st.session_state.employee = data

            st.success(
                "Login successful"
            )

            st.rerun()


        else:

            st.error(
                "Invalid login"
            )



# DASHBOARD

else:


    employee = st.session_state.employee


    st.success(
        f"Welcome {employee['employee']}"
    )


    st.subheader("Employee Profile")


    col1, col2 = st.columns(2)


    with col1:

        st.write(
            "Department"
        )

        st.info(
            employee["department"]
        )


    with col2:

        st.write(
            "Role"
        )

        st.info(
            employee["role"]
        )



    st.subheader(
        "Leave Management"
    )


    st.metric(
        "Annual Leave Balance",
        "30 Days"
    )


    st.metric(
        "Used Leave",
        "0 Days"
    )


    st.subheader(
        "AI HR Assistant"
    )


    question = st.text_input(
        "Ask company questions"
    )


    if st.button("Ask AI"):

        st.write(
            "RAG connection will be added here"
        )



    if st.button("Logout"):

        st.session_state.employee = None

        st.rerun()
import streamlit as st
import google.generativeai as genai
import os
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from dotenv import load_dotenv

load_dotenv() 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(health_data):
    model = genai.GenerativeModel('gemini-pro')
    input_prompt = f"""
    Analyze the health data of {health_data['Name']}. You are a doctor who provides personalized health recommendations based on their age, Heart Rate, Blood Pressure, and Health Problems given by patients. Tell about them with what that person should take for diet, exercise, etc., to maintain the blood pressure and heart rate within range. What would be the symptoms based on their health problems and the health data, and suggest which kind of doctors to consult for the same.
    {{"Name": "{health_data['Name']}","Age": "{health_data['Age']}", "Blood Pressure": "{health_data['Blood Pressure']}", "Heart Rate": "{health_data['Heart Rate']}", 'Health Problem': "{health_data['Health Problems']}"}}
    """

    response = model.generate_content(input_prompt)
    return response.text if response else None


def plot_heart_rate_chart(selected_person_details):
    plt.figure(figsize=(4, 3))

    # numeric values and convert to strings
    normal_heart_rate_str = str(80)
    person_heart_rate_str = str(selected_person_details['Heart Rate'])

    # Sort values for proper y-axis scale
    values = [normal_heart_rate_str, person_heart_rate_str]
    values = [float(''.join(filter(str.isdigit, val))) for val in values]  

    # Plot bars for normal and person's heart rate
    plt.bar(x=['Normal Heart Rate', "Patient Heart Rate"],
            height=values,
            color=['g', 'black'], alpha=0.5, width=0.2)

    plt.xticks(fontsize=5)  
    plt.yticks(fontsize=5)

    plt.title(f"Heart Rate Chart for {selected_person_details['Name']}", fontsize=9)
    plt.xlabel('Metrics', fontsize=7)
    plt.ylabel('Values', fontsize=7)
    plt.legend()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()


def plot_blood_pressure_chart(selected_person_details):
    plt.figure(figsize=(4, 3))

    # numeric values and convert to strings
    low_bp_str = "90/60 mmHg"
    high_bp_str = "140/90 mmHg"
    person_bp_str = str(selected_person_details['Blood Pressure'])

    # Sort values for proper y-axis scale
    values = [low_bp_str, high_bp_str, person_bp_str]
    values = [float(''.join(filter(str.isdigit, val))) for val in values]  # Extract numeric values

    # Plot bars for low, high, and person's blood pressure
    plt.bar(x=['Low B.P', 'High B.P', "Patient B.P"],
            height=values,
            color=['r', 'g', 'black'], alpha=0.5, width=0.2)
    plt.xticks(fontsize=5)  
    plt.yticks(fontsize=5)

    plt.title(f"Blood Pressure Chart for {selected_person_details['Name']}", fontsize=10)
    plt.xlabel('Metrics', fontsize=7)
    plt.ylabel('Values', fontsize=7)
    plt.legend()
    st.pyplot()

# streamlit app
st.title("Personalized Health Assistant")
st.text("Analyze Health Data and Provide Recommendations")

# Allow users to input health data directly
input_name = st.text_input("Enter the Name of the Person")
input_age = st.text_input("Enter your Age")
input_blood_pressure = st.text_input("Enter Blood Pressure")
input_heart_rate = st.text_input("Enter Heart Rate")
input_health_problems = st.text_area("Describe your Problem")

if input_name and input_age and input_blood_pressure and input_heart_rate:
    # Display the entered health details
    st.subheader(f"Health Details for {input_name}:\n")
    st.write(f"Name: {input_name}")
    st.write(f"Age: {input_age}")
    st.write(f"Heart Rate: {input_heart_rate}")
    st.write(f"Blood Pressure: {input_blood_pressure}")

    # Display health problems if provided
    if input_health_problems:
        st.write(f"Health Problems: {input_health_problems}")

    # Plot Heart Rate Chart
    plot_heart_rate_chart({
        'Name': input_name,
        'Heart Rate': input_heart_rate
    })

    # Plot Blood Pressure Chart
    plot_blood_pressure_chart({
        'Name': input_name,
        'Blood Pressure': input_blood_pressure
    })

    submit = st.button("Get Health Recommendations")

    if submit:
        health_data = {
            "Name": input_name,
            "Age": input_age,
            "Heart Rate": input_heart_rate,
            "Blood Pressure": input_blood_pressure,
            "Health Problems": input_health_problems
        }

        response = get_gemini_response(health_data)

        st.subheader("Model Response:")
        st.write(response)

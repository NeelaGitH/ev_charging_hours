import streamlit as st
import pickle
import pandas as pd

with open("charging_hours_v2.pkl", 'rb') as file_m:  
    model = pickle.load(file_m)
            
with open("pipeline_charging_hours_v2.pkl", 'rb') as file_p:
    pipeline = pickle.load(file_p)


st.title("Charging Hours Prediction")

form_values = {
    'Vehicle Model' : None,
    'State of Charge (Start %)' : None,
    'State of Charge (End %)' : None,
    'Temperature (°C)' : None,
    'Charger Type' : None

}

with st.form(key = "Charging_Hours"):

    st.subheader("Please input your vehicle features")

    form_values['Vehicle Model'] = st.radio("Choose your Vehicle Model", ["Tesla Model 3", "Hyundai Kona", "Nissan Leaf", "BMW i3", "Chevy Bolt"])

    form_values['State of Charge (Start %)'] = st.slider("Select your starting battery %", 0.00, 100.00, 10.00)

    form_values['State of Charge (End %)'] = st.slider("Select the battery % you want to charge your vehicle upto", 0.00, 100.00, 90.00)

    form_values['Temperature (°C)'] = st.slider("Select Temperature (°C)", 0.00, 60.00, 30.00)

    form_values['Charger Type'] = st.radio("Choose your charger type", ['DC Fast Charger', 'Level 1', 'Level 2'])

    submit_button = st.form_submit_button(label = "Submit")

    if submit_button:
        if not all(form_values.values()):
            st.warning("Please fill in all the fields")
        
        elif (form_values["State of Charge (Start %)"] > form_values["State of Charge (End %)"]):
            st.warning("Starting Charge % is larger than Ending Charge %")
        else:
            data = pd.DataFrame.from_dict([form_values])

            st.write("Your input values are", data)
            
            data_prepared = pipeline.transform(data)

            prediction = model.predict(data_prepared)

            st.write("The predicted charging hours required is", round(prediction[0],2))


            













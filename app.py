import streamlit as st
import pickle as pkl
import pandas as pd

# form for input 
def form_data():
    with st.form("my_form"):
        holiday = int(st.selectbox("Holiday Flag", [0, 1]))
        temp = float(st.number_input("Temperature in Fahrenheit"))
        Fuel_Price = float(st.number_input("Fuel Price in USD"))
        CPI = st.slider("CPI (Consumer Price Index)", min_value=100, max_value=250, step=1)
        Unemployment = int(st.slider("Unemployment Rate", min_value=5, max_value=15, step=1))
        submitted = st.form_submit_button("Submit")

        if submitted:
            st.write("Holiday ", holiday,"temp ", temp, "Fuel_Price ", Fuel_Price, "CPI", CPI,
                      "Unemployment Rate ", Unemployment,"%")
            return [holiday, temp, Fuel_Price, CPI, Unemployment]


# FRONTEND
bar = st.sidebar.radio("Get Sales Forecasting", ["Home", "For Next Week"])

if bar == "Home":
    st.header('Sales Forecasting')
    st.write('Details of Data')

if bar =="For Next Week":
    st.header("Sales Forecasting For Next Week")
    option = st.selectbox("Select Optiom", ["None", "Have Input Data", "Don't Have Input Data"])

    if option == "Have Input Data":
        store = st.selectbox("Select Store", [1, 2, 3, 4, 5])
        st.info('Fill all the Input Field')

        data = form_data()

        if data:
            model_path = "Models\\Sarima\\model_"+str(store)+".pkl"
            model = ""
            with open(model_path, 'rb') as f:
                model = pkl.load(f)

           # give the data to the dataframe as much week predcition you want
            result =  model.forecast(steps=1, exog=data)

        # sales for next week 
            st.success(f"Sales expected for next week at store {store} is {result[0]:.2f}")
#            st.balloons()
#            st.dataframe(pd.DataFrame(result))


    if option == "Don't Have Input Data":
        bool = False
        with st.form('my_form2'):
            store = st.selectbox("Select Store", [1, 2, 3, 4, 5])
            weeks = int(st.number_input("Number of Weeks", min_value=1, max_value=10, step=1))
            submitted = st.form_submit_button("Submit")

            if submitted:
                bool = True
                st.write("Store ", store, "weeks ", weeks)

        if bool == False:
            st.stop()
        model_path = "Models\\Arima\\model_"+str(store)+"arima.pkl"
        model = ""
        with open(model_path, 'rb') as f:
            model = pkl.load(f)

        # give the data to the dataframe as much week predcition you want
        result =  model.forecast(steps=weeks)

        # sales for next week 
#        st.success(f"Sales expected for next week at store {store} is {result[0]:.2f}")
        temp_df = pd.DataFrame(result)
        temp_df.rename(columns={"predicted_mean": "Expected Sales"}, inplace=True)
        st.dataframe(temp_df)
#        st.balloons()

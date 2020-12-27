from flask import Flask, render_template, request
from sklearn.preprocessing import StandardScaler
import pandas as pd
import gunicorn
scaler = StandardScaler()
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('loan_pred.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')












@app.route("/predict", methods=['POST'])
def predict():

    if request.method == 'POST':
        
        Gender = request.form['Gender']
        if(Gender=='Male'):
            Gender=1
        else:
            Gender=0     
        
        Married = request.form['Married']
        if(Married=='Yes'):
            Married=1
        else:
            Married=0        

        Self_Employed = request.form['Self_Employed']
        if(Self_Employed=='Yes'):
            Self_Employed=1
        else:
            Self_Employed=0  

        Education = request.form['Education']
        if(Education=='Yes'):
            Education=1
        else:
            Education=0

        Dependents_1 = int(request.form['Dependents_1'])
        Dependents_2=0
        Dependents_3above=0       
        if(Dependents_1==0):
            Dependents_1=0
            Dependents_2=0
            Dependents_3above=0
        elif(Dependents_1==1):
            Dependents_1=1
            Dependents_2=0
            Dependents_3above=0
        elif(Dependents_1==2):
            Dependents_1=0
            Dependents_2=1
            Dependents_3above=0
        else:
            Dependents_1=0
            Dependents_2=0
            Dependents_3above=1

        ApplicantIncome = int(request.form['ApplicantIncome'])
        
        CoapplicantIncome = int(request.form['CoapplicantIncome'])
        
        LoanAmount = int(request.form['LoanAmount'])

        Loan_Amount_Term = int(request.form['Loan_Amount_Term'])

        Credit_History = request.form['Credit_History']
        if(Credit_History=='Yes'):
            Credit_History=1
        else:
            Credit_History=0        

        Property_Area_Semiurban = request.form['Property_Area_Semiurban']       
        if(Property_Area_Semiurban=="Urban"):
            Property_Area_Semiurban=0
            Property_Area_Urban=1
        elif(Property_Area_Semiurban=="Semiurban"):
            Property_Area_Semiurban=1
            Property_Area_Urban=0
        else:
            Property_Area_Semiurban=0
            Property_Area_Urban=0


        train1=pd.read_csv("apply_fit_transform.csv")
        train=scaler.fit_transform(train1.drop(["Unnamed: 0"],axis=1))


        X=pd.DataFrame({'Gender': [Gender], 'Married': [Married],'Education': [Education], 'Self_Employed': [Self_Employed],'ApplicantIncome': [ApplicantIncome], 'CoapplicantIncome': [CoapplicantIncome],'Loan_Amount_Term': [Loan_Amount_Term], 'LoanAmount': [LoanAmount],'Credit_History': [Credit_History],'Dependents_1': [Dependents_1],'Dependents_2': [Dependents_2],'Dependents_3above': [Dependents_3above],'Property_Area_Semiurban': [Property_Area_Semiurban],'Property_Area_Urban': [Property_Area_Urban]})
        test1=pd.read_csv("apply_transform.csv")
        test=pd.concat([test1.drop(["Unnamed: 0"],axis=1),X],axis=0)
        test_scaled=scaler.transform(test)
        test_scaled_df=pd.DataFrame(data=test_scaled,columns=test.columns)
        
        #output=model.predict([[Gender,Married,Education,Self_Employed,ApplicantIncome,CoapplicantIncome,LoanAmount,Loan_Amount_Term,Credit_History,Dependents_1,Dependents_2,Dependents_3above,Property_Area_Semiurban,Property_Area_Urban]]) 
        prediction = pd.DataFrame(data=model.predict(test_scaled_df),columns=["prediction"])
         
        if prediction.prediction.tail(1).item==0:
            return render_template('index.html',prediction_texts="Loan Should not be approved")
        else:
            return render_template('index.html',prediction_texts="Loan should be approved")
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

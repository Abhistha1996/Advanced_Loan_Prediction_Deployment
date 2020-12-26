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


        X=pd.DataFrame({'Gender': [Gender], 'Married': [Married],'Education': [Education], 'Self_Employed': [Self_Employed],'ApplicantIncome': [ApplicantIncome], 'CoapplicantIncome': [CoapplicantIncome],'Loan_Amount_Term': [Loan_Amount_Term], 'LoanAmount': [LoanAmount],'Credit_History': [Credit_History],'Dependents_1': [Dependents_1],'Dependents_2': [Dependents_2],'Dependents_3above': [Dependents_3above],'Property_Area_Semiurban': [Property_Area_Semiurban],'Property_Area_Urban': [Property_Area_Urban]})
        #X=X.values.reshape(-1,1)
        #X = scaler.fit_transform(X)
        #Gender=scaler.fit_transform(Gender)
        #Married=scaler.fit_transform(Married)
        #Education=scaler.fit_transform(Education)
        #Self_Employed=scaler.fit_transform(Self_Employed)
        #ApplicantIncome=scaler.fit_transform(ApplicantIncome)
        #CoapplicantIncome=scaler.fit_transform(CoapplicantIncome)
        #Loan_Amount_Term=scaler.fit_transform(Loan_Amount_Term)     
        #LoanAmount=scaler.fit_transform(LoanAmount).reshape(-1, 1)
        #Credit_History=scaler.fit_transform(Credit_History)
        #Dependents_1=scaler.fit_transform(Dependents_1)
        #Dependents_2=scaler.fit_transform(Dependents_2)        
        #Dependents_3above=scaler.fit_transform(Dependents_3above)
        #Property_Area_Semiurban=scaler.fit_transform(Property_Area_Semiurban)       
        #Property_Area_Urban=scaler.fit_transform(Property_Area_Urban)      
        
        
        #output=model.predict([[Gender,Married,Education,Self_Employed,ApplicantIncome,CoapplicantIncome,LoanAmount,Loan_Amount_Term,Credit_History,Dependents_1,Dependents_2,Dependents_3above,Property_Area_Semiurban,Property_Area_Urban]]) 
        output=model.predict(X)         
        if output==0:
            return render_template('index.html',prediction_texts="Loan Should not be approved")
        else:
            return render_template('index.html',prediction_texts="Loan should be approved")
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)


import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import os
import json
from annotated_text import annotated_text
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import plotly
import streamlit.components.v1 as components
import bar_chart_race as bcr
import base64
from datasets import load_dataset
import turtle as trt





with st.sidebar:
    selected=option_menu(
        menu_title="Course of action",
        options=["Concatenation","QC Framework","Quality Chart","Track-up"],
        icons=["arrow-left-right","columns","graph-up-arrow","code-branch"],
        menu_icon="boxes",
        default_index=0,
        styles={
            "container":{"padding": "0!important","background-color":"azure"},
            "icon": {"color": "navy", "font-size": "25px"},
            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",
            }


        }
    )



#  Concatenation--------

if selected=="Concatenation":
    st.title(f"Concatenation")
    st.write("****Merge files in fastest way****")
    
    
    df=pd.DataFrame()

    files = st.file_uploader(" ", type=["xls","xlsx","csv"], accept_multiple_files=True)
    for uploaded_file in files: 
        Tabel=pd.read_excel(uploaded_file)
        currentdf=pd.DataFrame(Tabel)
        print(currentdf)
        twoFrames = [df, currentdf]
        df=pd.concat(twoFrames)
    columnNames = []
    for colName in df.columns:
        columnNames.append(colName.strip().upper().replace("_", " "))

    


    df.columns = columnNames
    df=df.fillna('')
    
    st.info('''
    ****Note:****\n
    Can upload multiple excel files here. Every file should contains same format.\n
    ****What i do:****\n
    I will merge every files into a single file. Convert column names to uppercase and remove _ symbol. At the end return this consolidated file with CSV format.\n
    Once i done my work, U can see highlighted DOWNLOAD button. Then you can find your file on clicking DOWNLOAD button. 

    ''')

    dfshape=df.shape
    st.write(dfshape)

    convert=df.to_csv(index=False)

    st.download_button(
        label="Download",
        data=convert,
        file_name='Final_consolidation.csv',
        mime='text/csv',
    )

    





#  QC Framework---------

elif selected=="QC Framework":
    st.title("QC FRAMEWORK")
    st.write("****Concatenation and Framework in just a drag****")


        
    df=pd.DataFrame()

    page_name=["Fresh","Non Fresh","Pseudo"]
    pages=st.radio('****Process****', page_name)
    

 
    if pages=="Fresh":
        files = st.file_uploader(" ", type=["xls","xlsx","csv"], accept_multiple_files=True)
        for uploaded_file in files: 
            Tabel=pd.read_excel(uploaded_file)
            currentdf=pd.DataFrame(Tabel)
            print(currentdf)
            twoFrames = [df, currentdf]
            df=pd.concat(twoFrames,ignore_index=True, sort=False)

       
        
        st.info('''
            ****Note:****\n
            Can upload multiple excel files here. Every file should contains same format.\n
            ****What i do:****\n
            I will consolidate every files into single file. After consolidating, will find the spelling mistakes for particular columns and replace it with correct and unique spelling. At last remove the duplicate records and convert it as CSV format file with unique records.\n
            Once I done my work, U can see highlighted DOWNLOAD button. Then you can find your file on clicking DOWNLOAD button. 
            ''')
        
    
   
        columnNames = []
        for colName in df.columns:
            columnNames.append(colName.strip().upper().replace("_", " "))

        df.columns = columnNames


           
            


        replacement='''
        [
            {
                "QC STATUS":
                {
                    "wrong":["crt","cORRECT","crct","CORRECT","correct","Correct","corect","CORECT","cORECT","Corect","CRT","CRCT","Crt","Crct","cRT","cRCT"],
                    "replacewith":"CORRECT"  
                }
            },
            {
                "QC STATUS":
                {
                    "wrong":["incorrect","Incorrect","INCORRECT","iNCORRECT","incorect","INCORECT","Incorect","iNCORECT","incrt","INCRT","Incrt","iNCRT","incrct","INCRCT","Incrct","iNCRCT","icrt","ICRT","Icrt","iCRT","icrct","ICRCT","Icrct","iCRCT"],
                    "replacewith":"INCORRECT"
                }
            },
            {
                "QC STATUS":{
                    "wrong":["NOT QCED","not qced","Not qced","Not Qced","nOT QCED","NOT QC'D","not qc'd","Not qc'd","Not Qc'd","Not Qc'D","nOT QC'D","NOT QC","not qc","Not qc","nOT QC","NO QCED","no qced","No qced","No Qced","nO QCED",
        "NO QC'D","no qc'd","No qc'd","No Qc'd","No Qc'D","nO QC'D","NO QC","no qc","No qc","No Qc","nO QC","NQ","nq","Nq","nQ","N Q","n q","N q","n Q","NOTQCED","notqced","Notqced","nOTQCED","NotQced","NOTQC'D","notqc'd","Notqc'd","nOTQC'D",
        "NOTQC","notqc","Notqc","nOTQC","Not Qc'ed","Not QC'ed","Not qc'ed","NotQc","NOQCED","noqced","Noqced","nOQCED","NoQced","NOQC'D","noqc'd","Noqc'd","NoQc'd","NoQc'D","nOQC'D","noqc'D","NOQC","noqc","Noqc","nOQC","NoQc"],
                    "replacewith":"Not Qced"
                }
            },
            {
                "QC STATUS":{
                    "wrong":["nan","NAN","Nan",""," ","  "],  
                    "replacewith":"Not Qced"
                }
            },
            {
                "USER ACTION":{
                    "wrong":["UPC PSEUDO COMMIT","UPCPSEUDOCOMMIT","UPCCOMMIT","UPC COMMIT","UPC","UPCPSEUDO","UPC PSEUDO","UPC-PSEUDO COMMIT","UPC-PSEUDOCOMMIT","UPC-PSEUDO","UPC-COMMIT","UPC - PSEUDO COMMIT","UPC - PSEUDOCOMMIT","UPC - COMMIT","UPC - PSEUDO",
                    "upc pseudo commit","upcpseudocommit","upccommit","upc commit","upc","upcpseudo","upc pseudo","upc-pseudo commit","upc-pseudocommit","upc-pseudo","upc-commit","upc - pseudo commit","upc - pseudocommit","upc - commit","upc - pseudo","Upc Pseudo Commit",
                    "UPC Pseudo Commit","UPS-PSEUDO COMMIT","UPC Pseudo commit","UPCPseudoCommit","UPCPseudocommit","UPCpseudocommit","UPC pseudo commit","UPC-Pseudo Commit","UPC - Pseudo Commit","UPC-Pseudocommit","UPC Commit","UPCCommit","UPCPseudo","uPC","Upc","Upc pseudo commit","Upc Pseudo Commit","uPC Pseudo Commit",
                    "Upc-Pseudo Commit","upc-Pseudo Commit","Upc - Pseudo Commit","Upc-Psedo commit","Upc - Pseudo commit","Upc Commit","Upc-Commit","Upc - Commit","Upc - commit","Upc-pseduocommit","Upc - pseudo commit","Upc-Pseudocommit","UPC-Pseudo commit","UPC - Pseudo commit"],
                    "replacewith":"UPC PSEUDO COMMIT"
                }
            },
            {
                "USER ACTION":{
                    "wrong":["LAC ONLY COMMIT","LACONLYCOMMIT","LAC ONLY COOMIT","LACCOMMIT","LAC COMMIT","LACONLY","LAC ONLY","LAC-ONLY COMMIT","LAC - ONLY COMMIT","LAC-ONLYCOMMIT","LAC -ONLY COMMIT","LAC - ONLYCOMMIT","LAC","Lac","lac","lAC","Lac commit","Laccommit","Lac Only","LacOnly","Lac only","Laconly",
                    "lac only commit","laconlycommit","laccommit","lac commit","laconly","lac only","lac-only commit","lac - only commit","lac-onlycommit","lac -only commit","lac - onlycommit","LAC Only Commit","LAC only commit","LAC Only commit","LACOnlyCommit","LacOnlyCommit","LacOnlycommit","Lac Only Commit",
                    "Lac only commit","Laconlycommit","Laconlycommit"],
                    "replacewith":"LAC ONLY COMMIT"
                }
            }, 
            {
                "USER ACTION":{
                    "wrong":["UNCODABLE","UNCODEABLE","Uncodeable","uncodeable","UNC","UNCO","uncodable","unc","unco","Uncodable","uNCODABLE","Unc","uNC","Unco","uNCO","U","u","UNCD","uncd","Uncd","uNCD"],
                    "replacewith":"UNCODABLE"
                }
            }, 
            {
                "USER ACTION":{
                    "wrong":["CONSOLIDATED LIST","CONSOLIDATED","CONSOLIDATE LIST","CONSOLIDATE","CONSO","CONSO LIST","CONSOLIST","CONSOLIDATEDLIST","CONSOLIDATELIST",
                    "consolidated list","consolidated","CONS","consolidate list","consolidate","conso","conso list","consolist","consolidatedlist","consolidatelist","Consolidated","Consolidate","Conso","cONSOLIDATED","cONSOLIDATE","Consolidated List","Consolidate List","Conso","Conso List","Consolidatedlist","ConsolidatedList","cONSOLIDATED lIST","cONSOLIDATE lIST"],
                    "replacewith":"CONSOLIDATED LIST"
                }
            },
            {
                "USER ACTION":{
                    "wrong":["FOR CODING REVIEW","FORCODINGREVIEW","for coding review","forcodingreview","For Coding Review","For coding review","For Coding review","ForCodingReview","Forcodingreview","ForCodingreview","fOR CODING REVIEW","fOR cODING rEVIEW","fORCODINGREVIEW","fORcODINGrEVIEW"],
                    "replacewith":"FOR CODING REVIEW"
                }
            },
            {
                "USER ACTION":{
                    "wrong":["nan","NAN","Nan",""," ","  "],  
                    "replacewith":"PENDING"
                }
            },
            {
                "USER ACTION":{
                    "wrong":["NOT QCED","not qced","Not qced","Not Qced","nOT QCED","NOT QC'D","not qc'd","Not qc'd","Not Qc'd","Not Qc'D","nOT QC'D","NOT QC","not qc","Not qc","nOT QC","NO QCED","no qced","No qced","No Qced","nO QCED",
        "NO QC'D","no qc'd","No qc'd","No Qc'd","No Qc'D","nO QC'D","NO QC","no qc","No qc","No Qc","nO QC","NQ","nq","Nq","nQ","N Q","n q","N q","n Q","NOTQCED","notqced","Notqced","nOTQCED","NotQced","NOTQC'D","notqc'd","Notqc'd","nOTQC'D",
        "NOTQC","notqc","Notqc","nOTQC","NotQc","Not QC'ed","Not Qc'ed","NOQCED","noqced","Noqced","nOQCED","NoQced","NOQC'D","noqc'd","Noqc'd","NoQc'd","NoQc'D","nOQC'D","noqc'D","NOQC","noqc","Noqc","nOQC","NoQc"," ","","Not Qc'ed","Pending"],
                    "replacewith": "PENDING"
                }
            }
        ]
        '''

        h=json.loads(replacement)


        for meta in h:
            for columnName in meta.keys():
                currentMeta = meta[columnName]
                for wrongEntry in currentMeta['wrong']:
                    d = {
                        columnName: {
                            wrongEntry: currentMeta['replacewith']
                        }
                    }
                    df = df.replace(d)



        df=df.fillna({ "USER ACTION":"PENDING"})
        df=df.fillna({ "QC STATUS":"Not Qced"})
        df=df.fillna('')
        
            
        
            
        
        conso=[]
        for consod in df.columns:
            conso=df['EXTERNAL CODE'].map(str)+df['PROCESSING GROUP CODE']+df['SEQ'].map(str)
        df['CONCAT']=conso
        
        df=df.drop_duplicates('CONCAT')
        

        dfshape=df.shape
        st.write(dfshape)
        
        
        
        convert=df.to_csv(index=False)

        st.download_button(
            label="Download",
            data=convert,
            file_name='QC_final_file.csv',
            mime='text/csv',
        )
    elif pages=="Non Fresh":
        st.write('work in progress')
    elif pages=="Pseudo":
        st.write('work in progress')

  




#   Quality Chart ----------

elif selected=="Quality Chart":
    st.title("Quality Chart")
    st.write("****Makes a better understanding****")


    df=pd.DataFrame()
    isFileUploaded = False

    files = st.file_uploader(" ", type=["xls","xlsx","csv"], accept_multiple_files=True)
    for uploaded_file in files: 
        Tabel=pd.read_excel(uploaded_file)
        currentdf=pd.DataFrame(Tabel)
        print(currentdf)
        twoFrames = [df, currentdf]
        df=pd.concat(twoFrames)
        isFileUploaded = True

    columnNames = []
    for colName in df.columns:
        columnNames.append(colName.strip().upper().replace("_", " "))

    df.columns = columnNames

    page_names=["Processing Group","Associate Quality","Processing Group(RACE-BAR)"]
    page=st.radio('Navigation', page_names)
   
    


    if page=="Processing Group":
        grp=[]
        grps=[]
        for chary in df.columns:
            grp=df[['PROCESSING GROUP DESCRIPTION',"ALLOCATION DATE"]]
        df1=pd.DataFrame(grp)
        st.write(df1)
        st.info('''
        ****Note:****\n
        This feature was run with ****PROCESSING GROUP DESCRIPTION**** column. Make sure the uploaded file should contains this column name.\n
        ****What i do:****\n
        I will analys the file and reflect a ****Horizontal BAR-GRAPH**** for a better comparision and understanding.

        ''')

        
       
        if isFileUploaded==True:
            df1["summation"]=df1.groupby(["PROCESSING GROUP DESCRIPTION"])
            
            
            


            figg = px.bar(df1, 
             x='PROCESSING GROUP DESCRIPTION', 
             y='IMPACT',
             text='summation',
             hover_data={"PROCESSING GROUP DESCRIPTION":True,
                         "IMPACT":False,
                         "summation":True},
            
            )
            figg.update_traces(textposition="outside")
            st.plotly_chart(figg)
            
            

       
    elif page=="Associate Quality":
        
        grs=[]
        grass=[]
        for chars in df.columns:
            grs=df[['NAME']]
        df1=pd.DataFrame(grs)
        for chart in df.columns:
            grass=df[['QC STATUS']]
        df1=pd.DataFrame(grass)
        
        



        fig=px.bar(
            df1,
            title='QC STATUS',
            width=0,
            height=0
        )
        st.plotly_chart(fig)

        


    elif page=="Processing Group(RACE-BAR)":
        st.write('work in progress')
        


elif selected=="Track-up":
    st.title("Tracker Fill")
    st.write("****Fill the tracker in easiest way****")

    df1=pd.DataFrame()

    files = st.file_uploader(" ", type=["xlsx"], accept_multiple_files=True)
    for uploaded_file in files: 
        Tabel=pd.read_excel(uploaded_file)
        currentdf=pd.DataFrame(Tabel)
        print(currentdf)
        twoFrames = [df1, currentdf] 
        df1=pd.concat(twoFrames,ignore_index=True, sort=False)


    columnNames = []
    for colName in df1.columns:
       columnNames.append(colName.strip().upper().replace("_", " "))

    df1.columns = columnNames

    


    
     




  
        

















 
   


  









    




















      
      
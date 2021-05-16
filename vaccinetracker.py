import pandas as pd
import os
import requests
import datetime as dt
import json
import urllib3
import boto3
from botocore.exceptions import ClientError

def send_email(sender, recipient, aws_region, subject, body_text, body_html):

   SENDER = sender
   RECIPIENT = recipient
   AWS_REGION = aws_region
   SUBJECT = subject
   BODY_TEXT = body_text
   BODY_HTML = body_html   
   CHARSET = "UTF-8"
   client = boto3.client('ses',region_name=AWS_REGION)
   try:
       response = client.send_email(
           Destination={
               'ToAddresses': [
                   RECIPIENT,
               ],
           },
           Message={
               'Body': {
                   'Html': {
                       'Charset': CHARSET,
                       'Data': BODY_HTML,
                   },
                   'Text': {
                       'Charset': CHARSET,
                       'Data': BODY_TEXT,
                   },
               },
               'Subject': {
                   'Charset': CHARSET,
                   'Data': SUBJECT,
               },
           },
           Source=SENDER,
     )
   except ClientError as e:
       return(e.response['Error']['Message'])
   else:
       return("Email sent! Message ID:" + response['MessageId'] )




def lambda_handler(event, context):
    i = 0
    df = pd.DataFrame(columns=['center_id','date','name','from','to','vaccine','fee_type','available_capacity_dose2'])
    
    date = (dt.datetime.now() + dt.timedelta(hours=5,minutes=30)).strftime('%d-%m-%Y')
    distictid = 186 #Added kurukshetra, you can change awith your distict ID

    url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={distictid}&date={date}"
    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'accept':'application/json',
        'accept-Language':'en_US'
    }
    
    print(url)
    r = requests.get(url, headers=headers, verify=False)
    d = json.loads(r.text)

    for data in d['centers']:
        for session_data in data['sessions']:
            df.loc[i,'center_id'] = data.get('center_id')
            df.loc[i,'name'] = data.get('name')
            df.loc[i,'from'] = data.get('from')
            df.loc[i,'to'] = data.get('to')
            df.loc[i,'fee_type'] = data.get('fee_type')
            df.loc[i,'date'] = session_data.get('date')
            df.loc[i,'vaccine'] = session_data.get('vaccine')
            df.loc[i,'available_capacity_dose2'] = session_data.get('available_capacity_dose2')
            i+=1
    #dft = df[(df.center_id==563578)]  # To show only LNGP Hospital KKR 
    dft = df
    myHTML = dft.to_html()
    myText = dft.to_string()

    mySUBJECT = f"Vaccination centers and slots availability in District:Kurukshetra"
    myRECIPIENTS = f"amit.rai@gmail.com" 

    resultMail = send_email(
       'hello.friend@gmail.com', # This email should be verified in Amazon SES
       myRECIPIENTS,
       'ap-south-1', 
       subject=mySUBJECT,
       body_text=myText,
       body_html=myHTML
    )
    print("resultMail "+resultMail)
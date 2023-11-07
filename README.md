<h1>AWS Serverless Application</h1>
<h1>Vaccination Slots and Availability Tracker</h1>
<p>This is a simple python AWS Lambda function to call public API to check the availability of vaccine doses and slots for given district Id in India</p>
<p>It will be integrated with AWS EventBrige and Simple Email Service(SES) to execute every day morning and send email to given email id with list of all 
Covid vaccination centers with dose availability and slots. I developed this for my parent, there is a huge possibility for improvement and to use as per 
requirements</p>
<p>To make it run, you need below dependancies those can be layered in lambda</p>
<ul>
<li>Pandas</li>
<li>Requests</li>
</ul>

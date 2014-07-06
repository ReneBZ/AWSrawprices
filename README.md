AWSrawprices
============

Extract AWS EC2 and RDS prices from js files on web

This python script scans the js files listed in the 'urls-all.txt' file, 
then does some scraping, ad-hoc manipulation and produces output with standarized labels 
having extracted the OnDemand prices and Reserved Instance prices.
The labels/columns of the output file are:
'Ec2orRds', 'size', 'OsDb', 'InstanceType', 'licence', 'deploy', 'region', 'ondemand', 'yrTerm1', 'yrTerm1Hourly', 'yrTerm3', 'yrTerm3Hourly'

The js files are currently provided by (I guess) AWS without any documentation nor assurance that they 
will keep them updated. Some files differ in their structure or format, therefore some manipulation had
to be done. As of today (Jul 4th,2014) they have current pricing and this script works well.
Tomorrow... who knows =S

We use the output file to load it as a tab into a Google Sheet which is configured to do full multiple instance quotes to customers (much easier -and better- than the AWS calculator)

BTW I used this task as a challange for learning Python, so I am sure that code is not 
optimized and has many deficencies. You are welcomed to optimize it.

AWSrawprices
============

Extract AWS EC2 and RDS prices from js files on web

This python script scans the js files listend in urls-all.txt file, 
then does some ad-hoc manipulation and produces output with standarized labels 
having extracted the OnDemand prices as Reserved Instance prices.

The js files are currently provided by AWS without any documentation nor assurance that they 
will keep them updated. As of today (Jun 22nd,2014) they have current pricing and this 
script works well.
Tomorrow... who knows =S

BTW I used this task as a challange for learning Python, so I am sure that code is not 
optimized and has many deficencies. You are welcomed to optimize it.
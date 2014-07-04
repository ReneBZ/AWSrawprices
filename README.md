AWSrawprices
============

Extract AWS EC2 and RDS prices from js files on web

This python script scans the js files listed in the 'urls-all.txt' file, 
then does some ad-hoc manipulation and produces output with standarized labels 
having extracted the OnDemand prices as Reserved Instance prices.

The js files are currently provided by (I guess) AWS without any documentation nor assurance that they 
will keep them updated. Some files differ in their structure or format, therefore some manipulation had
to be done. As of today (Jul 4th,2014) they have current pricing and this script works well.
Tomorrow... who knows =S

BTW I used this task as a challange for learning Python, so I am sure that code is not 
optimized and has many deficencies. You are welcomed to optimize it.

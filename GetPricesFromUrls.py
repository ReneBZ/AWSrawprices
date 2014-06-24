#!/usr/local/bin/python3.4
# PRICES OF EC2 AND RDS
import os, json, csv, string, re, urllib.request


def sweep_aws(dictolist, leveldeep, llave, ec2ords):
    global vpos
    s_type = str(type(dictolist))

    if ('str' in s_type):
        #print("    "*leveldeep+"str", llave, ":", dictolist)
        leveldeep=0

    elif 'list'in s_type:
        for index in range(len(dictolist)):
                sweep_aws(dictolist[index], leveldeep+1, "list[%s]" % index, ec2ords)

    elif ('dict' in s_type):
        if 'regions' in dictolist.keys():
            sweep_aws(dictolist['regions'],leveldeep+1,'regions <forced>', ec2ords)
        elif 'region' in dictolist.keys():
            #clean vector
            printinstance()
            lvector[kregion]=""
            lvector[ksize]=""
            if not stf.find("multiAZ")>0:
                lvector[kdeploy]=""
            lvector[kregion] = dictolist['region']
            printvector("Region: ",dictolist['region'])
            if 'instanceTypes' in dictolist.keys():
                sweep_aws(dictolist['instanceTypes'],leveldeep+1,'instanceTypes <forced>', ec2ords)
            elif 'tiypes' in dictolist.keys():
                sweep_aws(dictolist['tiypes'],leveldeep+1,'tiypes <forced>', ec2ords)
        elif 'sizes' in dictolist.keys():
            sweep_aws(dictolist['sizes'],leveldeep+1,'sizes <forced>', ec2ords)
        elif 'size' in dictolist.keys():
            printinstance()
            lvector[ksize]=dictolist['size']
            printvector("Size: ",dictolist['size'])
            if 'valueColumns' in dictolist.keys():
                sweep_aws(dictolist['valueColumns'],leveldeep+1,'valueColumns <forced>', ec2ords)
            elif 'prices' in dictolist.keys():
                sweep_aws(dictolist['prices'],leveldeep+1,'prices <forced>', ec2ords)
        elif 'tiers' in dictolist.keys():
            printinstance()
            if 'generation' in dictolist.keys():
                #   print(dictolist['generation'])
                if dictolist['generation'].find('ingle')>0 :
                    lvector[kdeploy]=""
                else:
                    lvector[kdeploy]="Multi-AZ"
            sweep_aws(dictolist['tiers'],leveldeep+1,'tiers <forced>', ec2ords)
        elif 'name' in dictolist.keys():
            if 'yr' in dictolist['name']:
                vpos= nvector.index(dictolist['name'])
            else:
                vpos=kondemand
            printvector("Name: ",dictolist['name'])
            sweep_aws(dictolist['prices'],leveldeep+1,'prices <forced>', ec2ords)
        elif 'USD' in dictolist.keys():
            lvector[vpos]=dictolist['USD']
            printvector("USD: ",dictolist['USD'])

        else:
            for key in dictolist.keys():
                sweep_aws(dictolist[key], leveldeep+1, key, ec2ords)

def printvector(slabel, svalue) :
    a = 1
    #print(lvector[1:], slabel, svalue)

def printinstance() :
    # ignore Asia Pacific regions "ap" (I don't use those regions but if you do, remove this filter)
    # also ignore when there is no instance size or no prices
    if lvector[ksize] != "" and "ap" not in lvector[kregion] and not (lvector[kondemand]+lvector[kyrTerm1]+ \
                                        lvector[kyrTerm1Hourly]+lvector[kyrTerm1]+lvector[kyrTerm1Hourly]==""):
        for i in range(len(lvector)):
             print('"%s"' % (lvector[i]),end=', ')
        print(" ")

        lvector[kondemand]=""
        lvector[kyrTerm1]=""
        lvector[kyrTerm3]=""
        lvector[kyrTerm1Hourly]=""
        lvector[kyrTerm3Hourly]=""


def extractfromfilename(sfilename):

    #get last part of filename
    lvector[kFileName] = sfilename[max(sfilename.find("ec2"),sfilename.find("rds"))-1:]

    # find out Product (ec2 or rds)
    if sfilename.find("ec2")>0:
        lvector[kEc2orRds]="ec2"
    else:
        lvector[kEc2orRds]="rds"

    # find Reserved Instance type
    if sfilename.find("light")>0:
        lvector[kInstanceType]="light"
    elif sfilename.find("medium")>0:
        lvector[kInstanceType]="medium"
    elif sfilename.find("heavy")>0:
        lvector[kInstanceType]="heavy"
    else:
        lvector[kInstanceType]="ondemand"

    # find out Os - Db
    if sfilename.find("linux")>0:
        lvector[kOsDb]="linux"
    elif sfilename.find("rhel")>0:
        lvector[kOsDb]="rhel"
    elif sfilename.find("sles")>0:
        lvector[kOsDb]="sles"
    elif sfilename.find("mswinSQLWeb")>0:
        lvector[kOsDb]="mswinSQLWeb"
    elif sfilename.find("mswinSQL")>0:
        lvector[kOsDb]="mswinSQL"
    elif sfilename.find("mswin")>0:
        lvector[kOsDb]="mswin"
    elif sfilename.find("mysql")>0:
        lvector[kOsDb]="mysql"
        lvector[klicence]="opensource"
    elif sfilename.find("postgresql")>0:
        lvector[kOsDb]="postgresql"
        lvector[klicence]="opensource"
    elif sfilename.find("oracle")>0:
        lvector[kOsDb]="oracle"
    elif sfilename.find("sqlserver")>0:
        lvector[kOsDb]="sqlserver"
    else:
        lvector[kOsDb]="no os"

    # find out licencing kind
    if sfilename.find("byol")>0:
        lvector[klicence]="byol"
    elif sfilename.find("-ex-")>0:
        lvector[klicence]="express"
    elif sfilename.find("-web-")>0:
        lvector[klicence]="web"
    elif sfilename.find("-se-")>0:
        lvector[klicence]="standard"
    elif sfilename.find("-li-")>0:
        lvector[klicence]="included"

    # find out deployment type
    if sfilename.find("multiAZ")>0:
        lvector[kdeploy]="Multi-AZ"
    else:
        lvector[kdeploy]=""


def prepareforjson(vjsstr):        #prepare keys for json
    vjsstr = vjsstr.replace('vers:0.01','"vers":"0.01"')
    vjsstr = vjsstr.replace('config','"config"')
    vjsstr = vjsstr.replace('regions','"regioxns"')
    vjsstr = vjsstr.replace('region','"region"')
    vjsstr = vjsstr.replace('regioxns','regions')
    vjsstr = vjsstr.replace('instanceTypes','"instanceTypes"')
    vjsstr = vjsstr.replace('prices','"prices"')
    vjsstr = vjsstr.replace('name:"db.','size:"db.')
    vjsstr = vjsstr.replace('name','"name"')
    vjsstr = vjsstr.replace('"USD"','USD')
    vjsstr = vjsstr.replace('USD','"USD"')
    vjsstr = vjsstr.replace('rate','"rate"')
    vjsstr = vjsstr.replace('valueColumns','"valueColumns"')
    vjsstr = vjsstr.replace('sizes','"sizxes"')
    vjsstr = vjsstr.replace('size','"size"')
    vjsstr = vjsstr.replace('sizxes','sizes')
    vjsstr = vjsstr.replace('tiers','"tiers"')
    vjsstr = vjsstr.replace('currencies','"currencies"')
    vjsstr = vjsstr.replace('types:','"tiypes":')
    vjsstr = vjsstr.replace('type:','"type":')
    vjsstr = vjsstr.replace('ECU:','"ECU":')
    vjsstr = vjsstr.replace('vCPU:','"vCPU":')
    vjsstr = vjsstr.replace('memoryGiB:','"memoryGiB":')
    vjsstr = vjsstr.replace('storageGB:','"storageGB":')
    vjsstr = vjsstr.replace('tiers:','"tiers":')
    vjsstr = vjsstr.replace('generation:','"generation":')
    vjsstr = vjsstr.replace('yearTerm','yrTerm')
    vjsstr = vjsstr.replace('multiAZ','Multi-AZ')
    vjsstr = vjsstr.replace('us-west-2','us-wes2t')
    vjsstr = vjsstr.replace('us-west-1','us-wes1t')
    vjsstr = vjsstr.replace('us-west','us-west-1')
    vjsstr = vjsstr.replace('us-wes1t','us-west-1')
    vjsstr = vjsstr.replace('us-wes2t','us-west-2')
    vjsstr = vjsstr.replace('us-east-1','us-east')
    vjsstr = vjsstr.replace('us-east','us-east-1')

    return(vjsstr)



# MAIN PROGRAM
#get each of the urls from the file that has all the urls
global stf, nvector, lvector
nvector = ["FileName", "Ec2orRds", "size", "OsDb", "InstanceType", "licence", "deploy", "region", "ondemand", "yrTerm1", "yrTerm1Hourly", "yrTerm3", "yrTerm3Hourly"]
kFileName = 0
kEc2orRds = 1
ksize = 2
kOsDb = 3
kInstanceType = 4
klicence = 5
kdeploy = 6
kregion = 7
kondemand = 8
kyrTerm1 = 9
kyrTerm1Hourly = 10
kyrTerm3 = 11
kyrTerm3Hourly = 12
lvector = [kFileName, kEc2orRds, ksize, kOsDb, kInstanceType, klicence, kdeploy, kregion, kondemand, kyrTerm1, kyrTerm1Hourly, kyrTerm3, kyrTerm3Hourly]
print(nvector[1:])

with open('urls-all.txt')as f:
    for line in f.readlines():
        stf = str(line).strip()

        #clean vector
        lvector=["","","","","","","","","","","","",""]
        vpos=kondemand

        extractfromfilename(stf)

        #print("FILE >>> %s" % stf)
        response = urllib.request.urlopen(stf)
        sth = response.read()
        response.close()
        s_all=str(sth)

        #remove the initial text and last ) bracket
        leftbaspos=s_all.find("callback(")
        vjsstr=s_all[leftbaspos+9:-3]

        #print(vjsstr)
        vjsstr = prepareforjson(vjsstr)

        #convert json to dict
        vdict=json.loads(vjsstr)
        vx=(vdict)

        leveldeep=0
        sweep_aws(vx, leveldeep, 'vx','rds')


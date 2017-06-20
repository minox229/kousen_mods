#-*- coding: utf-8 -*-
import spidev
import time
import os
import sys
import csv
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials     

### GoogleDrive
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('ojisan-fc28dbfd2b41.json', scope)
gc = gspread.authorize(credentials)
# wks = gc.open("meronpan").sheet2
doc = gc.open("meronpan")
sheet_num=1
cell_num=1

unti =  doc.worksheets()
tinko = " ".join(str(i) for i in unti)
# ojisan = tinko.split(" ")
# while "sheet"+str(sheet_num) in nanka is True:
#for i in nanka:
#    words=i.split(" ")

#split_list = [i.split() for i in nanka]
# while words.index("sheet"+str(sheet_num)):
# while "'sheet"+str(sheet_num)+"'" in ojisan is  True:
while tinko.find('sheet'+str(sheet_num)) is not -1:
   sheet_num += 1
wks = doc.add_worksheet('sheet'+str(sheet_num), 100, 20)
wks = doc.worksheet('sheet'+str(sheet_num))
# wks = doc.worksheet("sheet4")

 
##SPI
spi = spidev.SpiDev()
spi.open(0,0)

def ReadChannel(channel):
    adc = spi.xfer2([(0x07 if (channel & 0x04) else 0x06), (channel & 0x03) << 6, 0])
    data = ((adc[1] & 0x0f) << 8 ) | adc[2]
    return data

def ConvertVolts(data,places):
    volts = (data * 3.3) / float(4095)
    volts = round(volts,places)
    return volts

def ConvertTemp(data,places):
    temp = ((data * 3.3)/float(4095)*100)
    temp = round(temp,places)
    return temp

temp_channel = 0
delay = 0.0 
label=["data[Nm]","date","time"]
today = datetime.datetime.today()
date_f = today.strftime("%Y%m%d%H%M")
f= open("/home/pi/python/dB_data/" + date_f +'.csv','w')
datedate = today.strftime("%Y/%m/%d %H:%M")
csvWriter =csv.writer(f)
csvWriter.writerow([datedate])
csvWriter.writerow(label)

## drive_header 


try:
    while True:
        temp_level = ReadChannel(temp_channel)
        today = datetime.datetime.today()
        temp_volts = ConvertVolts(temp_level,3)
        temp = ConvertTemp(temp_level,2)
        ##print “Temp : %f V “% temp_volts
        date_date=today.strftime("%Y/%m/%d")
        time_time=today.strftime("%H:%M:%S")
        print date_date
        print time_time
        print temp_volts ,"[V](3.3V)"
        Nm= (temp_volts*40+10)
        #test = 110+((temp_volts-2.5)*10)/0.25 
        test = 110 - (2.5 - temp_volts)/0.025
        test2 = 110 - (2.75 - temp_volts)/0.025
        print Nm , "[dB]"  
        print test ,"[dB]"
        print test2 ,"[dB]"
        print "_________________________________"
        
        ## drive
        wks.update_acell('A'+str(cell_num),test)
        wks.update_acell('B'+str(cell_num),date_date + time_time)
        cell_num = cell_num+1

        csvWriter.writerow([Nm]+[date_date]+[time_time])#.format(Nm).format(date_date).format(time_time)
        time.sleep(delay)

except KeyboardInterrupt:
   print "end\n"
   f.close()
   spi.close()
   sys.exit(0)    

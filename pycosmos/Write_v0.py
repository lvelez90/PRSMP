import argparse
import os
from datetime import datetime, timedelta
from pathlib import Path
from obspy import read_inventory, read_events, read
import numpy as np

parser = argparse.ArgumentParser()
 # Parse for filepaths with input to generate a v0 and where to save the output
parser.add_argument("--staxml", type=Path, help="Filepath to STATIONXML file.")
parser.add_argument("--quakeml", type=Path, help="Filepath to QuakeML file.")
parser.add_argument("--mseed", type=Path, help="Filepath to MiniSeed file.")
parser.add_argument("--out", type=Path, help="Filepath where the .v0 file will be saved.")

 # Parse for variables that can be modified by user.
parser.add_argument("--event", type=ascii, help="Assign a name to the event.")
parser.add_argument("--lsb", type=float, help="Value of the Least Significant Bit (LSB) in micro-volts.")
parser.add_argument("--damp", type=float, help="Value of the Sensor damping (fraction of critical).")                    
parser.add_argument("--sens", type=float, help="Value of the Sensor sensitivity in volts/g for accelerometer.")
args = parser.parse_args()

# Read StationXML file 
inv = read_inventory('%s' % args.staxml, format="STATIONXML")
   #inv = read_inventory('/home/lvelez/pyCosmos/ADJ1.staxml')


#Read QuakeML file
cat = read_events('%s' % args.quakeml, format="QUAKEML")
   #cat = read_events('/home/lvelez/pyCosmos/quakeml.xml')


# Read MiniSeed file
mseed = read('%s' % args.mseed) 
   #mseed = read('/home/lvelez/pyCosmos/mona.mseed' )
chn_total = 0
for i in mseed[chn_total].stats.channel:
 chn_total+=1

########################################################################

#dataless = read_inventory('/home/lvelez/pyCosmos_2022/data/GNC1.xml')
#tr = mseed[0].copy()
#d_array = tr.remove_response(inventory=dataless)

#####################################################################

class Write_v0():

 def __init__(self,chn=0):
  self.chn = chn
 
 def write_v0(chn):  
  

# Read StationXML file 
   inv = read_inventory('%s' % args.staxml, format="STATIONXML")
   #inv = read_inventory('/home/lvelez/pyCosmos/ADJ1.staxml')
   net = inv[0]
   sta = net[0]
   #chn = sta[0]

   event = cat[0]
   origin = event.origins[0]
   mag = event.magnitudes[0].mag
   msecs = origin.time.microsecond / 1000000
   secs = origin.time.second + msecs
   #event_date = origin.time
   frmt_date=origin.time.strftime('%Y%m%d%H')
   event_desc = cat[0].event_descriptions
   sta_code = "", net.code, "-", sta.code
   sta_cd = "".join(sta_code)
   chan_azim = int(sta[chn+1].azimuth)
   sta_comment = inv[0][0][1].comments[0].value

   if 'ETNA-2' in sta_comment:
     LSB = 0.298024
   elif 'OBSIDIAN-4X' in sta_comment:
     LSB = 2.38
   else:
     LSB = -999
   

# Read MiniSeed file 
   #dataless = read_inventory('/home/lvelez/Downloads/Magas_Arriba/data/CLS1_dataless.xml')
   tr = mseed[chn].copy()
   #rm_resp_mseed = tr.remove_response(inventory=dataless, output="ACC")  
   array_detrend = tr.detrend("demean")
   data = mseed[chn].data
   data_size = data.size
   i = 0
   mseed[chn].plot(outfile='plot.png')
   #array_float = [rm_resp_mseed[i] * 100000 for i in range(0,data_size)]
      
      

   data_array = np.intc(array_detrend)
   evt_chan = mseed[chn].stats.channel
   duration = mseed[chn].stats.endtime - mseed[chn].stats.starttime
   max_acc = mseed[chn].max()
   scnl_frmt = "",sta.code,".",evt_chan,".",net.code,".01"
   scnl = "".join(scnl_frmt)

   max_acc_index = -1
   for i in range(data_size):
     if mseed[chn].data[i] == max_acc:
          max_acc_index = i
          max_acc_time = max_acc_index * 0.005
          break
   


   # Time variables
   event_year = origin.time.year
   event_month_hdr = origin.time.strftime('%b')
   event_day = origin.time.day
   event_day_hdr = origin.time.strftime('%a')
   event_year = origin.time.year
   event_date = origin.time.strftime('%Y/%m/%d')
   event_hr_hdr = origin.time.strftime('%H:%M')
   origin_dt_frmt = origin.time.strftime('%Y/%m/%d %H:%M:%S')  
   pretrig_secs = 30
   postdetrig_secs = duration - pretrig_secs
   rcrd_secs = ((origin.time.hour*3600) + (origin.time.minute*60) + (origin.time.second)) - pretrig_secs
   rcrd_start_hour = str(timedelta(seconds=rcrd_secs))
   rcrd_start_date = event_date +" "+ rcrd_start_hour
   current_date = datetime.now()
   current_dt_frmt = current_date.strftime('%Y-%m-%d %H:%M:%S')

   # Network and Station Variables
   network_code = 54 # Strong Motion Network Code

   # Misc
   record_id = "",sta.code , ".",evt_chan,".",net.code,".01"
   rc_id = ''.join(record_id)
   
   


# Parameters for Text Header

   text_params = [event_desc[0].text, event_day_hdr,event_month_hdr, event_day, event_year,
    event_hr_hdr, origin.latitude, origin.longitude, origin.depth, event.magnitudes[0].mag,
    origin_dt_frmt, network_code,sta_cd, sta.site.name, sta.latitude, 
    sta.longitude, chn+1, chn_total, rcrd_start_date, chan_azim,
    int(duration), max_acc, max_acc_time, current_dt_frmt]



# Parameters of Integer Header
   int_params = [0, 1, 50, 120, 1, -999, -999, 0, -999, -999, # 1-10
    42, -999, -999, -999, -999, 1, -999, -999, 1, -999, # 11-20
   -999, -999, -999, -999, -999, -999, -999, -999, -999, 109, # 21-30
    3, -999, -999, -999, 24, 24, -999, -999, -999, origin.time.year, # 31-40     ##Trying to modify 35,36 to 0 from 24 
   -999, origin.time.month, origin.time.day, origin.time.hour, origin.time.minute, 5, 8, -999, -999, -999, # 41-50
   -999, 20, -999, chan_azim, -999, -999, -999, -999, -999, -999, # 51-60                                  
   -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, # 61-70
   -999, -999, -999, -999, 1, 0, -999, -999, -999, -999, # 71-80
   -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, # 81-90
   -999, -999, -999, -999, -999, -999, -999, -999, -999, -999] # 91-100

# Parameters of Real Header
   real_params = [sta.latitude, sta.longitude, sta.elevation, -999.0, -999.0, # 1-5
   -999.0, -999.0, -999.0, -999.0, origin.latitude, # 6-10
   origin.longitude, origin.depth/1000, -999, -999.0, mag, # 11-15
   -999.0, 20.121995, 81.129693, -999.0, -999.0, #16-20                   ## Modified 17 & 18 from default              ##
   -999.0,  LSB, -999.0, pretrig_secs, postdetrig_secs, # 21-25          ##0.298024 or 2.38                        ##
   80.0, -999.0, -999.0, -999.0, secs, # 26-30                            ## Modified 26 from default                   ##
   -999.0,-999.0, -999.0, mseed[chn].stats.delta, duration, # 31-35       ##                                            ##
   -999.0, -999.0, -999.0, -999.0, 210,    # 36-40                        ## Modified 40 from 0 to nat freq 210 Hz      ##
    0.697089, 0.050, -999.0, -999.0, -999.0, # 41-45                       ## May need to change 42s value               ##
   -999.0, 1.0, -999.0, -999.0, 0.0,       # 46-50                        ##                                            ##
   -999.0, -999.0, -999.0, -999.0, -999.0, # 51-55                        ##                                            ## 
   -999.0, -999.0, -999.0, -999.0, -999.0, # 56-60                        ##                                            ##
   -999.0, 5.0, duration, max_acc, max_acc_time, # 61-65                        ## May need 65 time at max value              ##
    0.0, -999.0, -999.0, -999.0, -999.0,   # 66-70                        ## Modified 66 from default                   ##
   -999.0, -999.0, -999.0, -999.0, -999.0, # 71-75
   -999.0, -999.0, -999.0, -999.0, -999.0, # 76-80
   -999.0, -999.0, -999.0, -999.0, -999.0, # 81-85
   -999.0, -999.0, -999.0, -999.0, -999.0, # 86-90
   -999.0, -999.0, -999.0, -999.0, -999.0, # 91-95 
   -999.0, -999.0, -999.0, -999.0, -999.0] # 95-100


# Assign a name to the v0 file using the network code, station code, and channel.
   
   if args.out != None:
    parent_dir = '%s' % args.out
   else:
    parent_dir = '/home/lvelez/pyCosmos_2022/PyCosMan_v0/out'   
    dir_name = "",parent_dir,"/",net.code,"",sta.code,"-",frmt_date
    dn = ''.join(dir_name)

   file_name = "",net.code,"",sta.code,"-",frmt_date,"-",evt_chan,".v0"
   file = ''.join(file_name)
   file_path = "",dn,"/",file

   if os.path.exists(dn) == True:
    pass
   else:
     os.mkdir(dn) 
   
   fn = ''.join(file_path)    

# Write Text Header to text file
   with open(fn, "w") as f:
    print("Raw acceleration          (Format v01.20 with 13 text lines)"
    "\nRecord of",text_params[0]," of ",text_params[1],"",text_params[2], "", text_params[3],",",text_params[4],"",text_params[5],"UTC"
    "\nHypocenter", text_params[6],"  ",text_params[7]," H=", int(text_params[8]*0.001),"km", "Ml:", text_params[9], 
    "\nOrigin:", text_params[10],"   UTC"
    "\nStatn No:",text_params[11], "         Code:",text_params[12],"",text_params[13],
    "\nCoords:", text_params[14], "", text_params[15],"Site Geology:"
    "\nRecorder: Unk            (",text_params[16], "Chns of ",text_params[17]," at Sta) Sensor: (see comment)  "
    "\nRcrd start time:",text_params[18],"UTC (Q=?) RcrdId:"
    "\nSta Chan:",text_params[19],"deg       Location:"
    "\nRaw record length =",text_params[20],"sec,   Uncor max = ",text_params[21],"   , at ", text_params[22]," sec. "
    "\nProcessed",text_params[23],"AST"
    "\nNo filtering!"
    "\nValues used when parameter of data value is unknown/unspecified:   -999, -999.000", file = f)

# Write Integer header into file.
   int_size = len(int_params)
   int_col = 10
   int_lines = int_size // int_col
   i = 0

   with open(fn, "a") as f:
    print(" 100 Integer-header values follow on  10 lines, Format = (10I8)", file = f)
    for z in range(0, int_lines):
     print(f"{int_params[i]:8}{int_params[i+1]:8}{int_params[i+2]:8}{int_params[i+3]:8}{int_params[i+4]:8}{int_params[i+5]:8}{int_params[i+6]:8}{int_params[i+7]:8}{int_params[i+8]:8}{int_params[i+9]:8}", file = f)  
     i += int_col

# Write Real header into file.
   real_size = len(real_params)
   real_col = 5
   real_lines = real_size // real_col
   j = 0

   with open(fn, "a") as f:
    print(" 100 Real-header values follow on  20 lines, Format = (5F15.6)", file = f)
    for y in range(0, real_lines):
     print(f"{real_params[j]:15.6f}{real_params[j+1]:15.6f}{real_params[j+2]:15.6f}{real_params[j+3]:15.6f}{real_params[j+4]:15.6f}", file = f)
     j += real_col
     
# Write comment lines into file.
   with open(fn, "a") as f:
     print("    2 Comment line(s) follow, each starting with a |"
     "\n| RcrdId:",rc_id,
     #"\n| Sensor:",sta[chn+1].sensor.model,"s/n:",sta[chn+1].sensor.serial_number,
     "\n|<SCNL>%s"%scnl,"     <AUTH>", current_date, file = f)    

# Write acceleration data into file. 
   
   k = 0
   j = 0
   with open (fn, "a") as f:
    print("  ", data_size, "raw accel.   pts approx  ",int(duration), "secs, units=counts (50),Format=(1I6)", file = f)
    for i in range(0,data_size):
      try:
       if j == 0 and data_array[i] > 0:     
        print(f"  {mseed[chn].data[i]:4}", end=" ", file =f)
        j += 1
       else:
        print(f"  {mseed[chn].data[i]:4}", end=" ", file =f)
        j += 1
       if j == 1:
        j = 0
        print("",file = f) 
       k += 8
      except IndexError:
       break
   with open(fn, "a") as f:  
    print('End-of-data for',evt_chan, 'acceleration', file = f)

   
    

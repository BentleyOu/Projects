Field Description

C/A,UNIT,SCP,STATION,LINENAME,DIVISION,DATE,TIME,DESC,ENTRIES,EXITS


C/A      = Control Area (A002)
UNIT     = Remote Unit for a station (R051)
SCP      = Subunit Channel Position represents an specific address for a device (02-00-00)
STATION  = Represents the station name the device is located at
LINENAME = Represents all train lines that can be boarded at this station
           Normally lines are represented by one character.  LINENAME 456NQR repersents train server for 4, 5, 6, N, Q, and R trains.
DIVISION = Represents the Line originally the station belonged to BMT, IRT, or IND   
DATE     = Represents the date (MM-DD-YY)
TIME     = Represents the time (hh:mm:ss) for a scheduled audit event
DESc     = Represent the "REGULAR" scheduled audit event (Normally occurs every 4 hours)
           1. Audits may occur more that 4 hours due to planning, or troubleshooting activities. 
           2. Additionally, there may be a "RECOVR AUD" entry: This refers to a missed audit that was recovered. 
ENTRIES  = The comulative entry register value for a device
EXIST    = The cumulative exit register value for a device



Example:
The data below shows the entry/exit register values for one turnstile at control area (A002) from 09/27/14 at 00:00 hours to 09/29/14 at 00:00 hours


C/A,UNIT,SCP,STATION,LINENAME,DIVISION,DATE,TIME,DESC,ENTRIES,EXITS
A002,R051,02-00-00,LEXINGTON AVE,456NQR,BMT,09-27-14,00:00:00,REGULAR,0004800073,0001629137,
A002,R051,02-00-00,LEXINGTON AVE,456NQR,BMT,09-27-14,04:00:00,REGULAR,0004800125,0001629149,
A002,R051,02-00-00,LEXINGTON AVE,456NQR,BMT,09-27-14,08:00:00,REGULAR,0004800146,0001629162,
A002,R051,02-00-00,LEXINGTON AVE,456NQR,BMT,09-27-14,12:00:00,REGULAR,0004800264,0001629264,
A002,R051,02-00-00,LEXINGTON AVE,456NQR,BMT,09-27-14,16:00:00,REGULAR,0004800523,0001629328,
A002,R051,02-00-00,LEXINGTON AVE,456NQR,BMT,09-27-14,20:00:00,REGULAR,0004800924,0001629371,
A002,R051,02-00-00,LEXINGTON AVE,456NQR,BMT,09-28-14,00:00:00,REGULAR,0004801104,0001629395,
A002,R051,02-00-00,LEXINGTON AVE,456NQR,BMT,09-28-14,04:00:00,REGULAR,0004801149,0001629402,
A002,R051,02-00-00,LEXINGTON AVE,456NQR,BMT,09-28-14,08:00:00,REGULAR,0004801168,0001629414,
A002,R051,02-00-00,LEXINGTON AVE,456NQR,BMT,09-28-14,12:00:00,REGULAR,0004801304,0001629463,
A002,R051,02-00-00,LEXINGTON AVE,456NQR,BMT,09-28-14,16:00:00,REGULAR,0004801463,0001629521,
A002,R051,02-00-00,LEXINGTON AVE,456NQR,BMT,09-28-14,20:00:00,REGULAR,0004801737,0001629555,
A002,R051,02-00-00,LEXINGTON AVE,456NQR,BMT,09-29-14,00:00:00,REGULAR,0004801836,0001629574,
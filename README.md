# RFID-BASED-CLOCK-IN-CLOCK-OUT-SYSTEM
RFID-BASED-CLOCK-IN-CLOCK-OUT-SYSTEM Which also stores image of the person giving attendance once his face is detected.

main.py :
create_table_connecion(): Connects to the SQL SERVER Database 
data_entry(): Performs the in and out entry of a person depending on if he is already in or not
Also stores the latitude and longitude of the place where attendance is giving
get_cam(): Uses OpenCV to start a videostream and when face is detected that frame is stored as an image in the local storage and send to SQL Server as a BLOB data.

To Retrieve BLOB Data from SQL Server to display on your Website :
Retrieve.cs





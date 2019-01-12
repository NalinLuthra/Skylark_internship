# Notes

## 5 Functions are defined
     1.) Haversine
            haversine(lon1, lat1, lon2, lat2)
            It is used to calculate distance in meters between to latitude and longitude
     2.) Images Data
            images_data(folder)
            This function returns GPS coordinates with image name in python object and takes input of folder where
            images are present
     3.) Video Output
            video(folder, image_data, distance)
            This function returns nothing but it saves csv file in a folder "answers/" with file name
            "video_(whatever is file name).csv". The CSV file contains the list of all the images within given distance
            from gps coordinates given in video.
     4.) Images Output
            def images(filename, image_data, distance)
            It works similar to video(...) function except it stores data in ("answers/Images_info_"+filename)
     5.) KML Path calculator
            def kml_path(filename,video_link)
            This function calculates the KML path from video and mark important assets given by user.

## You need to install following libraries:-
    1.) pysrt ---> pip install pysrt
    2.) simplekml ---> pip install simplekml
    3.) piexif ---> pip install piexif

You can also install all the dependencies running req.sh script in main directory

## Commands to run req.sh


sudo chmod u+x req.sh
./req.sh


## Run Python Script for given task:-
    python task.py

#### Every output will be stored in folder name "answers"

#### Extra info
    4 Images are missing EXIF(GPS) Values :- DJI_0061.JPG : DJI_0452.JPG : DJI_0377.JPG : DJI_0605.JPG

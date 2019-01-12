import piexif as pf
import os
from math import radians, cos, sin, asin, sqrt
import csv
import pysrt
import simplekml


# This function is used to calculate distance between two coordinates
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    lon1, lat1, lon2, lat2 = float(lon1), float(lat1), float(lon2), float(lat2)
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    m = 6371 * c * 1000
    return m


'''This function is used to take input of folder and load all the images' gps data in a python object'''


def images_data(folder):
    images_data = []
    for filename in os.listdir(folder):
        img = pf.load(os.path.join(folder, filename))
        #It checks if EXIF values are not empty
        if bool(img["GPS"]) is not False:
            #Lat and long are converted to decimal number to be used in haversine
            long = (img["GPS"][4][0][0] / img["GPS"][4][0][1]) + ((img["GPS"][4][1][0] / img["GPS"][4][1][1]) / 60) + (
                        (img["GPS"][4][2][0] / img["GPS"][4][2][1]) / 3600)
            lat = (img["GPS"][2][0][0] / img["GPS"][2][0][1]) + ((img["GPS"][2][1][0] / img["GPS"][2][1][1]) / 60) + (
                        (img["GPS"][2][2][0] / img["GPS"][2][2][1]) / 3600)
            data = [long, lat, filename]
            images_data.append(data)
    return images_data


"""This function is used to take input of loaded python object and distance with file name of
    the csv file which consists of all the important locations"""


def images(filename, image_data, distance):
    with open(filename) as Rcsv_file, open("answers/Images_info_"+filename,"w+") as Wcsv_file:
        #Declaring two objects to read and write in csv file
        csv_writer =csv.writer(Wcsv_file,delimiter=',')
        csv_read = csv.reader(Rcsv_file, delimiter=',')
        line_c = 0
        for row in csv_read:
            if line_c == 0:
                csv_writer.writerow(row)
                line_c = line_c + 1
                continue
            else:
                str_conv = ''
                for i in image_data:
                    #Checking this distance under range
                    if haversine(row[1], row[2], i[0], i[1]) < distance:
                        str_conv = str(i[2]) + " : " + str_conv
                row[3] = str_conv
                csv_writer.writerow(row)


'''This function is used to take video srt file and distance with image data'''


def video(folder, image_data, distance):
    for filename in os.listdir(folder):
        with open("answers/video_" + filename + ".csv", 'w+') as vid_o:
            headings = ['Starting point', 'Image_names']
            writer = csv.writer(vid_o, delimiter=',')
            writer.writerow(headings)
            vid = pysrt.open(os.path.join(folder, filename))
            for i in vid:
                v = i.text.split(',')
                video_data = []
                for p in range(2):
                    video_data.append([])
                video_data[0].append(str(i.start))
                #Blank string is declared to be written in CVS after editing
                str_conv = ''
                for j in image_data:
                    if haversine(v[0], v[1], j[0], j[1]) < distance:
                        str_conv = str(j[2]) + " : " + str_conv
                video_data[1] = str_conv
                writer.writerow(video_data)


'''This function calculates the path currently it is hard coded'''


def kml_path(filename,video_link):
    kml = simplekml.Kml()
    with open(filename) as r:
        csv_r = csv.reader(r, delimiter=',')
        line_c = 0
        for row in csv_r:
            if line_c == 0:
                line_c = 1
            else:
                #It is used to add important points in KML map
                kml.newpoint(name=row[0], coords=[(row[1], row[2])])
    #It creates a path from video data
    vid = pysrt.open(video_link)
    ls = kml.newlinestring()
    for i in vid:
        v = i.text.split(',')
        ls.coords.addcoordinates([(v[0], v[1], v[2])])

    kml.save('answers/drone_path.kml')


def main():
    a = images_data("images")
    images("assets.csv",a,50)
    video("videos", a, 35)

    #Creating KML Path
    kml_path("assets.csv","videos/DJI_0301.SRT",)


if __name__ == '__main__':
    main()
from math import floor
from math import copysign
from datetime import datetime
import numpy as np

class ShipStatus:
    cx = 0.1

    def __init__(self, lat,lng,course,speed,class_value,current_date):
        self.class_value = int(class_value)
        self.course = self.__discretize_course(course)
        self.speed = self.__discretize_speed(speed)
        self.row = self.__discretize_row(lat)
        self.column = self.__discretize_row(lng)
        self.hour_sin,self.hour_cos,self.day_sin,self.day_cos = self.__discretize_date(current_date)

    def __discretize_speed(self,speed):
        max_speed = 3
        speed = float(speed)
        # speed class
        sc = 0 # slow - speed between 0.5 and 3
        if speed > 3 and speed <= 14:
            sc = 1 # medium
        elif speed > 14 and speed <= 23:
            sc = 2 # high
        elif speed > 23 and speed <= 60:
            sc = 3 # very high
        elif speed > 60:
            sc = 4 # exception
        return sc/max_speed 

    def __discretize_course(self,course):
    # course class
        course = float(course)
        max_course = 7
        cc = 0 # nord 337.5 - 22.5
        if course > 22.5 and course <= 67.5:
            cc = 1
        elif course > 67.5 and course <= 112.5:
            cc = 2
        elif course > 112.5 and course <= 157.5:
            cc = 3
        elif course > 157.5 and course <= 202.5:
            cc = 4
        elif course > 202.5 and course <= 247.5:
            cc = 5
        elif course > 247.5 and course <= 292.5:
            cc = 6
        elif course > 292.5 and course <= 337.5:
            cc = 7
        return cc/max_course

    def __get_position(self,x,ctype):
        if self.cx > 0:
            if ctype == "lng":
                xg = floor(copysign((abs(x)%180),x)/self.cx)
                if xg == -0:
                    xg = 0 
            else:
                xg = floor(x/self.cx)
        else:
            xg = -1
        return xg

    def __discretize_row(self,lat):
        lat = float(lat)
        max_row = 377
        row = self.__get_position(lat,'lat')
        return row/max_row

    def __discretize_column(self,lng):
        lng = float(lng)
        max_column = 160
        column = self.__get_position(lng,'lng')
        return column/max_column

    def __discretize_date(self,current_date):
        cdate = datetime.strptime(current_date, '%Y-%m-%d %H:%M:%S')

        hour_sin = np.sin(2 * np.pi * cdate.hour/24.0)
        hour_cos = np.cos(2 * np.pi * cdate.hour/24.0)
        day_sin = np.sin(2 * np.pi * cdate.timetuple().tm_yday/365.0)
        day_cos = np.cos(2 * np.pi * cdate.timetuple().tm_yday/365.0)

        return hour_sin,hour_cos,day_sin,day_cos

    def get_status(self):
        return [self.class_value, self.course,self.speed,self.row,self.column,self.hour_sin,self.hour_cos,self.day_sin,self.day_cos]

    def get_cx(self):
        return self.cx
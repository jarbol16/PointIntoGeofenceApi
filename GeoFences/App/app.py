import os
import sys
import json
import re
import core.repository as rep
from connection import server
from flask import Flask, request
from flask_restful import Resource, Api
import matplotlib.path as mpltPath
from urllib.parse import urlparse
#from flask.ext.jsonpify import json.json
from json import dumps
app = Flask(__name__)
api = Api(app)


class GeoFence(Resource):

    @staticmethod
    def get_geofences():
        file = open("setting.json", "r")
        data = json.load(file)
        db = data["DB"]
        __server = server.Server(db["id"], db["db_name"], db["server"], db["port"], db["user"], db["pass"], 8459)
        res = rep.get_geofences(__server)

        return res

    def get(self):
        res = self.get_geofences()
        return { 'geofences':[ x['name'] for x in res['geofences']]}

    @staticmethod
    def polygon_area(vertices):
        n = len(vertices)  # of corners
        a = 0.0
        for i in range(n):
            j = (i + 1) % n
            a += abs(vertices[i][0] * vertices[j][1] - vertices[j][0] * vertices[i][1])
        area = a / 2.0
        return area

class Point(Resource):
    def __init__(self):
        self.POLYGON = []

    def get(self,list_point):
        geos = GeoFence.get_geofences()
        for x in geos["geofences"]:
            self.get_polygon(str(x["geometry"]),x["name"])
        f = self.search_geo(eval(list_point))
        return f

    def get_polygon(self,polygon,name):
        _POLYGON = []
        print(polygon)
        try:
            regex = r"(?P<longitud>[|-][0-9.]*) (?P<latitud>[0-9.]*)"
            matches = re.finditer(regex, polygon)
            URL = "https://www.keene.edu/campus/maps/tool/?coordinates="
            for match in matches:
                _POLYGON.append([float(match["longitud"]),float(match["latitud"])])
                URL += "{0}%2C{1}%0A".format(match["longitud"],match["latitud"])
            o = urlparse(URL)
            self.POLYGON.append({"polygon":_POLYGON,"name":name,"URL":o.geturl(),"P":polygon})
        except:
            pass
        return _POLYGON

    def search_geo(self,points):
        FILTER = []
        for geo in self.POLYGON:
            try:
                path = mpltPath.Path(geo["polygon"])
                inside2 = path.contains_points(points)
                #print(geo["name"],geo["polygon"],inside2)
                total = len([x for x in inside2 if x==True])
                prob = ((total*100)/len(points))
                if prob > 50:
                    if len(geo["name"]) > 0:
                        if len([x for x in FILTER if x["GeoFence"] == geo["name"]]) == 0:
                            area = GeoFence.polygon_area(geo["polygon"])
                            FILTER.append({"GeoFence":geo["name"],"Probability":"{0}%".format(prob),"AREA":area,"URL":geo["URL"],"P":geo["P"]})
            except:
                pass
        return FILTER

api.add_resource(GeoFence, '/geofences')
api.add_resource(Point,'/points/<string:list_point>')

if __name__ == "__main__":
    app.run(port='5004')





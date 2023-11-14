from flask import Flask, render_template, request, Response, redirect
from geopy.geocoders import Nominatim
import folium
import urllib.request
import os, json
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from opencage.geocoder import OpenCageGeocode

key = 'd4cddfbe4d9348a2a5d92dcc30966e0e'


app = Flask(__name__)

path = os.getcwd() + "/output/"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/geo')
def geo():
    return render_template("geo.html")

@app.route('/ip')
def ip():
    return render_template("ip.html")

@app.route('/id')
def identity():
    return render_template("id.html")

@app.route('/envia',methods=['GET','POST'])
def geo_html():
	if request.method == 'POST':
		url=request.form['url']
		geolocator=Nominatim(user_agent="GetLoc")
		location=geolocator.geocode(url)
		print(location.address)

		print((location.latitude,location.longitude))
		m=folium.Map(Location=[location.latitude, location.longitude])
		m.save(path+'../output/location.html')
		with open(path+ '../output/location.html',"r") as f:
			content=f.read()
			return Response(content,mimetype='text/html')
		
@app.route('/envia2',methods=['GET','POST'])
def ip_html():
	if request.method == 'POST':
		ip=request.form['url']
		url=urllib.request.urlopen("http://geolocation-db.com/jsonp/"+ip)
		data=url.read().decode()
		data=data.split("(")[1].strip(")")
		parsed=json.loads(data)
		parsed_2=json.dumps(parsed,indent=4,sort_keys=True)
		print(parsed_2)
		return render_template('out.html',temp=parsed_2)

@app.route('/envia3',methods=['GET','POST'])
def id_html():
	if request.method == 'POST':
		mobile=request.form['url']
		mobile=phonenumbers.parse(mobile)
		geocoder2=OpenCageGeocode(key)
		query=str(mobile)
		result=geocoder2.geocode(query)
		a=timezone.time_zones_for_number(mobile)
		b=carrier.name_for_number(mobile,"en")
		c=geocoder.description_for_number(mobile,"en")
		d=phonenumbers.is_valid_number(mobile)
		e=phonenumbers.is_possible_number(mobile)
		print(result)
		print(a)
		print(b)
		print(c)
		print("Numero de telefono validado: ",d)
		print("Comprobar posibilidad de numero: ",e)
		result_1="Ciudad: "+f"{a}"+ ","+ "Operador: "+f"{b}" + "," +"Pais: "+ f"{c}"+","+"Geolocalization: "+f"{result}"+","+"Numero de telefono validado: "+f"{d}"+ "," +"Revisando posibilidad de numero: "+f"{e}"
		return render_template('out_2.html',temp=result_1)


if __name__ == '__main__':
		app.run(host='localhost')	
from flask import Flask, render_template, request, Response, redirect,jsonify
from geopy.geocoders import Nominatim
import folium
import urllib.request
import os, json
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from opencage.geocoder import OpenCageGeocode
from index import crear_app


from bd import creartabla , insertar,seleccionar,eliminarviejo
key = '900995c5d7064ae1a9c47af99bce0da1'

data = []
app = crear_app()
#app.register_blueprint(bp)

path = os.getcwd() #+ "/output/"

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
		print(path)
		print((location.latitude,location.longitude))
		data = [(location.address,location.latitude,location.longitude)]
		insertar(data)
		m=folium.Map(Location=[location.latitude, location.longitude], zoom_start=15)
		folium.Marker([location.latitude, location.longitude], popup=location.address).add_to(m)

		m.save(path+'\output\location.html')
		with open(path+ '\output\location.html',"r") as f:
			content=f.read()
			return Response(content,mimetype='text/html')
		
def apdf():
	data=seleccionar()
	return data
		
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


#   METODO MAIN
if __name__ == '__main__':
	#creartabla()
	eliminarviejo()
	app.run(host='localhost')
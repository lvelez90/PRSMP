class EarthquakesController < ApplicationController
require 'httparty'

start_date = (Date.today - 10.years).strftime('%Y-%m-%d')
end_date = Date.today.strftime('%Y-%m-%d')

url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=#{start_date}&endtime=#{end_date}&minmagnitude=4&latitude=18.2208&longitude=-66.5901&maxradiuskm=500"

response = HTTParty.get(url)

earthquakes = response['features'].map do |feature|
  {
    date: Time.at(feature['properties']['time'] / 1000).strftime('%Y-%m-%d %H:%M:%S %Z'),
    location: feature['properties']['place'],
    latitude: feature['geometry']['coordinates'][1],
    longitude: feature['geometry']['coordinates'][0],
    magnitude: feature['properties']['mag']
  }
end


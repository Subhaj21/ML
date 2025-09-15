# pip install requests rapidfuzz
import requests          #for using OSM machine to understand locationn and from  jason hierarchy
from rapidfuzz import process    #for missppelled locations..it will match the closest related 
                                 #words and detect the correct word for the location
import re    #for regex like "Block AG", "Sector I"
# A small list of major known place names used by the fuzzy matcher:

known_locations = ["Kolkata", "Salt Lake", "Howrah", "Delhi", "Mumbai", "Chennai", "Bangalore"]  #correct sppelling of places
cause_keywords = {
    "garbage": ["garbage", "trash", "waste", "dustbin"],
    "water": ["water", "leakage", "drain", "sewage"],
    "traffic": ["traffic", "congestion", "jam", "signal"],
    "electricity": ["electricity", "power", "light", "transformer"],
}  #Example: if a post contains “trash”, it is classified as "garbage".

def get_location_hierarchy(querry):
    url="https://nominatim.openstreetmap.org/search"
    parameter={"q":querry,"format":"json","addressdetails":1}
    headers={"User-Agent":"CivicResponse/1.0"}

    try:
        response=requests.get(url,parameter=parameter,headers=headers,timeout=10)
        data=response.json()
    except Exception as e:

        print("OSM api error",e)
        return None
    
    if not data:
        return None
    
    address=data[0].get({"Address",{}})
#    this will give the [0 index] address part of the osm data and return empty {} if no address found
    
    location_hierarchy={}
    for field in ["state","city","town","village","suburb"]:
        if address.get(field):
            location_hierarchy[field]= address[field] 
    return location_hierarchy if location_hierarchy else None
    # this will make a list of the location with the fields and values like the state,city,town,etc

def extract_sublocations(post,location_hierarchy):
    cleaned=post.lower()
    for loc in location_hierarchy.values():
        cleaned=cleaned.replace(loc.lower(),"")

    

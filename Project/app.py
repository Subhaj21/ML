# this code is here to make the sentences into keywords
import spacy
from fastapi import FastAPI, Query
nlp = spacy.load("en_core_web_sm")

def sentence_classification(sentence):
    doc=nlp(sentence)
    keywords=[]
    for token in doc:
        if token.pos_ in ["NOUN","PROPN","ADJ"] and not token.is_stop:
            keywords.append(token.lemma_.lower())
    return list(set(keywords))

# sentence="near the school road there is a broken pipe"
# print(sentence_classification(sentence))
# key=sentence_classification(sentence)

# this code is here to look at the keywords and determine the departments ....datas are already given...it just checks which dept 
departments = {
    "Public Works": [
        # Basic road infrastructure
        "road", "street", "lane", "avenue", "sidewalk", "footpath", "crosswalk",
        "speed breaker", "flyover", "bridge", "underpass", "overpass", "divider",
        "traffic circle", "pothole", "crack", "bumpy road", "dusty road", "uneven road",
        # Maintenance & construction
        "construction debris", "road widening", "road repair", "road erosion",
        "road blockage", "road accident spot", "repair pending", "waterlogging on road","road", "street", "lane", "avenue", "sidewalk", "footpath", "crosswalk",
        "speed breaker", "flyover", "bridge", "underpass", "overpass", "divider",
        "traffic circle", "pothole", "crack", "bumpy road", "dusty road", "uneven road",
        "construction debris", "road widening", "road repair", "road erosion",
        "road blockage", "road accident spot", "repair pending", "waterlogging on road"
    ],

    "Street Lighting & Electrical": [
        # Basic electrical items
        "streetlight", "lamp post", "bulb", "tube light", "light", "switch", "socket", 
        "fuse", "electric pole", "wiring", "cable", "transformer", "meter",
        # Electrical issues
        "power cut", "load shedding", "blackout", "brownout", "low voltage",
        "short circuit", "spark", "electric shock", "overload", "burnt wire",
        "loose wire", "underground cable damage", "overhead wire", "flickering light",
        "generator", "inverter", "electrical fire","streetlight", "lamp post", "bulb", "tube light", "light", "switch", "socket", 
        "fuse", "electric pole", "wiring", "cable", "transformer", "meter",
        "power cut", "load shedding", "blackout", "brownout", "low voltage",
        "short circuit", "spark", "electric shock", "overload", "burnt wire",
        "loose wire", "underground cable damage", "overhead wire", "flickering light",
        "generator", "inverter", "electrical fire"
    ],

    "Parks & Recreation": [
        # Facilities
        "playground", "swings", "slides", "see-saw", "sandbox", "benches", "paths",
        "gardens", "lawns", "fountain", "sports ground", "basketball court",
        "public park", "community park", "recreational facility",
        # Issues
        "broken equipment", "rusty slides", "damaged benches", "litter in park",
        "fallen tree", "damaged fence", "overgrown grass", "water leakage in fountain",
        "slippery path", "uneven lawn", "playground unsafe","playground", "swings", "slides", "see-saw", "sandbox", "benches", "paths",
        "gardens", "lawns", "fountain", "sports ground", "basketball court",
        "public park", "community park", "recreational facility",
        "broken equipment", "rusty slides", "damaged benches", "litter in park",
        "fallen tree", "damaged fence", "overgrown grass", "water leakage in fountain",
        "slippery path", "uneven lawn", "playground unsafe"
    ],

    "Water Supply": [
        # Basic water infrastructure
        "water", "tap", "pipeline", "pipe", "tank", "well", "reservoir", "filter",
        "hand pump", "borewell", "overhead tank", "drinking water",
        # Issues
        "leak", "burst pipe", "broken pipeline", "supply cut", "irregular supply",
        "dirty water", "rusty water", "contamination", "low pressure", "no pressure",
        "shortage", "scarcity", "flooding", "tank overflow", "chlorination",
        "filtration", "treatment plant", "booster pump failure", "groundwater depletion", "water", "tap", "pipeline", "pipe", "tank", "well", "reservoir", "filter",
        "hand pump", "borewell", "overhead tank", "drinking water",
        "leak", "burst pipe", "broken pipeline", "supply cut", "irregular supply",
        "dirty water", "rusty water", "contamination", "low pressure", "no pressure",
        "shortage", "scarcity", "flooding", "tank overflow", "chlorination",
        "filtration", "treatment plant", "booster pump failure", "groundwater depletion"
    ],

    "Sewage & Drainage": [
        # Basic infrastructure
        "sewage", "drainage", "drain", "manhole", "storm drain", "blocked drain", 
        "open drain", "overflowing sewage", "wastewater", "clogged drain",
        # Problems
        "flooding", "water stagnation", "foul smell", "mosquito breeding",
        "rodents", "contamination", "health hazard", "pipe leakage", "backflow",
        "irregular cleaning", "drain repair pending", "sewage leak","sewage", "drainage", "drain", "manhole", "storm drain", "blocked drain", 
        "open drain", "overflowing sewage", "wastewater", "clogged drain",
        "flooding", "water stagnation", "foul smell", "mosquito breeding",
        "rodents", "contamination", "health hazard", "pipe leakage", "backflow",
        "irregular cleaning", "drain repair pending", "sewage leak"
    ],

    "Traffic & Transportation": [
        # Traffic infrastructure
        "traffic signal", "junction", "pedestrian crossing", "zebra crossing", 
        "road signage", "road markings", "bus stop", "parking space", "traffic sign",
        "speed limit sign", "roundabout", "road lane", "traffic light",
        # Issues
        "signal not working", "missing signage", "damaged bus stop", "illegal parking",
        "road congestion", "traffic jam", "unsafe crossing", "blocked lane",
        "pedestrian hazard", "accident-prone area","traffic signal", "junction", "pedestrian crossing", "zebra crossing", 
        "road signage", "road markings", "bus stop", "parking space", "traffic sign",
        "speed limit sign", "roundabout", "road lane", "traffic light",
        "signal not working", "missing signage", "damaged bus stop", "illegal parking",
        "road congestion", "traffic jam", "unsafe crossing", "blocked lane",
        "pedestrian hazard", "accident-prone area"
    ],

    "Building & Housing": [
        # Structures
        "building", "apartment", "house", "public building", "residential complex",
        "wall", "roof", "floor", "balcony", "ceiling", "foundation", "structure",
        # Issues
        "cracks", "structural damage", "unsafe building", "unauthorized construction",
        "housing code violation", "damaged roof", "leaking ceiling", "collapse risk",
        "fire hazard", "broken doors/windows", "weak foundation","building", "apartment", "house", "public building", "residential complex",
        "wall", "roof", "floor", "balcony", "ceiling", "foundation", "structure",
        "cracks", "structural damage", "unsafe building", "unauthorized construction",
        "housing code violation", "damaged roof", "leaking ceiling", "collapse risk",
        "fire hazard", "broken doors/windows", "weak foundation"
    ],

    "Health & Safety": [
        # Hygiene & public safety
        "garbage", "trash", "waste", "unclean area", "open waste", "stagnant water",
        "mosquitoes", "flies", "rodents", "pest infestation", "spill", "contamination",
        # Issues
        "disease risk", "hygiene problem", "emergency hazard", "electrical hazard",
        "open manhole", "slippery surface", "foul smell", "pollution", 
        "fire risk", "blocked emergency exit","garbage", "trash", "waste", "unclean area", "open waste", "stagnant water",
        "mosquitoes", "flies", "rodents", "pest infestation", "spill", "contamination",
        "disease risk", "hygiene problem", "emergency hazard", "electrical hazard",
        "open manhole", "slippery surface", "foul smell", "pollution", 
        "fire risk", "blocked emergency exit"
    ],

    "Environmental Department": [
        # Environment
        "tree", "green zone", "forest", "park", "water body", "lake", "river", "pond",
        "protected area", "wildlife habitat", "natural habitat", "air", "noise", "soil",
        # Issues
        "illegal tree-cutting", "pollution", "water contamination", "air pollution",
        "noise complaint", "green space encroachment", "habitat destruction",
        "industrial waste", "deforestation", "illegal dumping", "chemical leakage",
        "tree", "green zone", "forest", "park", "water body", "lake", "river", "pond",
        "protected area", "wildlife habitat", "natural habitat", "air", "noise", "soil",
        "illegal tree-cutting", "pollution", "water contamination", "air pollution",
        "noise complaint", "green space encroachment", "habitat destruction",
        "industrial waste", "deforestation", "illegal dumping", "chemical leakage"
    ]
}



def classify_dept(key):
    dept_score={dept:0 for dept in departments}
    for dept, dept_keywords in departments.items():
        for word in key:
            if word in dept_keywords:
                dept_score[dept]+=1
    depp=max(dept_score,key=dept_score.get)
    if depp==0:
        return "No matching department found"
    else:
        return depp
        
# print(classify_dept(key))

# this code will classify with the statements and departments choosen earlier and apply the logic to  determine department with the new sentences
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Training data
texts = [
    # Public Works
#    / "There are large potholes on the main road that need urgent repair",
    "The sidewalk near the market is broken and unsafe for pedestrians",
    "Drainage system near my house is damaged and water is accumulating",
    "Road construction debris has not been cleared for weeks",
    "The street near my home has cracks and uneven asphalt",
    "Bumpy road near the school is causing accidents",
    "Flyover surface has cracks and needs maintenance",
    "Crosswalk is uneven and risky for pedestrians",
    "Speed breaker near the hospital is broken",
    "Bridge near the park has minor damages that need fixing",
    "Uneven road near residential area is dangerous",
    # "Construction debris blocking the street is unsafe",
    "The main road has large cracks causing vehicle damage",
    "Road repair near the market is delayed",
    "Potholes are forming rapidly on the highway",
    "Sidewalk edges are broken and hazardous",
    "The street near the bus stop is very dusty",
    "Traffic circle has uneven asphalt causing accidents",
    "Flyover railing is damaged and needs fixing",
    "Bridge surface is cracked and slippery",
    "Crosswalk paint is faded, risky for pedestrians",
    "Bumpy road near the hospital makes commuting unsafe",
    "Speed breaker missing near school zone",
    "Road near the park is eroded and dangerous",
    "Street near river has potholes forming rapidly",
    "Cracks on the bridge endanger vehicles",
    "Construction debris blocking footpath near my house",
    "Uneven road surface causing minor accidents",
    "Sidewalk near shopping complex is broken",
    "Road repair work has not started yet",
    "Main street has deep potholes",
    "Bumpy road near bus stop causing delays",
    "Flyover expansion is incomplete and hazardous",
    "Crosswalk near park is unsafe for children",
    "Speed breaker damaged and causing accidents",
    "Bridge near market is cracked and slippery",
    "Road near hospital has debris and potholes",
    "Sidewalk near school is uneven and risky",
    "Street near park is dusty and full of cracks",
    "Potholes on highway causing vehicle damage",
    "Road near residential area is sinking",
    "Traffic circle repair is pending for weeks",
    "Bumpy road near railway station causing accidents",
    "Bridge railing near school zone is damaged",
    "Crosswalk near market is broken",
    "Uneven asphalt road near park",
    "Road near main bus stop has cracks",
    "Sidewalk near hospital is broken",
    "Street near lake is uneven and dusty",
    "Flyover near school is unsafe",
    "Potholes near junction causing traffic issues",

    # Street Lighting & Electrical
    "Streetlight on 5th Avenue is not working at night",
    "Electric wires are hanging dangerously near the park",
    "Transformer near the market caught fire last night",
    "The streetlight has been flickering for days", 
    "Streetlight on 5th Avenue is not working at night",
    "Electric wires are hanging dangerously near the park",
    "Power cut has left the entire colony in darkness",
    "Low voltage is affecting appliances in the neighborhood",
    "Fuse near the main road is blown and needs replacement",
    "Short circuit in the electric pole is dangerous",
    "Lamp post near the school is completely non-functional",
    "Blackout occurred due to faulty wiring near the hospital",
    "Overhead wiring is loose and risky for pedestrians",
    "Electric pole near market is leaning dangerously",
    "Streetlight bulb has blown out and needs replacement",
    "Power outage affecting entire locality",
    "Transformer leakage caused small sparks near street",
    "Low voltage causing appliances to malfunction",
    "Flickering streetlight near school is unsafe",
    "Damaged fuse causing blackout in area",
    "Short circuit reported near residential complex",
    "Spark from electrical wire near park is dangerous",
    "Streetlight cable is loose and needs urgent repair",
    "Electric pole wiring is exposed near hospital",
    "Lamp post near junction is non-functional",
    "Power cut has been occurring for several hours",
    "Blackout in the neighborhood after transformer failure",
    "Streetlight near playground flickering intermittently",
    "Low voltage affecting commercial buildings",
    "Short circuit causing minor sparks near market",
    "Fuse box near streetlight is damaged",
    "Electric pole near highway is tilted",
    "Transformer near school sparking occasionally",
    "Streetlight cable damaged due to heavy winds",
    "Electric pole wires hanging dangerously",
    "Lamp post near residential area broken",
    "Power outage in main street",
    "Blackout due to damaged overhead wiring",
    "Streetlight near hospital not working",
    "Low voltage problem near market",
    "Short circuit in lamp post wiring",
    "Fuse damaged near playground",
    "Electricity supply irregular near junction",
    "Transformer malfunction near streetlight",
    "Exposed wires near bus stop",
    "Power cut affecting nearby houses",
    "Flickering lights near main road",
    "Damaged electric pole near park",
    "Streetlight not illuminating road",
    "Overhead wiring problem near school",
    "Short circuit causing blackout",

    # Parks & Recreation
    "Playground swings are broken in the central park",
    "Garden benches are damaged and need replacement",
    "Public park paths are full of litter and unsafe",
    "The slides in the park are rusty and dangerous",
    "The community park fountain is leaking and unusable",
    "Sports ground has uneven surface and potholes",
    "Recreational facility equipment is damaged",
    "Paths in the community park are slippery",
    "The community park fountain is leaking and unusable",
    "Overgrown grass is making the playground unusable",
    "Benches in the garden are broken and unstable",
    "Swings near playground are rusted",
    "Slides near community park unsafe",
    "Fountain near garden leaking water",
    "Paths in sports ground are uneven",
    "Playground equipment broken",
    "Recreational area benches damaged",
    "Overgrown grass near park",
    "Garden benches unstable",
    "Community park fountain leaking",
    "Public park swings unsafe",
    "Slides in playground need replacement",
    "Sports ground paths cracked",
    "Playground surface uneven",
    "Benches in community park broken",
    "Fountain in recreational facility damaged",
    "Paths near park slippery",
    "Playground equipment unsafe for children",
    "Slides near school park broken",
    "Garden paths overgrown",
    "Community park swings damaged",
    "Benches near playground cracked",
    "Fountain near playground leaking",
    "Public park slides rusted",
    "Recreational area paths uneven",
    "Sports ground benches broken",
    "Playground swings missing",
    "Slides in public park broken",
    "Garden fountain overflowing",
    "Paths near sports ground damaged",
    "Playground equipment rusted",
    "Benches near fountain damaged",
    "Community park slides unsafe",
    "Playground surface damaged",
    "Slides near community park rusty",
    "Fountain near playground broken",
    "Paths near garden unsafe",
    "Playground swings unsafe",
    "Slides near school unsafe",
    "Benches near sports ground broken",
    "Community park fountain leaking"
]

labels = [
    # Public Works
    *["Public Works"]*50,
    # Street Lighting & Electrical
    *["Street Lighting & Electrical"]*50,
    # Parks & Recreation
    *["Parks & Recreation"]*50,
]

# Water Supply
texts += [
    "Tap water has been coming out dirty and unsafe to drink",
    "There is a leak in the main water pipeline",
    "Water supply has been irregular for several days",
    "The overhead tank near my area is empty",
    "Burst pipe has flooded the streets in our neighborhood",
    "Low water pressure is affecting homes near the market",
    "Reservoir water level is critically low",
    "Pipeline burst near the school is causing waterlogging",
    "Dirty water is being supplied through the overhead tank",
    "Contamination in drinking water has been reported",
    "Tap water supply is inconsistent across the colony",
    "Leak in the main pipeline causing water shortage",
    "Overhead tank has not been cleaned for months",
    "Water mains are broken and need urgent repair",
    "Bursted pipe near hospital flooding the road",
    "Reservoir contamination affecting local supply",
    "Low pressure causing tap water flow issues",
    "Pipeline leakage near playground causing waterlogging",
    "Tap water is rusty and unsafe to consume",
    "Burst pipe near market causing street flooding",
    "Water contamination reported near residential area",
    "Irregular water supply disrupting daily life",
    "Overhead tank empty and water supply halted",
    "Tap water coming out muddy and brown",
    "Leakage in pipeline near school causing puddles",
    "Burst water main affecting multiple households",
    "Dirty water supplied through overhead tank",
    "Water supply irregular for the past week",
    "Pipe near bus stop is leaking continuously",
    "Water contamination near community park reported",
    "Main pipeline has minor cracks leaking water",
    "Overhead tank overflowing causing street flooding",
    "Tap water pressure too low in entire area",
    "Burst pipe near junction causing chaos",
    "Water supply halted due to pipe damage",
    "Dirty water reported in overhead tank",
    "Pipeline leak flooding residential street",
    "Tap water irregular and discolored",
    "Reservoir overflow affecting local roads",
    "Leak in pipeline causing wet streets",
    "Water tank empty and residents complaining",
    "Pipe burst near hospital causing flooding",
    "Contamination found in tap water supply",
    "Water pressure extremely low in neighborhood",
    "Tap water has foul smell",
    "Pipeline leakage near park causing muddy water",
    "Burst pipe flooding nearby street",
    "Overhead tank leaking and unsafe",
     "Burst pipe has flooded the streets in our neighborhood",
    "Low water pressure is affecting homes near the market",
    "Water supply disrupted for several days",
]

labels += ["Water Supply"] * 50

# Sewage & Drainage
texts += [
    "Sewage is overflowing onto the street causing foul smell",
    "Clogged drain has caused flooding near the market",
    "Manhole cover is missing and is a safety hazard",
    "Drainage system is blocked and water is stagnant",
    "Overflowing sewage is attracting mosquitoes",
    "Storm drain is full and water is stagnating",
    "Foul smell from sewage is affecting nearby homes",
    "Pipe leakage in the drain is causing flooding",
    "Unclean drains are causing health issues",
    "Backflow from blocked drains is spreading contamination",
    "Clogged sewage pipe near school causing overflow",
    "Drainage near park blocked due to debris",
    "Manhole near hospital open and dangerous",
    "Overflowing drain near residential area",
    "Sewage water leaking into streets",
    "Blocked drain causing stagnant water in neighborhood",
    "Overflowing sewage attracting pests",
    "Pipe in drainage system broken and leaking",
    "Foul smell from sewer affecting residents",
    "Clogged storm drain causing street flooding",
    "Open manhole near market creating hazard",
    "Drain near bus stop overflowing",
    "Sewage backflow near community park",
    "Blocked drainage near playground",
    "Overflowing sewage contaminating street water",
    "Pipe leakage in sewer causing puddles",
    "Drain blockage causing unhygienic conditions",
    "Overflowing manhole near junction",
    "Stagnant water due to clogged drainage",
    "Sewage flooding near hospital road",
    "Drainage system failure causing smell",
    "Pipe burst in sewage line",
    "Clogged sewer pipe near school",
    "Overflowing drain near residential complex",
    "Open manhole near highway",
    "Drainage water stagnant near park",
    "Sewage overflowing into street",
    "Clogged storm drain causing contamination",
    "Pipe leak in drainage system",
    "Foul smell from blocked manhole",
    "Drain near market overflowing",
    "Sewage pipe near bus stop broken",
    "Blocked drainage causing health risk",
    "Overflowing sewage near playground",
    "Drainage system leaking into streets",
    "Clogged manhole attracting mosquitoes",
    "Pipe leakage causing sewage spill",
    "Storm drain is full and water is stagnating",
    "Foul smell from sewage is affecting nearby homes",
    "Pipe leakage in the drain is causing flooding",
    "Stagnant water due to overflow",
]

labels += ["Sewage & Drainage"] * 50

# Traffic & Transportation
texts += [
    "Traffic signals at the junction are not working",
    "Damaged pedestrian crossing is unsafe for commuters",
    "Bus stop near the hospital is broken and unusable",
    "Road signage is missing, causing confusion for drivers",
    "Parking issues are making the main road congested",
    "Traffic jam is happening due to blocked lanes",
    "Pedestrian crossing paint is faded and dangerous",
    "Accident-prone junction lacks proper signage",
    "Roundabout signals are malfunctioning",
    "Illegal parking is obstructing traffic near the market",
    "Traffic light not functioning at busy junction",
    "Damaged zebra crossing near school",
    "Bus stop shelter broken and unsafe",
    "Missing road signage causing accidents",
    "Congested main road due to parking issues",
    "Traffic blockage near marketplace",
    "Pedestrian crossing near hospital damaged",
    "Roundabout signs faded and unclear",
    "Traffic signals near park not working",
    "Illegal parking blocking lanes",
    "Bus stop near school unusable",
    "Traffic light malfunctioning at intersection",
    "Damaged road signage causing confusion",
    "Parking lot near market overcrowded",
    "Pedestrian crossing near bus station unsafe",
    "Traffic jam due to lane closure",
    "Roundabout signals flickering",
    "Illegal parking near hospital creating hazards",
    "Damaged crossing near community park",
    "Traffic signal near junction broken",
    "Bus stop near highway roof broken",
    "Missing traffic signs causing accidents",
    "Congested road near playground",
    "Pedestrian path damaged near main road",
    "Traffic blockage due to construction",
    "Roundabout signage missing",
    "Illegal parking near school obstructing road",
    "Traffic light broken near bus stop",
    "Damaged crossing paint near hospital",
    "Bus stop shelter unsafe for commuters",
    # "Road signage faded near park",
    "Parking issues causing jams",
    "Pedestrian crossing broken near market",
    "Traffic signal malfunctioning at roundabout",
    "Lane blocked near junction causing congestion",
    "Illegal parking near community center",
    "Traffic light flickering near school",
    "Traffic jam is happening due to blocked lanes",
    "Pedestrian crossing paint is faded and dangerous",
    "Damaged bus stop near hospital",
    "Signage missing at busy intersection",
]

labels += ["Traffic & Transportation"] * 50

# Building & Housing
texts += [
    "Old building near my house has cracks and is unsafe",
    "Unauthorized construction is happening on the main road",
    "Housing code violations in the neighborhood need attention",
    "Structural damage has made the apartment unsafe to live in",
    "Walls in the public building are crumbling and dangerous",
    "Roof damage is making the house uninhabitable",
    "Apartment foundation has minor cracks",
    "Ceiling has water leakage and is unsafe",
    "Balcony railing is loose and risky",
    "Floor of the building is uneven and damaged",
    "Building near school has cracks",
    "Unauthorized construction near park",
    "Housing code violation reported in colony",
    "Structural damage in apartment building",
    "Walls in office building crumbling",
    "Roof leak causing damage inside house",
    "Apartment wall cracks spreading",
    "Ceiling water leakage near bedroom",
    "Balcony railing broken and unsafe",
    "Floor tiles uneven in building",
    "Old building near market unsafe",
    "Unauthorized construction on main road",
    "Housing code violation near hospital",
    "Structural cracks in residential building",
    "Walls in public building damaged",
    "Roof damage in apartment complex",
    # "Apartment ceiling leaking",
    # "Balcony railing loose near school",
    "Floor cracks in building",
    "Building structure unsafe",
    "Old walls crumbling in house",
    "Unauthorized construction site unsafe",
    "Housing code violation reported",
    "Apartment roof damaged",
    "Walls near corridor cracked",
    "Structural damage in old building",
    "Ceiling collapse risk in apartment",
    "Balcony unsafe for use",
    "Floor damage causing hazard",
    "Building near hospital unsafe",
    "Unauthorized construction near playground",
    "Housing code violation at street",
    "Structural damage near main road",
    "Walls cracked in residential complex",
    "Roof leak near school building",
    "Apartment balcony railing broken",
    "Floor uneven in apartment",
    "Old building unsafe near market",
    "Unauthorized construction observed",
    "Walls in the public building are crumbling and dangerous",
    "Housing violation complaint filed",
]

labels += ["Building & Housing"] * 50

# Health & Safety
texts += [
    "Garbage is lying in open areas attracting rats",
    "Unhygienic conditions near the market are a health hazard",
    "Open drains are causing disease risk in the locality",
    "Fallen electric wires are creating emergency hazards",
    "Stagnant water is breeding mosquitoes near homes",
    "Trash scattered on streets is a risk to public health",
    "Rodent infestation reported near residential area",
    "Open waste near the park is unhygienic",
    "Spill of chemicals is creating a hazard",
    "Blocked emergency exits are unsafe for residents",
    "Garbage bins overflowing near school",
    "Unhygienic conditions in playground",
    "Stagnant water near bus stop",
    "Fallen electric pole wires",
    "Open waste dumping near hospital",
    "Rodents in neighborhood causing health issues",
    "Garbage heap attracting flies",
    "Stagnant puddles near community park",
    "Open drains causing disease outbreak",
    "Spilled chemicals near residential area",
    "Blocked emergency exit in building",
    # "Unhygienic streets near market",
    # "Garbage around park unattended",
    "Stagnant water causing mosquito breeding",
    "Fallen electric wires near junction",
    "Trash in playground causing health risk",
    "Rodent infestation near community center",
    "Open waste near bus stop",
    "Spilled chemical container on street",
    "Garbage heap causing smell",
    "Stagnant water near school",
    "Open drains causing contamination",
    "Emergency hazard from fallen wire",
    "Unhygienic condition near hospital",
    "Garbage scattered in public area",
    "Rodent infestation in street",
    "Stagnant water near playground",
    "Open waste near residential complex",
    "Fallen electric wires on road",
    "Trash causing health hazard",
    "Unhygienic areas near market",
    "Rodent problem near school",
    "Stagnant water creating health risk",
    "Open drains near bus station",
    "Fallen wire causing emergency",
    "Fallen electric wires are creating emergency hazards",
    "Stagnant water is breeding mosquitoes near homes",
    "Trash scattered on streets is a risk to public health",
    "Garbage near junction",
    "Spilled chemicals near playground",
    "Unhygienic garbage heap",
]

labels += ["Health & Safety"] * 50

# Environmental Department
texts += [
    "Illegal tree-cutting is happening in the green zone",
    "Factory smoke is polluting the air near residential areas",
    "Noise pollution from construction is disturbing the neighborhood",
    "Water body near my area is contaminated with waste",
    "Protected green spaces are being encroached illegally",
    "Deforestation near the river is destroying wildlife habitat",
    "Air pollution levels are dangerously high",
    "Noise from heavy vehicles is disturbing the locality",
    "Illegal dumping of industrial waste has been reported",
    "Green space encroachment is affecting community parks",
    "Tree cutting near playground reported",
    "Air pollution near school affecting students",
    "Noise from construction near hospital",
    "Water contamination near river",
    "Green space illegally occupied",
    "Deforestation near community park",
    "Illegal tree felling near market",
    "Factory emissions polluting air",
    "Noise disturbance from industrial activity",
    "Contaminated pond near residential area",
    "Protected park encroached",
    "Tree cutting reported in green zone",
    "Air pollution from nearby factory",
    "Noise near highway affecting residents",
    "Illegal dumping in water body",
    "Green space being reduced illegally",
    "Deforestation affecting wildlife",
    "Tree cutting in public park",
    "Smoke pollution near market area",
    "Noise pollution from ongoing construction",
    "Water contamination in local pond",
    "Protected area encroached illegally",
    # "Illegal tree felling reported",
    "Air pollution affecting school children",
    # "Noise from vehicles disturbing peace",
    "Water contamination near playground",
    "Green area illegally occupied",
    "Deforestation near river bank",
    "Illegal cutting of trees in park",
    "Factory smoke near residential colony",
    "Noise pollution from highway traffic",
    "Water body contaminated with chemicals",
    "Green space encroachment in urban area",
    "Deforestation reported near forest reserve",
    "Illegal tree felling in green area",
    "Air pollution levels dangerously high",
    "Noise from industrial plant disturbing neighborhood",
    "Air pollution levels are dangerously high",
    "Noise from heavy vehicles is disturbing the locality",
    "Water contamination reported near school",
    "Protected park illegally encroached",
]

labels += ["Environmental Department"] * 50



# Create vectorizer and model
vectorize=CountVectorizer()
cls=MultinomialNB()


# Step 2: Train
def train():
 x=vectorize.fit_transform(texts)
 cls.fit(x,labels)

def predict(new_text):
  train()
  x_new=vectorize.transform([new_text])
  lab=cls.predict(x_new)[0]
  
#   print(lab)
  texts.append(new_text)
  labels.append(lab)
  return lab
  

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Complaint Classification API is running 🚀"}


@app.get("/classify")
def classify(q: str = Query(..., description="Complaint text to classify")):
    dep1 = predict(q)  # ML model prediction
    key = sentence_classification(q)
    dep2 = classify_dept(key)  # Keyword-based classification
    
    if dep1 == dep2:
        return {"department": dep1}
    else:
        return {"department": f"{dep1} (ML) and {dep2} (Keywords)"}





# Step 3: Predict for new complaint
# def classify_new_sentences():
#  new_text=(input("Enter :"))
#  new_text=[new_text]
#  value=True

#  while value==True:
# #    print("\n\n----------------------\n\n")
# #    print("Classified by sentence model")
#    dep1=predict(new_text)
#    new_text=str(new_text)
# #   print(texts)
# #   print(labels)
#    key=sentence_classification(new_text)
# #    print("\n\n----------------------\n\n")
# #    print("Classified by keyword model")
#    dep2=classify_dept(key)
#    if dep1==dep2:
#       print(dep1)
#    else:
#       print(f"{dep1} and {dep2}")
#    new_text=(input("Enter :"))

#    if new_text=='0':
#      value=False
#    new_text=[new_text]
   
 
# classify_new_sentences()

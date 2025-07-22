# 🐍 Step 1: Put your master list and present list here
master_list = [
    "Amargadhi", "Anbukhaireni", "Arjundhara", "Bahrabise", "Bansagadhi", "Bardibas", "Barhathawa",
    "Bedkot", "Belauri", "Belbari", "Beni", "Benighat", "Besishahar", "Bhadrapur", "Bhajani",
    "Bhakunde Besi", "Bhanu", "Bheriganga", "Bhimdatta", "Bhimeshwor", "Bhojpur", "Bideha",
    "Binayee Tribeni", "Birendranagar", "Birtamod", "Buddhashanti", "Budhabare", "Budhanilkantha",
    "Byas", "Chainpur", "Chainpur, Bajhang", "Chandrapur", "Changunarayan", "Chautara",
    "Chhireshwornath", "Dailekh Narayan", "Dakshinkali", "Damak", "Dasharathchand", "Devchuli",
    "Devdaha", "Dhading Besi", "Dhangadhi", "Dhankuta", "Dhanusadham", "Dharan", "Dhulikhel",
    "Dhunche", "Diktel", "Dipayal Silgadi", "Dudhouli", "Duhabi", "Dumre", "Dunai", "Fikkal",
    "Gaidakot", "Gajuri", "Galchi", "Galyang", "Gamgadhi", "Gaur", "Gauradhaha", "Gauriganga",
    "Ghodaghodi", "Ghorahi", "Godawari", "Godawari Kailali", "Gokarneshwor", "Gokuleshwor Darchula",
    "Golbazar", "Gulariya", "Gurbhakot", "Hansapur", "Haripur", "Ichchhyakamana", "Ilam", "Inaruwa",
    "Ishworpur", "Itahari", "Jaleswor", "Janakpur", "Jhapa Rural Muncipality", "Jiri", "Jitpur Simara",
    "Jomsom", "Jumla", "Kageshwori Manohara", "Kalaiya", "Kalika", "Kamalamai", "Kamalbazar",
    "Kanchan", "Kanchanrup", "Kankai", "Kapilbastu", "Kathmandu", "Kawasoti", "Khairahani", "Khajura",
    "Khalanga Darchula", "Khalanga Jajarkot", "Khandbari", "Kirtipur", "Kohalpur", "Krishnanagar",
    "Kusma", "Lahan", "Lamkichuha", "Lekbesi", "Letang", "Lumbini Sanskritik", "Madhyabindu",
    "Madhyapur Thimi", "Madi", "Mahalaxmi", "Malangwa", "Mangalsen", "Manma", "Manthali", "Martadi",
    "Mechinagar", "Melamchi", "Mirchaiya", "Mithila", "Mithila Bihari", "Musikot", "Myanglung",
    "Nagarain", "Nagarjun", "Nepalgunj", "Nijgadh", "Nilakantha", "Omsatiya", "Pakhribas", "Panchkhal",
    "Parsa", "Pathari Shanishchare", "Phungling", "Pratappur", "Putalibazar", "Pyuthan", "Rajapur",
    "Rajbiraj", "Ramdhuni", "Ramgram", "Rangeli", "Rapti", "Ratuwamai", "Resunga", "Rolpa", "Rukumkot",
    "Sabaila", "Sainamaina", "Salleri", "Salyan", "Sandhikharka", "Sanfebagar", "Shankharapur",
    "Shivasataxi", "Shuklagandaki", "Siddharthanagar", "Siddhicharan", "Simikot", "Siraha", "Suddhodhan",
    "Suddodhan", "Sundarbazar", "Sundarharaicha", "Sunwal", "Sunwarshi", "Suryabinayak", "Tansen",
    "Tarkeshwar", "Tikapur", "Tillotama", "Tokha", "Triyuga", "Tulsipur", "Urlabari"
]

present_list = [
    "Amargadhi", "Anbukhaireni", "Baglung", "Banepa", "Banganga", "Bardaghat", "Bardibas", "Barhathawa",
    "Beni", "Besishahar", "Bhadrapur", "Bhanu", "Bharatpur", "Bhimad", "Bhimdatta", "Bhimeshwor",
    "Bhojpur", "Bidur", "Binayee Tribeni", "Biratnagar", "Birendranagar", "Birgunj", "Birtamod", "Butwal",
    "Byas", "Chainpur", "Chainpur, Bajhang", "Chandragiri", "Chandrapur", "Chautara", "Dailekh Narayan",
    "Damak", "Dasharathchand", "Devdaha", "Dhangadhi", "Dhankuta", "Dharan", "Dhunche", "Diktel",
    "Dipayal Silgadi", "Duhabi", "Dumre", "Fikkal", "Galyang", "Gaur", "Gauradhaha", "Ghorahi",
    "Gokarneshwor", "Gokuleshwor Darchula", "Gorkha", "Gulariya", "Hariwan", "Hetauda", "Ilam", "Inaruwa",
    "Itahari", "Jaleswor", "Janakpur", "Jiri", "Jitpur Simara", "Jomsom", "Jumla", "Kageshwori Manohara",
    "Kamalamai", "Kapilbastu", "Kathmandu", "Kawasoti", "Khalanga Darchula", "Khalanga Jajarkot",
    "Khandbari", "Kusma", "Lalitpur", "Lamahi", "Lamkichuha", "Lekhnath", "Malangwa", "Mangalsen",
    "Manma", "Manthali", "Martadi", "Mechinagar", "Melamchi", "Mithila", "Musikot", "Myanglung",
    "Nepalgunj", "Nilakantha", "Pathari Shanishchare", "Phidim", "Phungling Municipality", "Pokhara",
    "Putalibazar", "Pyuthan", "Ramgram", "Rampur", "Rangeli", "Ratnanagar", "Resunga", "Rolpa", "Rukumkot",
    "Salleri", "Salyan", "Sandhikharka", "Shivaraj", "Siddharthanagar", "Siddhicharan", "Simikot",
    "Sundarbazar", "Sundarharaicha", "Sunwal", "Suryabinayak", "Tansen", "Tikapur", "Tillotama",
    "Tulsipur", "Urlabari", "Waling"
]

# 🐍 Step 2: Convert to lower case for case-insensitive comparison
master_set = set(name.lower().strip() for name in master_list)
present_set = set(name.lower().strip() for name in present_list)

# 🐍 Step 3: Find missing cities
missing_cities = sorted(master_set - present_set)

# 🐍 Step 4: Print nicely (title case)
print("✅ Unique / missing cities:")
for city in missing_cities:
    print(city.title())

# 🐍 Optional: save to Excel
import pandas as pd
pd.DataFrame({'Missing_Cities': [city.title() for city in missing_cities]}).to_excel('unique_missing_cities.xlsx', index=False)
print("\n📄 Saved to unique_missing_cities.xlsx")

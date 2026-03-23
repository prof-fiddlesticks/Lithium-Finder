import ee
import geemap
import os

# 1. Initialize GEE
try:
    ee.Initialize(project='lithium-finder')
except Exception as e:
    ee.Authenticate()
    ee.Initialize(project='lithium-finder')

print("1. Authenticated successfully. Building 100-site dataset...")

# 2. THE COORDINATES (100 Sites)
locations = [
    # --- 50 LITHIUM SITES (Label: 1) ---
    {'Site': 'Atacama, Chile', 'lat': -23.65, 'lon': -68.30, 'label': 1},
    {'Site': 'Salar de Uyuni, Bolivia', 'lat': -20.20, 'lon': -67.50, 'label': 1},
    {'Site': 'Clayton Valley, USA', 'lat': 37.75, 'lon': -117.65, 'label': 1},
    {'Site': 'Hombre Muerto, Argentina', 'lat': -25.45, 'lon': -67.05, 'label': 1},
    {'Site': 'Greenbushes, Australia', 'lat': -33.85, 'lon': 116.05, 'label': 1},
    {'Site': 'Pilgangoora, Australia', 'lat': -21.01, 'lon': 118.88, 'label': 1},
    {'Site': 'Thacker Pass, USA', 'lat': 41.70, 'lon': -118.00, 'label': 1},
    {'Site': 'Salar de Arizaro, Argentina', 'lat': -24.40, 'lon': -66.90, 'label': 1},
    {'Site': 'Salar de Tara, Chile', 'lat': -23.20, 'lon': -67.40, 'label': 1},
    {'Site': 'Bristol Lake, USA', 'lat': 34.80, 'lon': -115.70, 'label': 1},
    {'Site': 'Searles Lake, USA', 'lat': 35.70, 'lon': -117.30, 'label': 1},
    {'Site': 'Salar de Maricunga, Chile', 'lat': -27.20, 'lon': -68.60, 'label': 1},
    {'Site': 'Salar de Coipasa, Chile', 'lat': -19.50, 'lon': -69.10, 'label': 1},
    {'Site': 'Silver Peak, USA', 'lat': 38.10, 'lon': -117.20, 'label': 1},
    {'Site': 'Cauchari-Olaroz, Argentina', 'lat': -23.90, 'lon': -66.10, 'label': 1},
    {'Site': 'Mount Marion, Australia', 'lat': -31.15, 'lon': 121.48, 'label': 1},
    {'Site': 'Wodgina, Australia', 'lat': -21.18, 'lon': 118.66, 'label': 1},
    {'Site': 'Bikita, Zimbabwe', 'lat': -19.95, 'lon': 31.43, 'label': 1},
    {'Site': 'Manono, DRC', 'lat': -7.30, 'lon': 27.41, 'label': 1},
    {'Site': 'Whabouchi, Canada', 'lat': 51.68, 'lon': -75.86, 'label': 1},
    {'Site': 'Goulamina, Mali', 'lat': 11.02, 'lon': -7.63, 'label': 1},
    {'Site': 'Salar de Diablillos, Argentina', 'lat': -25.28, 'lon': -66.81, 'label': 1},
    {'Site': 'Salar de Centenario, Argentina', 'lat': -24.65, 'lon': -66.75, 'label': 1},
    {'Site': 'Salar de Llullaillaco, Argentina', 'lat': -24.71, 'lon': -68.53, 'label': 1},
    {'Site': 'Salar de Olaroz, Argentina', 'lat': -23.80, 'lon': -66.80, 'label': 1},
    {'Site': 'Salar de Rincon, Argentina', 'lat': -24.15, 'lon': -67.05, 'label': 1},
    {'Site': 'Salar de Pozuelos, Argentina', 'lat': -24.35, 'lon': -66.95, 'label': 1},
    {'Site': 'Salar de Pastos Grandes, Arg', 'lat': -24.45, 'lon': -66.75, 'label': 1},
    {'Site': 'Salar de Tres Quebradas, Arg', 'lat': -27.30, 'lon': -68.65, 'label': 1},
    {'Site': 'Salar de Pedernales, Chile', 'lat': -26.25, 'lon': -69.15, 'label': 1},
    {'Site': 'Salar de Ascotan, Chile', 'lat': -21.65, 'lon': -68.25, 'label': 1},
    {'Site': 'Salar de Carcote, Chile', 'lat': -21.35, 'lon': -68.35, 'label': 1},
    {'Site': 'Salar de Surire, Chile', 'lat': -18.85, 'lon': -69.05, 'label': 1},
    {'Site': 'Salar de Quisquiro, Chile', 'lat': -23.25, 'lon': -67.25, 'label': 1},
    {'Site': 'Salar de Jama, Argentina', 'lat': -23.20, 'lon': -66.95, 'label': 1},
    {'Site': 'Zhabuye Salt Lake, China', 'lat': 31.35, 'lon': 84.05, 'label': 1},
    {'Site': 'Taijinaier Salt Lake, China', 'lat': 37.85, 'lon': 93.65, 'label': 1},
    {'Site': 'Salton Sea Geothermal, USA', 'lat': 33.20, 'lon': -115.60, 'label': 1},
    {'Site': 'Smackover Surface Proxy, USA', 'lat': 33.25, 'lon': -92.65, 'label': 1},
    {'Site': 'Finniss, Australia', 'lat': -12.75, 'lon': 130.65, 'label': 1},
    {'Site': 'Kathleen Valley, Australia', 'lat': -27.55, 'lon': 120.65, 'label': 1},
    {'Site': 'Mt Cattlin, Australia', 'lat': -33.55, 'lon': 120.05, 'label': 1},
    {'Site': 'Bald Hill, Australia', 'lat': -31.75, 'lon': 122.05, 'label': 1},
    {'Site': 'Mt Holland, Australia', 'lat': -32.15, 'lon': 119.75, 'label': 1},
    {'Site': 'Tanco Mine, Canada', 'lat': 50.45, 'lon': -95.35, 'label': 1},
    {'Site': 'Rose Lithium, Canada', 'lat': 52.05, 'lon': -76.85, 'label': 1},
    {'Site': 'Moblan, Canada', 'lat': 50.65, 'lon': -74.95, 'label': 1},
    {'Site': 'Arcadia, Zimbabwe', 'lat': -17.75, 'lon': 31.45, 'label': 1},
    {'Site': 'Bougouni, Mali', 'lat': 11.45, 'lon': -7.55, 'label': 1},
    {'Site': 'Cinovec, Czech Republic', 'lat': 50.75, 'lon': 13.75, 'label': 1},

    # --- 50 CONTROL SITES (Label: 0) ---
    {'Site': 'Amazon Forest', 'lat': -3.10, 'lon': -60.00, 'label': 0},
    {'Site': 'New York City', 'lat': 40.78, 'lon': -73.96, 'label': 0},
    {'Site': 'Tokyo', 'lat': 35.68, 'lon': 139.76, 'label': 0},
    {'Site': 'Sahara Desert', 'lat': 25.00, 'lon': 15.00, 'label': 0},
    {'Site': 'Outback Australia', 'lat': -25.00, 'lon': 133.00, 'label': 0},
    {'Site': 'Paris', 'lat': 48.85, 'lon': 2.35, 'label': 0},
    {'Site': 'Brasilia', 'lat': -15.79, 'lon': -47.88, 'label': 0},
    {'Site': 'London', 'lat': 51.50, 'lon': -0.12, 'label': 0},
    {'Site': 'Shanghai', 'lat': 31.23, 'lon': 121.47, 'label': 0},
    {'Site': 'Sydney', 'lat': -33.86, 'lon': 151.20, 'label': 0},
    {'Site': 'Agra, India', 'lat': 27.17, 'lon': 78.04, 'label': 0},
    {'Site': 'Singapore', 'lat': 1.35, 'lon': 103.81, 'label': 0},
    {'Site': 'Reykjavik', 'lat': 64.14, 'lon': -21.94, 'label': 0},
    {'Site': 'Buenos Aires', 'lat': -34.60, 'lon': -58.38, 'label': 0},
    {'Site': 'Mexico City', 'lat': 19.43, 'lon': -99.13, 'label': 0},
    {'Site': 'Greenland Ice Sheet', 'lat': 72.00, 'lon': -40.00, 'label': 0},
    {'Site': 'Pacific Ocean', 'lat': 0.00, 'lon': -140.00, 'label': 0},
    {'Site': 'Yellowstone Geysers', 'lat': 44.42, 'lon': -110.58, 'label': 0},
    {'Site': 'Iowa Cornfield', 'lat': 42.00, 'lon': -93.00, 'label': 0},
    {'Site': 'Swiss Alps', 'lat': 46.55, 'lon': 8.55, 'label': 0},
    {'Site': 'Gobi Desert', 'lat': 42.50, 'lon': 105.00, 'label': 0},
    {'Site': 'Kalahari Desert', 'lat': -23.00, 'lon': 22.00, 'label': 0},
    {'Site': 'Siberian Tundra', 'lat': 65.00, 'lon': 100.00, 'label': 0},
    {'Site': 'Dubai Desert', 'lat': 24.80, 'lon': 55.40, 'label': 0},
    {'Site': 'Grand Canyon', 'lat': 36.10, 'lon': -112.10, 'label': 0},
    {'Site': 'Death Valley, USA', 'lat': 36.25, 'lon': -116.85, 'label': 0},
    {'Site': 'White Sands, USA', 'lat': 32.75, 'lon': -106.25, 'label': 0},
    {'Site': 'Bonneville Salt Flats, USA', 'lat': 40.75, 'lon': -113.85, 'label': 0},
    {'Site': 'Aral Sea (Dried), KAZ', 'lat': 45.35, 'lon': 59.65, 'label': 0},
    {'Site': 'Atacama Dirt, Chile', 'lat': -24.50, 'lon': -69.50, 'label': 0},
    {'Site': 'Rub al Khali, KSA', 'lat': 20.00, 'lon': 50.00, 'label': 0},
    {'Site': 'Simpson Desert, AUS', 'lat': -24.55, 'lon': 137.55, 'label': 0},
    {'Site': 'Bingham Canyon Mine, USA', 'lat': 40.52, 'lon': -112.15, 'label': 0},
    {'Site': 'Mount Vesuvius, ITA', 'lat': 40.82, 'lon': 14.42, 'label': 0},
    {'Site': 'Lake Superior, USA', 'lat': 47.75, 'lon': -87.55, 'label': 0},
    {'Site': 'Victoria Falls, ZMB', 'lat': -17.92, 'lon': 25.85, 'label': 0},
    {'Site': 'Antarctic Ice Shelf', 'lat': -75.00, 'lon': 0.00, 'label': 0},
    {'Site': 'Mount Everest', 'lat': 27.98, 'lon': 86.92, 'label': 0},
    {'Site': 'Loch Ness, UK', 'lat': 57.32, 'lon': -4.42, 'label': 0},
    {'Site': 'Congo Rainforest', 'lat': -0.50, 'lon': 20.00, 'label': 0},
    {'Site': 'Everglades Swamp, USA', 'lat': 25.75, 'lon': -80.65, 'label': 0},
    {'Site': 'Taiga Forest, RUS', 'lat': 60.00, 'lon': 90.00, 'label': 0},
    {'Site': 'Black Forest, GER', 'lat': 48.35, 'lon': 8.15, 'label': 0},
    {'Site': 'Sundarbans Mangroves, BGD', 'lat': 21.95, 'lon': 89.15, 'label': 0},
    {'Site': 'Los Angeles, USA', 'lat': 34.05, 'lon': -118.24, 'label': 0},
    {'Site': 'Cairo, EGY', 'lat': 30.04, 'lon': 31.23, 'label': 0},
    {'Site': 'Mumbai, IND', 'lat': 19.07, 'lon': 72.87, 'label': 0},
    {'Site': 'Beijing, CHN', 'lat': 39.90, 'lon': 116.40, 'label': 0},
    {'Site': 'Sao Paulo, BRA', 'lat': -23.55, 'lon': -46.63, 'label': 0},
    {'Site': 'Johannesburg, ZAF', 'lat': -26.20, 'lon': 28.04, 'label': 0}
]

# Convert to GEE Features
pts = ee.FeatureCollection([
    ee.Feature(ee.Geometry.Point([loc['lon'], loc['lat']]), {'Site': loc['Site'], 'Label': loc['label']})
    for loc in locations
])

# 3. DEFINE THE 20 MARKERS
def get_all_20_markers(image):
    b = {
        'B2': image.select('B2'), 'B3': image.select('B3'),
        'B4': image.select('B4'), 'B7': image.select('B7'),
        'B8': image.select('B8'), 'B8A': image.select('B8A'),
        'B11': image.select('B11'), 'B12': image.select('B12')
    }

    # Group 1: Evaporites
    si1 = image.expression('sqrt(B4 * B11)', b).rename('SI1')
    ndsi = image.normalizedDifference(['B11', 'B12']).rename('NDSI')
    bmi = b['B2'].divide(b['B11']).rename('BMI')
    borate = b['B12'].divide(b['B11']).rename('Borate_Proxy')
    mndwi = image.normalizedDifference(['B3', 'B11']).rename('MNDWI')
    ndmi = image.normalizedDifference(['B8', 'B11']).rename('NDMI')
    albedo = image.expression('sqrt((B4**2 + B3**2 + B2**2) / 3.0)', b).rename('Albedo')

    # Group 2: Clays
    clay_cmr = b['B11'].divide(b['B12']).rename('Clay_CMR')
    hydrox = b['B11'].divide(b['B8A']).rename('Hydroxyl_OHI')
    argillic = b['B12'].divide(b['B8']).rename('Argillic')
    sulfate = b['B11'].divide(b['B4']).rename('Sulfate_Proxy')

    # Group 3: Hard Rock
    iron_ox = b['B4'].divide(b['B2']).rename('Iron_Oxide')
    ferrous = b['B11'].divide(b['B8']).rename('Ferrous_Idx')
    gossan = b['B11'].divide(b['B4']).rename('Gossan')
    silica = b['B4'].divide(b['B11']).rename('Silica_Proxy')

    # Group 4: Context
    veg_stress = b['B8A'].divide(b['B7']).rename('VegStress')
    bsi = image.expression('((B11 + B4) - (B8 + B2)) / ((B11 + B4) + (B8 + B2))', b).rename('BSI')
    savi = image.expression('((B8 - B4) / (B8 + B4 + 0.5)) * 1.5', b).rename('SAVI')
    ndbi = image.normalizedDifference(['B11', 'B8']).rename('NDBI')
    shadow = b['B2'].divide(b['B4']).rename('Shadow_Proxy')

    return image.addBands([
        si1, ndsi, bmi, borate, mndwi, ndmi, albedo,
        clay_cmr, hydrox, argillic, sulfate,
        iron_ox, ferrous, gossan, silica,
        veg_stress, bsi, savi, ndbi, shadow
    ])

print("2. Requesting Sentinel-2 Imagery...")

# 4. LOAD SATELLITE DATA
s2 = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
      .filterBounds(pts)
      .filterDate('2023-01-01', '2023-12-31')
      .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
      .median())

full_stack = get_all_20_markers(s2)

# 5. EXTRACT THE DATA
print("3. Extracting 20 chemistry markers at all 100 points (this will take a couple minutes)...")

features_to_extract = [
    'SI1', 'NDSI', 'BMI', 'Borate_Proxy', 'MNDWI', 'NDMI', 'Albedo',
    'Clay_CMR', 'Hydroxyl_OHI', 'Argillic', 'Sulfate_Proxy',
    'Iron_Oxide', 'Ferrous_Idx', 'Gossan', 'Silica_Proxy',
    'VegStress', 'BSI', 'SAVI', 'NDBI', 'Shadow_Proxy'
]

training_set = full_stack.select(features_to_extract).sampleRegions(
    collection=pts,
    properties=['Site', 'Label'],
    scale=20,
    tileScale=4
)

# 6. EXPORT TO CSV
output_file = os.path.join(os.getcwd(), 'master_lithium_dataset_100_sites.csv')
geemap.ee_to_csv(training_set, filename=output_file)

print(f"✅ SUCCESS! Massive 100-Site Dataset saved to: {output_file}")

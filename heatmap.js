// ==========================================
// 1. TARGET LOCATION (Salar de Atacama)
// ==========================================
var lat = -23.5;
var lon = -68.15;
var roi = ee.Geometry.Point([lon, lat]).buffer(30000); // 30km radius
Map.setCenter(lon, lat, 10);

// ==========================================
// 2. PULL SATELLITE CONSTELLATIONS
// ==========================================
var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterBounds(roi)
    .filterDate('2023-01-01', '2023-12-31')
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
    .median()
    .clip(roi);

var s1 = ee.ImageCollection('COPERNICUS/S1_GRD')
    .filterBounds(roi)
    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
    .filter(ee.Filter.eq('instrumentMode', 'IW'))
    .median()
    .clip(roi);

var dem = ee.Image('NASA/NASADEM_HGT/001').select('elevation').clip(roi);
var terrain = ee.Terrain.products(dem);

var l8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
    .filterBounds(roi)
    .filterDate('2023-01-01', '2023-12-31')
    .filter(ee.Filter.lt('CLOUD_COVER', 10))
    .median()
    .clip(roi);

// ==========================================
// 3. CALCULATE THE 20 MARKERS 
// ==========================================
// Group 1: Spectral
var swir_1 = s2.select('B11');
var swir_2 = s2.select('B12');
var nir = s2.select('B8');
var clay_idx = s2.select('B11').divide(s2.select('B12')).rename('Clay');
var iron_ox = s2.select('B4').divide(s2.select('B3')).rename('Iron');
var ndsi = s2.normalizedDifference(['B3', 'B11']).rename('NDSI');
var gypsum = s2.select('B11').divide(s2.select('B8')).rename('Gypsum');
var borate = s2.select('B12').divide(s2.select('B8')).rename('Borate');

// Group 2: Bio-Geo
var ndvi = s2.normalizedDifference(['B8', 'B4']).rename('NDVI');
var ndre = s2.normalizedDifference(['B8A', 'B5']).rename('NDRE');
var ndwi = s2.normalizedDifference(['B3', 'B8']).rename('NDWI');
var savi = s2.expression('((B8 - B4) / (B8 + B4 + 0.5)) * 1.5', {
    'B8': s2.select('B8'),
    'B4': s2.select('B4')
}).rename('SAVI');

// Group 3: Structure
var elev = dem;
var slope = terrain.select('slope');
var aspect = terrain.select('aspect');
var radar_vv = s1.select('VV');
var radar_vh = s1.select('VH');
var radar_ratio = radar_vv.divide(radar_vh).rename('Radar_Ratio');

// Group 4: Thermal
var temp_c = l8.select('ST_B10').multiply(0.00341802).add(149.0).subtract(273.15).rename('Temp_C');
var therm_stress = temp_c.divide(ndvi.add(1.1)).rename('Therm_Stress');

// ==========================================
// 4. NORMALIZE TO "INTENSITY" HEATMAPS (0.0 to 1.0)
// ==========================================
var make_heatmap = function(image, min_val, max_val) {
    return image.unitScale(min_val, max_val).clamp(0, 1);
};

// Heatmap Palette: Black -> Purple -> Red -> Orange -> Yellow
var pal_heat = ['000000', '4B0082', 'FF0000', 'FF8C00', 'FFFF00'];
var vis_heat = {min: 0, max: 1, palette: pal_heat};

// ==========================================
// 5. ADD ALL 20 LAYERS TO MAP
// ==========================================
Map.addLayer(s2, {bands: ['B4', 'B3', 'B2'], min: 0, max: 3000}, '0. Base True Color', true);

// 1. Spectral
Map.addLayer(make_heatmap(swir_1, 1000, 4000), vis_heat, 'M1: SWIR_1 Intensity', false);
Map.addLayer(make_heatmap(swir_2, 500, 3500), vis_heat, 'M2: SWIR_2 Intensity', false);
Map.addLayer(make_heatmap(nir, 1000, 4000), vis_heat, 'M3: NIR Intensity', false);
Map.addLayer(make_heatmap(clay_idx, 0.8, 1.5), vis_heat, 'M12: Clay Index Heatmap', false);
Map.addLayer(make_heatmap(iron_ox, 0.5, 2.0), vis_heat, 'M13: Iron Oxide Heatmap', false);
Map.addLayer(make_heatmap(ndsi, -0.2, 0.5), vis_heat, 'M11: NDSI Heatmap', false);
Map.addLayer(make_heatmap(gypsum, 0.5, 2.0), vis_heat, 'M14: Gypsum Heatmap', false);
Map.addLayer(make_heatmap(borate, 0.5, 1.5), vis_heat, 'M15: Borate Proxy Heatmap', false);

// 2. Bio-Geo
Map.addLayer(make_heatmap(ndvi, -0.2, 0.6), vis_heat, 'M7: NDVI Heatmap', false);
Map.addLayer(make_heatmap(ndre, -0.1, 0.4), vis_heat, 'M8: NDRE Heatmap', false);
Map.addLayer(make_heatmap(ndwi, -0.5, 0.2), vis_heat, 'M10: NDWI Moisture Heatmap', false);
Map.addLayer(make_heatmap(savi, -0.2, 0.5), vis_heat, 'M9: SAVI Heatmap', false);

// 3. Structure
Map.addLayer(make_heatmap(elev, 2000, 4500), vis_heat, 'M4: Elevation Heatmap', false);
Map.addLayer(make_heatmap(slope, 0, 30), vis_heat, 'M5: Slope Heatmap', false);
Map.addLayer(make_heatmap(aspect, 0, 360), vis_heat, 'M6: Aspect Heatmap', false);
Map.addLayer(make_heatmap(radar_vv, -25, 0), vis_heat, 'M18: Radar VV Roughness', false);
Map.addLayer(make_heatmap(radar_vh, -30, -5), vis_heat, 'M19: Radar VH Scattering', false);
Map.addLayer(make_heatmap(radar_ratio, 0.5, 2.0), vis_heat, 'M20: Radar Lineament Heatmap', false);

// 4. Thermal
Map.addLayer(make_heatmap(temp_c, 15, 45), vis_heat, 'M16: Surface Temp Heatmap', false);
Map.addLayer(make_heatmap(therm_stress, 10, 40), vis_heat, 'M17: Thermal Stress Heatmap', false);

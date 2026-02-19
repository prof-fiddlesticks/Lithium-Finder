/**
 * LITHIUM PROSPECTING SUITE (FIXED)
 */

// 1. AREA OF INTEREST
var roi = ee.Geometry.Point([-67.48, -23.55]).buffer(25000); 
Map.centerObject(roi, 10);

// 2. DATASETS
var s2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterBounds(roi).filterDate('2023-01-01', '2023-12-31')
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10)).median();

var aster = ee.ImageCollection("ASTER/AST_L1T_003")
    .filterBounds(roi).median().resample('bilinear')
    .reproject({crs: s2.projection(), scale: 20});

var alos = ee.ImageCollection("JAXA/ALOS/PALSAR/YEARLY/SAR_EPOCH")
    .filterBounds(roi).first().clip(roi);

// 3. THE 20 MARKERS
var M1 = s2.select('B11').divide(s2.select('B12')).rename('M1_Clay');
var M2 = s2.select('B11').divide(s2.select('B8A')).rename('M2_Hydroxyl');
var M3 = aster.select('B04').divide(aster.select('B06')).rename('M3_Alunite');
var M4 = aster.select('B04').divide(aster.select('B05')).rename('M4_Kaolinite');
var M5 = aster.select('B06').divide(aster.select('B07')).rename('M5_Sericite');
var M6 = s2.normalizedDifference(['B8', 'B4']).rename('M6_NDVI');
var M7 = s2.select('B8A').divide(s2.select('B7')).rename('M7_RedEdge');
var M8 = s2.expression('2.5*((B8-B4)/(B8+6*B4-7.5*B2+1))', {'B8':s2.select('B8'),'B4':s2.select('B4'),'B2':s2.select('B2')}).rename('M8_EVI');
var M9 = s2.normalizedDifference(['B8A', 'B11']).rename('M9_CanopyWater');
var M10 = s2.select('B3').divide(s2.select('B2')).rename('M10_Chloro');
var M11 = s2.normalizedDifference(['B3', 'B8']).rename('M11_NDWI');
var M12 = s2.expression('sqrt(B4*B11)', {'B4':s2.select('B4'),'B11':s2.select('B11')}).rename('M12_Salinity');
var M13 = s2.normalizedDifference(['B8', 'B11']).rename('M13_NDMI');
var M14 = s2.select(['B2','B3','B4']).reduce(ee.Reducer.mean()).rename('M14_Albedo');
var M15 = s2.select('B2').divide(s2.select('B11')).rename('M15_Brine');
var M16 = aster.select('B13').divide(aster.select('B10')).rename('M16_Silicate');
var M17 = aster.select('B13').divide(aster.select('B14')).rename('M17_Carbonate');
var M18 = aster.select('B13').multiply(0.006822).subtract(273.15).rename('M18_LST');
var M19 = alos.select('HV').rename('M19_SAR');
var M20 = s2.select('B4').divide(s2.select('B2')).rename('M20_Iron');

// 4. THE STACK & ANALYTICS
var stack = ee.Image.cat([M1,M2,M3,M4,M5,M6,M7,M8,M9,M10,M11,M12,M13,M14,M15,M16,M17,M18,M19,M20]);
var totalScore = stack.reduce(ee.Reducer.mean()).rename('Li_Potential');

// 5. ALWAYS-ON LAYERS (Moved outside evaluate)
Map.addLayer(s2, {bands:['B4','B3','B2'], max:3000}, '1. Natural Color');
Map.addLayer(M7, {min: 0.8, max: 1.2, palette: ['black', 'orange', 'white']}, '2. Veg Stress Marker');

// 6. ASYNC HEATMAP WITH SAFETY CHECK
totalScore.reduceRegion({
  reducer: ee.Reducer.percentile([2, 98]),
  geometry: roi,
  scale: 100, // Increased scale to make it faster/stable
  maxPixels: 1e9
}).evaluate(function(stats) {
  // If stats is undefined, use fallback values
  var minVal = stats ? stats['Li_Potential_p2'] : 0.8;
  var maxVal = stats ? stats['Li_Potential_p98'] : 2.0;
  
  Map.addLayer(totalScore, {
    min: minVal, 
    max: maxVal, 
    palette: ['#0000ff', '#00ffff', '#ffff00', '#ffaa00', '#ff0000']
  }, '3. Lithium Potential Heatmap');
});

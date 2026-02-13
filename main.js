// =============================================================================
// 1. DEFINE THE 5 PROBES
// =============================================================================
var pond1 = ee.Geometry.Point([-68.385, -23.575]); // Pond 1 (Fresh)
var pond2 = ee.Geometry.Point([-68.369, -23.575]); // Pond 2 (Active)
var pond3 = ee.Geometry.Point([-68.355, -23.575]); // Pond 3 (Old)
var pond4 = ee.Geometry.Point([-68.369, -23.560]); // Pond 4 (North)
var pond5 = ee.Geometry.Point([-68.369, -23.590]); // Pond 5 (South)

// Combine them so we can draw them on the map later
var allPonds = ee.FeatureCollection([
  ee.Feature(pond1, {'label': 'Pond 1'}),
  ee.Feature(pond2, {'label': 'Pond 2'}),
  ee.Feature(pond3, {'label': 'Pond 3'}),
  ee.Feature(pond4, {'label': 'Pond 4'}),
  ee.Feature(pond5, {'label': 'Pond 5'})
]);

// =============================================================================
// 2. LOAD DATA (FIXED TO PREVENT ERROR)
// =============================================================================
var dataset = ee.ImageCollection('COPERNICUS/S2_SR')
    .filterBounds(allPonds)
    .filterDate('2023-01-01', '2024-12-30')
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 2))
    // *** THE FIX ***: We explicitely select bands here to stop the "Tile Error"
    .select(['B2', 'B3', 'B4', 'B8']);

// =============================================================================
// 3. THE MATH FUNCTION (Calculates Index + Formats Bands)
// =============================================================================
var processImage = function(image) {
  // 1. Scale raw bands so they fit on the graph (0-40 range)
  var blue  = image.select('B2').divide(100).rename('Blue');
  var green = image.select('B3').divide(100).rename('Green');
  var red   = image.select('B4').divide(100).rename('Red');
  var nir   = image.select('B8').divide(100).rename('NIR');

  // 2. Calculate Lithium Index (Red / Blue)
  // We multiply by 20 just to make it sit higher on the chart so you can see it
  var lithiumIndex = image.select('B4').divide(image.select('B2'))
                          .multiply(20) 
                          .rename('Lithium_Index_x20');

  // 3. Combine everything
  return ee.Image.cat([blue, green, red, nir, lithiumIndex])
                 .set('system:time_start', image.get('system:time_start'));
};

var timeSeries = dataset.map(processImage);

// =============================================================================
// 4. GENERATE 5 SEPARATE CHARTS (One per Pond)
// =============================================================================

// Define the Chart Style Helper
var makeChart = function(region, title) {
  return ui.Chart.image.series({
    imageCollection: timeSeries,
    region: region,
    reducer: ee.Reducer.mean(),
    scale: 10
  }).setOptions({
    title: title,
    vAxis: {title: 'Value'},
    hAxis: {title: 'Date'},
    // Explicit Colors: Blue, Green, Red, Gray(NIR), Orange(Index)
    colors: ['blue', 'green', 'red', 'gray', '#e0440e'], 
    lineWidth: 2
  });
};

// Print them to the Console
print('Analyzing Pond 1...', makeChart(pond1, 'Pond 1 Analysis'));
print('Analyzing Pond 2...', makeChart(pond2, 'Pond 2 Analysis'));
print('Analyzing Pond 3...', makeChart(pond3, 'Pond 3 Analysis'));
print('Analyzing Pond 4...', makeChart(pond4, 'Pond 4 Analysis'));
print('Analyzing Pond 5...', makeChart(pond5, 'Pond 5 Analysis'));

// =============================================================================
// 5. MAP VISUALIZATION (FIXED)
// =============================================================================
Map.centerObject(pond2, 14);
Map.setOptions('SATELLITE');

// Draw the Ponds
Map.addLayer(allPonds.draw({color: 'white', pointRadius: 5}), {}, 'Probe Locations');

// Background Image (FIXED: Added .select to prevent crash)
var bgImage = ee.ImageCollection('COPERNICUS/S2_SR')
                .filterBounds(allPonds)
                .filterDate('2023-01-01', '2023-06-30')
                .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 5))
                .select(['B4', 'B3', 'B2']) // <--- This fixes the Red Error Box
                .median();

Map.addLayer(bgImage, {min: 0, max: 3000}, 'Visual Reference (True Color)', true, 0.6);

def addition(numbers: list) -> float:
    return sum(numbers)
def show_code():
    code = '''
<%@ page language="java" contentType="text/html; charset=UTF-8"
pageEncoding="UTF-8" %>
<!DOCTYPE html>
<html>
<head>
 <meta charset="UTF-8">
 <title>Google Maps JSP</title>
 <script
src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDfq8d0ZSNXvrptb9MzFsIFoRWayhpTt0Y"
></script>
 <script>
 function initMap() {
 var lat = parseFloat(document.getElementById("lat").value) || 0;
 var lng = parseFloat(document.getElementById("lng").value) || 0;
 var map = new google.maps.Map(document.getElementById('map'), {
 center: { lat: lat, lng: lng },
 zoom: 10
 });
 new google.maps.Marker({
 position: { lat: lat, lng: lng },
 map: map
 });
 }
 </script>
</head>
<body>
 <h2>Enter Coordinates</h2>
 <form action="" method="get" onsubmit="initMap(); return false;">
 Latitude: <input type="text" id="lat" name="lat" required><br>
 Longitude: <input type="text" id="lng" name="lng" required><br>
 <button type="submit">Show on Map</button>
 </form>
 <div id="map" style="width: 100%; height: 400px;"></div>
</body>
</html>
    '''
    print(code)
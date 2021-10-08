
// $(document).ready(function(){
    $('#street').on('focus',function(){
        $("#showmap").modal('show');
    });
    // });
     var user_location;
    
          function initMap() {
             if (document.getElementById("demo_map") !== null) {
            
            
            var myLatlng = {lat:-6.802353,lng:39.279556}
           const map = new google.maps.Map(document.getElementById("demo_map"), {
              center: myLatlng,
              zoom: 15,
              fullscreenControl: false,
              zoomControl: true,
              scaleControl: true,
              Mapsize: 'any',
              // mapTypeId: "roadmap"
            });
           const input = document.getElementById("map_search");
           const searchBox = new google.maps.places.SearchBox(input);
           // map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
           map.addListener("bounds_changed", () => {
              searchBox.setBounds(map.getBounds());
            });
            let markers = [];
            searchBox.addListener("places_changed", () => {
              const places = searchBox.getPlaces();
    
              if (places.length == 0) {
                return;
              } // Clear out the old markers.
    
              markers.forEach(marker => {
                marker.setMap(null);
              });
              markers = [];
            const bounds = new google.maps.LatLngBounds();
              places.forEach(place => {
                if (!place.geometry) {
                  console.log("Returned place contains no geometry");
                  return;
                }
                
                const icon = {
                  url: place.icon,
                  size: new google.maps.Size(71, 71),
                  origin: new google.maps.Point(0, 0),
                  anchor: new google.maps.Point(17, 34),
                  scaledSize: new google.maps.Size(25, 25)
                }; // Create a marker for each place.
    
                markers.push(
                  new google.maps.Marker({
                    map,
                    icon,
                    title: place.name,
                    position: place.geometry.location
                  })
                );
    
                if (place.geometry.viewport) {
                  // Only geocodes have viewport.
                  bounds.union(place.geometry.viewport);
                } else {
                  bounds.extend(place.geometry.location);
                }
              });
              map.fitBounds(bounds);
    
            });
    
    
    
            //  // Create the initial InfoWindow.
            // var infoWindow = new google.maps.InfoWindow(
            //     {content: 'Click the map to get Lat/Lng!', position: myLatlng});
            // //  const service = new google.maps.places.PlacesService(map);
            // infoWindow.open(map);
    
            // //Configure the click listener.
            // map.addListener('click', function(mapsMouseEvent) {
            // //   // Close the current InfoWindow.
            //   infoWindow.close();
    
            // //   // Create a new InfoWindow.
            //   infoWindow = new google.maps.InfoWindow({position: mapsMouseEvent.latLng});
            //   infoWindow.setContent(mapsMouseEvent.latLng.toString());
            //   infoWindow.open(map);
            //   console.log(mapsMouseEvent.toString())
            //   user_location = mapsMouseEvent.latLng.toString();
            //   user_location = user_location.replace(/[()]/g, '').split(',');
            // });
    
             new ClickEventHandler(map, origin);
             }
    
             liveDelivery();
           
    }
    
    function liveDelivery(){
      if(document.getElementById("live_map") !== null){
    //     setTimeout(function() {
    //   location.reload();
    // }, 5000);
    
        var order_url = window.location.href;
        var order_id = order_url.substring(order_url.lastIndexOf('/') + 1, order_url.lastIndexOf('?'));
        // var token = order_url.substring(order_url.lastIndexOf('?')+1);
        // var get_url  = `http://localhost:8069/delivery/orders/${order_id}?${token}`;
        // console.log(order_id,token,get_url)
        // fetch(get_url)
        //    .then(function(response){
        //       return response.json();
        //    }).then(function(text){
        //     console.log(text.name)
        //    });
    // var result =[
    //           {'id':1,'name':"clinton","address":"Bagamoyo Rd Dar es Salaam","lat":-6.765042,"long":39.229990},
    //           {'id':2,'name':"richard","address":"Morogoro Road Dar es Salaam","lat":-6.790646,"long":39.197649},
    //           {'id':4,'name':"richardclinton","address":"Mbweni T TCL Dar JKT,Dar es Salaam","lat":-6.608019,"long":39.163545},
    //           {'id':3,'name':"joseph","address":"249 Morroco Rd Dar es Salaam","lat":-6.791562,"long":39.264124},
    //           ];
    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer();
    var drivers;
    var base_url = window.location.origin;
    console.log(base_url)
    fetch(`${base_url}/location?order_id=${order_id }`)
            .then(function(response){
              return response.json();
            }).then(function(text){
              if(text.length == 0){
                document.getElementById("live_map").style.height="30px"
                 document.getElementById("live_map").innerHTML="<div class='text-center' style='font-size: 20px;font-weight:bold'>Your delivery will start soon, Please wait...</div>"
              }else{
    var myLatlng = {lat:text[0]['customer']['partner_latitude'],lng:text[0]['customer']['partner_longitude']};
    var map = new google.maps.Map(document.getElementById("live_map"),{
       center: myLatlng,
              zoom: 7,
     });
    directionsRenderer.setMap(map);
     directionsService.route(
          {
            origin: new google.maps.LatLng(text[0]['driver']['latitude'],text[0]['driver']['longitude']),
            destination:new google.maps.LatLng(text[0]['customer']['partner_latitude'],text[0]['customer']['partner_longitude']),
            travelMode: google.maps.TravelMode.DRIVING
          }, (response, status) => {
                if (status === "OK") {
                  directionsRenderer.setDirections(response);
                } else {
                  window.alert("Directions request failed due to " + status);
                }
              }
      );
            // for(var i = 0; i < text.length; i++){
            //   var driver_no = Object.keys(text[1]).length;
            //   drivers = text[1];
            //   console.log(driver_no)
              // console.log(text[0]['customer']['name'],text[0]['customer']['partner_latitude'],text[0]['customer']['partner_longitude'])
    // var marker = new google.maps.Marker({
    // map: map,
    // position: new google.maps.LatLng(text[0]['customer']['partner_latitude'],text[0]['customer']['partner_longitude']),
    // title:text[0]['customer']['street']
    // });
            // }
          }
            });
        //     .then(function(){
        // console.log(drivers)
        //     })     
    // for(var i = 0; i < result.length; i++){
    // var marker = new google.maps.Marker({
    // map: map,
    // position: new google.maps.LatLng(result[i]['lat'],result[i]['long']),
    // title:result[i]['address']
    // });
    // }
    }
    }
    
    
    
    function isIconMouseEvent(e) {
      return "placeId" in e;
    }
    class ClickEventHandler {
      constructor(map, origin) {
        // this.origin = origin;
        this.map = map;
        // this.directionsService = new google.maps.DirectionsService();
        // this.directionsRenderer = new google.maps.DirectionsRenderer();
        // this.directionsRenderer.setMap(map);
        this.placesService = new google.maps.places.PlacesService(map);
        this.infowindow = new google.maps.InfoWindow();
        this.infowindowContent = document.getElementById("infowindow-content");
        this.infowindow.setContent(this.infowindowContent);
        // Listen for clicks on the map.
        this.map.addListener("click", this.handleClick.bind(this));
      }
      handleClick(event) {
        console.log("You clicked on: " + event.latLng);
          user_location = event.latLng.toString();
          user_location = user_location.replace(/[()]/g, '').split(',');
        // If the event has a placeId, use it.
        if (isIconMouseEvent(event)) {
          console.log("You clicked on place:" + event.placeId);
          // Calling e.stop() on the event prevents the default info window from
          // showing.
          // If you call stop here when there is no placeId you will prevent some
          // other map click event handlers from receiving the event.
          event.stop();
          // this.calculateAndDisplayRoute(event.placeId);
          this.getPlaceInformation(event.placeId);
        }
      }
       getPlaceInformation(placeId) {
        const me = this;
        this.placesService.getDetails({ placeId: placeId }, (place, status) => {
          if (status === "OK") {
            me.infowindow.close();
            me.infowindow.setPosition(place.geometry.location);
            me.infowindowContent.children["place-icon"].src = place.icon;
            me.infowindowContent.children["place-name"].textContent = place.name;
            // me.infowindowContent.children["place-id"].textContent = place.place_id;
            me.infowindowContent.children["place-address"].textContent =
              place.formatted_address;
            me.infowindow.open(me.map);
          }
          document.getElementById("map_search").value = place.name + "," +place.formatted_address;
        });
      }
    }
    const googleMapsScript = document.createElement('script');
    googleMapsScript.src = "http://maps.googleapis.com/maps/api/js?key=AIzaSyCdomGxOD4t7VPHQ7ZHidPLZXo7bYswAr4&callback=initMap&libraries=places&v=weekly";
    document.head.appendChild(googleMapsScript)
    
    function saveInfo(){
     document.getElementById('lat').value = user_location[0];
     document.getElementById('long').value = user_location[1];
     var address = document.getElementById("map_search").value
     document.getElementById("street").value = address
     $("#showmap").modal('hide');
    }
    
    function custom_form_get_order(e){
      console.log("clinton")
    }
    // API_KEYS = "AIzaSyCdomGxOD4t7VPHQ7ZHidPLZXo7bYswAr4";
    
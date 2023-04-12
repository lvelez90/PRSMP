// Import and register all your controllers from the importmap under controllers/*

import { application } from "controllers/application"

// Eager load all controllers defined in the import map under controllers/**/*_controller
import { eagerLoadControllersFrom } from "@hotwired/stimulus-loading"
eagerLoadControllersFrom("controllers", application)

// Lazy load controllers as they appear in the DOM (remember not to preload controllers in import map!)
// import { lazyLoadControllersFrom } from "@hotwired/stimulus-loading"
// lazyLoadControllersFrom("controllers", application)

// initialize the map
var map = L.map('mapid').setView([18.2208, -66.5901], 10);

// add the Esri satellite image basemap layer
L.esri.basemapLayer('Imagery').addTo(map);

// add a marker to the center of the map
L.marker([18.2208, -66.5901]).addTo(map);


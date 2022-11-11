// window.$ = window.jquery = require('./node_modules/jquery');
// window.dt = require('./node_modules/datatables.net')();
// window.$('#myTable').DataTable();

var $       = require( 'jquery' );
var dt      = require( 'datatables.net' )( window, $ );
var buttons = require( 'datatables.net-buttons' )( window, $ );
<?php 

$python_env = "/usr/bin/python3";
header('Content-Type: application/json');

/*if(isset($_GET['latitude']) && 
		isset($_GET['longitude']) && 
		isset($_GET['heading']) && 
		isset($_GET['sog']) && 
		isset($_GET['basic_class']) &&
		isset($_GET['date']))*/
//{
	$lat = isset($_GET['latitude']) ? $_GET['latitude'] : 37.23098;
	$lng = isset($_GET['longitude']) ? $_GET['longitude'] : 12.68286;
	$heading = isset($_GET['heading']) ? $_GET['heading'] : 46;
	$sog = isset($_GET['sog']) ? $_GET['sog'] : 13;
	$bc = isset($_GET['basic_class']) ? $_GET['basic_class'] : 1; 
	$mydate = isset($_GET['date']) ? str_replace("T", " ", $_GET['date']) : '2021-10-27 12:33:10';
	$output = "";
	exec("$python_env ../CLI/predict.py -l $lat -n $lng -c $heading -s $sog -b $bc -t $mydate", $output);
	echo $output[0];
//}

//else
//	echo "Parameters: latitude, longitude, sog, heading, basic_class, date, timestamp";
?>
<?php 

$python_env = "/usr/bin/python3";
header('Content-Type: application/json');

if(isset($_GET['latitude']) && 
		isset($_GET['longitude']) && 
		isset($_GET['heading']) && 
		isset($_GET['sog']) && 
		isset($_GET['basic_class']) &&
		isset($_GET['date']))
{
	$lat = $_GET['latitude'];
	$lng = $_GET['longitude'];
	$heading = $_GET['heading'];
	$sog = $_GET['sog'];
	$bc = $_GET['basic_class']; 
	$mydate = str_replace("T", " ", $_GET['date']);
	$output = "";
	exec("$python_env ../CLI/predict.py -l $lat -n $lng -c $heading -s $sog -b $bc -t $mydate", $output);
	echo $output[0];
}
else if (isset($_GET['record_id']))
{
	$output = "";
	$record_id = $_GET['record_id'];
	exec("$python_env predict.py record_id -r $record_id", $output);
	echo $output[0];
}
else
	echo "Parameters: latitude, longitude, sog, heading, basic_class, date, timestamp";
?>
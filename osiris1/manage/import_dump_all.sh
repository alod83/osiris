#!/bin/bash

echo "* * * * * Import Dump * * * * *"

user="postgres"
export PGPASSWORD='osiProj16'
db_name="dati_ais_with_ts"

echo "Removing duplicates"
psql -U postgres <<EOF
\connect $db_name
CREATE TABLE satellite_ais_data_clean AS (SELECT * FROM satellite_ais_data WHERE 1 = 2);
CREATE TABLE satellite_srp_dataset AS (SELECT * FROM satellite_ais_data_clean WHERE 1 = 2);
CREATE INDEX "mmsi_dateTime" ON satellite_ais_data_clean USING btree (date_time, mmsi);
CREATE INDEX "mmsi_dateTime" ON satellite_srp_dataset USING btree (date_time, mmsi);
INSERT INTO satellite_ais_data_clean SELECT DISTINCT date_time,mmsi,course,speed,heading,imo,ship_name,callsign,ship_type,a,b,c,d,draught,destination,eta,navigation_status,geom FROM satellite_ais_data;
INSERT INTO satellite_srp_dataset SELECT DISTINCT date_time,mmsi,course,speed,heading,imo,ship_name,callsign,ship_type,a,b,c,d,draught,destination,eta,navigation_status,geom FROM satellite_ais_data_clean WHERE heading >= 0 and heading <= 359 and speed >= 0.5 and speed <= 60;

EOF
echo "Done"

#echo "Starting setup"
#start_time=$(psql -U postgres -q -t -d $db_name <<EOF
#SELECT min(date_time) FROM srp_dataset;
#EOF
#)
#end_time=$(psql -U postgres -q -t -d $db_name <<EOF
#SELECT max(date_time) FROM srp_dataset;
#EOF
#)
#python /home/angelica/Git/osiris/knn/setup.py -s $start_time -e $end_time -b 1
#echo "Done"

#echo "Running training"
#nr=$(psql -U postgres -q -t -d $db_name <<EOF
#SELECT max(record_id) FROM srp_dataset;
#EOF
#)

#echo "KNN"
#python /home/angelica/Git/osiris/knn/train.py -a knn -n $nr 
#cp /home/angelica/Git/osiris/knn/data/*knn* /var/www/html/srp/data/
#echo "Done"

#echo "Getting classes"
#python /home/angelica/Git/osiris/knn/get_classes.py -n $nr
#cp /home/angelica/Git/osiris/knn/classes.csv /var/www/html/srp_viewer/dump/
#echo "Done"


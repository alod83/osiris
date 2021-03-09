#!/bin/bash

# leggere da linea di comando la data e l'id
OPTIND=1         # Reset in case getopts has been used previously in the shell.

# Initialize our own variables:
mydate="2017-10-16"
ID="prova"
while getopts "h?i:d:" opt; do
    case "$opt" in
    h|\?)
        echo "usage run_predict.sh -i folder_id -d folder_date"
        exit 0
        ;;
    i)  ID=$OPTARG
        ;;
    d)  mydate=$OPTARG
        ;;
    esac
done

declare -A modules

# correggere il percorso
#data_dir="/data/OSIRIS_REPOSITORY/"$mydate"/"$ID"/"
data_dir="/data/owncloud/Shared/OSIRIS_REPOSITORY/"$mydate"/"$ID"/"
#data_dir="/data/OSIRIS_REPOSITORY/"$mydate"/"$ID"/"
module_dir="/home/angelica/Git/osiris/srp"

# TODO check whether my file .done exists in this case exit
#srp_done=$data_dir"SRP/SRP.done"
#if [ -f "$srp_done" ];
#then
#	echo "Data already processed"
#	exit 1
#fi

declare -a modules_name=("detection" "classification" "kinematic", "metadata")
declare -A modules[detection]
modules[detection,name]="SD"
modules[detection,filepath]="SD/detection.csv"
declare modules[detection,fields]
modules[detection,fields,0]='SdI'
modules[detection,fields,1]='SClat'
modules[detection,fields,2]='SClon'
modules[detection,fields,3]='SL'
modules[detection,fields,4]='SW'
modules[detection,fields,5]='SH'


declare -A modules[classification]
modules[detection,classification]="SC"
modules[classification,filepath]="SC/classification.csv"
declare modules[classification,fields]
modules[classification,fields,0]='SdI'
modules[classification,fields,1]='SC'	# Ship class
modules[classification,fields,2]='ST'	# Ship type
modules[classification,fields,3]='SFL'	# Ship type
modules[classification,fields,4]='SFW'	# Ship type
modules[classification,fields,5]='HDAM'	# Ship type
modules[classification,fields,6]='SFH'	# Ship fine heading

declare -A modules[kinematic]
modules[kinematic,name]="SKE"
modules[kinematic,filepath]="SKE/kinematic.csv"
declare modules[kinematic,fields]
modules[kinematic,fields,0]='SdI'
modules[kinematic,fields,1]='SSA'		# Ship speed amplitude
modules[kinematic,fields,2]='SSO'

declare -A modules[metadata]
modules[metadata,name]="DPP"
modules[metadata,filepath]="DPP/metadata.csv"
declare modules[metadata,fields]
date_index=5
hour_index=6
#modules[metadata,fields,0]='ID'
#modules[metadata,fields,1]='URIa'
#modules[metadata,fields,2]='URIp'
#modules[metadata,fields,3]='SAT'
#modules[metadata,fields,4]='OP'
#modules[metadata,fields,5]='SST' # starting time of acquisition
# omitting other fields

# Retrieve input data

declare -A features
declare SdI_list

timestamp="null"
for module in "${modules_name[@]}"
do
	
	filename=$data_dir${modules[$module,filepath]}
	
	count=1
	echo $module
	while read line; do
		#declare -A features
		# skip first line
		
		if [ $count -gt 1 ]
  		then
  			arr_line=(${line//,/ })
  			#IFS=',' read -r -a arr_line <<< $line
  			SdI=${arr_line[0]}
  			#echo $SdI
			
			if [ "$module" == "detection" ]; then
				declare -A features[$SdI]
				SdI_list+=($SdI)
			fi
			
			if [ "$module" == "metadata" ]; then
				cdate=${arr_line[$date_index]} 
				chour=${arr_line[$hour_index]}
				timestamp="$cdate $chour"
			else
  				fields_array=${modules[$module,fields]}
  				for index in ${!arr_line[@]}; do
  					class="big"
  					if [ "$module" == "classification" ] && [ "$index" == 1 ]; then
  						#echo ${arr_line[$index]}
  						class=${arr_line[$index]}
  						if [ "$class" == "big" ]; then
  							class="1"
  						else
  							class="0"
  						fi
  						features[$SdI,${modules[$module,fields,$index]}]=$class
  					else
    					features[$SdI,${modules[$module,fields,$index]}]=${arr_line[$index]}
    				fi
    				#echo $features[$SdI,${modules[$module,fields,$index]}]
				done
			fi
  		fi
  		count=$((count + 1))
  		
	done <$filename
done


# prepare output file
output_file=$data_dir"SRP/route_prediction.json"
tmp_output_file="/data/SRP/route_prediction.json"
echo '{"type": "FeatureCollection", "features": [' > $tmp_output_file
number_of_effective_SdI=0
# run predict for each SdI
for i in "${SdI_list[@]}"
do
	
  	#echo "{" >> $output_file
  	
  	lat=${features[$i,'SClat']}
  	
  	lng=${features[$i,'SClon']}
  	sog=${features[$i,'SSA']}
  	cog=${features[$i,'SSO']}
  	bclass=${features[$i,'SC']}
  	use_sfh=false
  	if [ -z "$cog" ];
  	then
  		cog=${features[$i,'SFH']}
  		use_sfh=true
  	fi
  	if [ ! -z "$lat" ] && [ ! -z "$lng" ] && [ ! -z "$sog" ] && [ ! -z "$cog" ] && [ ! -z "$bclass" ] && [ "$sog" != "null" ] && [ "$cog" != "null" ] && [ ! "$timestamp" != "null" ]; then
  		#if [ "$i" != "${SdI_list[0]}" ];
  		#then
  		#	echo "," >> $output_file
  		#fi
  		number_of_effective_SdI=$((number_of_effective_SdI + 1))
  		python $module_dir/predict.py -i ${features[$i,'SdI']} -o $tmp_output_file -f features -l $lat -n $lng -c $cog -s $sog -b $bclass -t $timestamp
		h_dam=${features[$i,'HDAM']}
		if [ "$h_dam" = "true" ] && [ "$use_sfh" = "true" ]; then
			cog=$(((cog + 180)%360))
			echo "," >> $output_file
			python $module_dir/predict.py  -i ${features[$i,'SdI']} -o $tmp_output_file -f features -l $lat -n $lng -c $cog -s $sog -b $bclass -t $timestamp
		fi
	fi
	#echo "}" >> $output_file
	#len=$((${#SdI_list[@]}))
	if [ "$i" -lt "$number_of_effective_SdI" ]; then
		echo "," >> $tmp_output_file
	fi
done
echo "]}" >> $tmp_output_file
mv $tmp_output_file $output_file


  		
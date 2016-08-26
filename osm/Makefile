osm_uk_museums_galleries.csv : osm_uk_museums_galleries_filtered.jsonl
	echo 'lon,lat,type,name,website' > $@ && jq -c '[(if .geometry.type == "Point" then .geometry.coordinates else .geometry.coordinates[0] end)[], .properties.tourism, .properties.name, .properties.website] | @csv' $< -r >> $@

osm_uk_museums_galleries_filtered.jsonl : osm_uk_museums_galleries.geojson
	jq -c '.features[] | select(.properties != {})' $< > $@

osm_uk_museums_galleries.geojson :
	overpass --timeout 5000 '(node["tourism"~"gallery|museum"](49.16,-13.41,60.86,1.77);way["tourism"~"gallery|museum"](49.16,-13.41,60.86,1.77);>;relation["tourism"="gallery|museum"](49.16,-13.41,60.86,1.77);>;)' --responseformat "geojson" > $@


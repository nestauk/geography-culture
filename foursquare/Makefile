SHELL := /bin/bash

foursquare_out_with_dates.csv: foursquare_out_subset.csv
	< foursquare_out_subset.csv cols -c createdAt python convert_date.py | csvcut -c 2-7,1 > $@

foursquare_out_subset.csv : foursquare_out.csv
	paste -d ',' <(python2 csvquote.py culture24musandgal_utf8.csv | csvcut -c 1,2) <(cat foursquare_out.csv) > $@
 
foursquare_out.csv : foursquare_out.jsonl
	jq -c '.response.venue | {name: .name, url: .url, lat: .location.lat, lng: .location.lng, checkinsCount: .stats.checkinsCount, createdAt: .createdAt}' foursquare_out.jsonl | in2csv --format ndjson > foursquare_out.csv

foursquare_out.jsonl : culture24musandgal_utf8.csv
	cat $< | csvcut -c 2,8,7 | tail -n +2 | python3 crawl.py > $@

culture24musandgal_utf8.csv: culture24musandgal.csv
	csvformat -e 'latin8' $< > $@


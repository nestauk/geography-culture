foursquare_out.jsonl : culture24musandgal_utf8.csv
	cat $< | csvcut -c 2,8,7 | tail -n +2 | python3 crawl.py > $@

culture24musandgal_utf8.csv: culture24musandgal.csv
	csvformat -e 'latin8' $< > $@

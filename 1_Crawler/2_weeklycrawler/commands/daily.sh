#bin/bash
cd ~/Documents/SMM/1_Crawler/2_weeklycrawler/
command=(scrapy\ crawl\ guardianauto\ -a\ today=$(date +%Y-%m-%d))
eval $command
command=(scrapy\ crawl\ independentauto\ -a\ today=$(date +%Y-%m-%d))
eval $command

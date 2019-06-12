
lcount=$(wc -l $@ | cut -d ' ' -f 1)

while [[ $lcount > 0 ]]; do

command=$(head -n 1 $@)
command="$(echo -e "${command}" | sed -e 's/[[:space:]]*$//')"
echo $command

eval $command
echo -e $command'\n' >> completed.txt
sed -i "1d" $@

sleep 1200
lcount=$(wc -l $@ | cut -d ' ' -f 1)

done



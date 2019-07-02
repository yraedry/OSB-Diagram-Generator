#!/usr/bin/env bash

if [[ -f services.txt ]];
then
    rm -rf services.txt
fi
for i in {1..10};
do
    curl -s -u GBANUN1:d37fa52d22323dade1516139af593cb103e1f870 -X GET https://api.github.com/orgs/AtradiusGroup/repos\?page\=$i | grep -i full_name | grep -i Cibt- |cut -d'/' -f 2 | sed 's/",//' >>  ../Files/services.txt
done
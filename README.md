# Introduction
This docker container was a personal idea to setup a netcup ddns python project. In Summary it allows you to update a dns record to point to you public ip. 
This can than be used to connect via vpn to you home system

# Depdencies 
docker or kubernetes 

# Usage Docker example 

## Manual 
docker run --rm -e CUSTOMER_NUMBER=<your_customer_number> -e API_KEY=<your_api_key> -e API_PASSWORD=<your_api_password> -e DOMAIN=<your_domain> -e RECORD_NAME=<your_vpn_subdomain> ghcr.io/alb-dev/netcup-ddns:latest 

## Run as cron 
* */5 * * * docker run --rm -e CUSTOMER_NUMBER=<your_customer_number> -e API_KEY=<your_api_key> -e API_PASSWORD=<your_api_password> -e DOMAIN=<your_domain> -e RECORD_NAME=<your_vpn_subdomain> ghcr.io/alb-dev/netcup-ddns:latest 

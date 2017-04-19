#!/bin/bash

KEY=$(mktemp key.XXXXXX)
CRT=$(mktemp crt.XXXXXX)

cleanup() {
    rm -f "${KEY}" "${CRT}"
}

trap cleanup EXIT

openssl req \
       -subj "/C=XX/ST=XX/L=XXXX/O=XXXXX/CN=tmpserv" \
       -newkey rsa:2048 -nodes -keyout "${KEY}" \
       -x509 -days 365 -out "${CRT}"

echo;echo;echo
echo "--------------------------------------------------"
echo "Starting up, use the following command to connect:"
echo "   openssl s_client -connect <your-host>:4433"
echo "Hit ctrl-c to exit"
echo "--------------------------------------------------"
echo;echo;echo

openssl s_server -cert "${CRT}" -key "${KEY}"

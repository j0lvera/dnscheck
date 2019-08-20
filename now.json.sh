#!/bin/bash
set -e

strings=(
  arn1
  bom1
  bru1
  cdg1
  #  chs1
  #  cle1
  #  dub1
  #  gru1
  #  hel1
  #  hkg1
  #  hnd1
  #  iad1
  #  icn1
  #  lax1
  #  lhr1
  #  pdx1
  #  sfo1
  #  sin1
  #  syd1
  #  tpe1
  #  yul1
  #  zrh1
)

for i in "${strings[0]}"; do
  JSON=$(
    cat <<-EOF
{
  "version": 2,
  "name": "$i-dnscheck.now.sh",
  "alias": "$i-dnscheck.now.sh",
  "regions": ["$i"],
  "routes": [
    { "src": "./*", "dest": "/" }
  ],
  "builds": [
    { "src": "index.py", "use": "@now/python" }
  ]
}
EOF
  )

  # Generate configuration files
  echo "$JSON" >now.region."$i".json
done

#! /bin/bash
set -e

# Render the pug files
python3 scripts/render.py Seminars.csv

# Pug rendering
node_modules/.bin/pug --doctype html --pretty layout/index.pug --out .
npx pug --doctype html --pretty layout/index.pug --out .

# Remove temporary pug files
rm layout/past.pug
rm layout/upcoming.pug
rm layout/next.pug

# Move to folder
rm -rf www/*
cp -r static/* www/
mv index.html www/index.html

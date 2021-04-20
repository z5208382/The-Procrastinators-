#!/bin/sh
rm -r prebundle
npm run-scripts build
mv build prebundle

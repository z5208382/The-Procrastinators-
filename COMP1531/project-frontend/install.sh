#!/bin/sh
if [ -d '/home/cs1531/public_html/20T1/.npm' ]
then
  echo "prefix=/import/kamen/3/cs1531/public_html/20T1/.npm" > .npmrc
fi
npm install
npm link @date-io/moment
npm link @material-ui/core
npm link @material-ui/styles
npm link @material-ui/icons
npm link @material-ui/pickers
npm link @mdi/js
npm link @mdi/react
npm link axios
npm link cors
npm link epoch-timeago
npm link express
npm link moment
npm link querystring
npm link react
npm link react-dom
npm link react-router-dom
npm link lodash
npm link react-toastify
npm link qs

#!/bin/bash

npm install;

if [ $USE_DEV_MODE = "true" ];
  then
    npm run start;
  else
    npm run build;
    node server $WEB_PORT;
fi
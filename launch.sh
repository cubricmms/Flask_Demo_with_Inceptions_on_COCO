#!/bin/sh

docker-compose build --build-arg model_url="http://download.tensorflow.org/models/object_detection/ssd_inception_v2_coco_2018_01_28.tar.gz"
docker-compose exec web flask db upgrade
docker-compose up

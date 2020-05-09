#!/bin/sh


docker-compose exec web flask db upgrade

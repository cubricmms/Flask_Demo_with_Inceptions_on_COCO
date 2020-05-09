<h1 align="center">
  <a href="https://github.com/cubricmms/Flask_Demo_with_Inceptions_on_COCO" title="Flask Demo Documentation">
    <img src="https://github.com/cubricmms/Flask_Demo_with_Inceptions_on_COCO/blob/master/pg/app/static/lens.png?raw=true" width="200px" height="200px" />
  </a>
  <br />
  Flask And TensorFlow Serving using Docker
</h1>

<p align="center">
  The project is a Flask backend serving objection detection apis provided from TensorFlow serving. Both are deployed using Docker. A live demo can be found at <a href="http://68.183.188.102:5000">DigitalOcean</a>.
</p>

<br />

## Project Overview

**Flask And Tensorflow Serving using Docker** is using [**Flask**](https://flask.palletsprojects.com/en/1.1.x/) as backend server, [**PostgreSQL**](https://www.postgresql.org) as database, [**TensorFlow Serving**](https://www.tensorflow.org/tfx/serving/docker) as image detection service.

The project is replying on [**SQLAlchemy**](https://www.sqlalchemy.org) and [**Flask-Migrate**](https://flask-migrate.readthedocs.io/en/latest/) to manage tables.

[**Flask-Uploads**](https://pythonhosted.org/Flask-Uploads/) and [**Flask-Dropzone**](https://flask-dropzone.readthedocs.io/en/latest/) are used for handling image uploads. And the Flask-Uploads manages image datastore while Flask-Dropzone handling frontend js.

[**Flask-Login**](https://flask-login.readthedocs.io/en/latest/) is for user registration, login and logout, and api authorizations. Currently functions like email confirmations are not implemented in this demo.

The model of tensorflow serving can be found in this Github Repository [Model Zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md). The model picked for this demo is **ssd_inception_v2_coco**. 

For any other models in the model zoo repository or your own trained, change the build args in `launch.sh`, like `docker-compose build --build-arg model_url="http://download.tensorflow.org/models/object_detection/ssd_inception_v2_coco_2018_01_28.tar.gz"` 
## Prerequisite
#### Running Directly
For running demo without Docker, you need Python 3.6 or later and PostgreSQL database set up accordingly. To setup Tensorflow Serving, you can find more details at this <a href="https://medium.com/@pierrepaci/deploy-tensorflow-object-detection-model-in-less-than-5-minutes-604e6bb0bb04">Medium</a> post.

Install dependencies listed in the requirements by `pip install -r requirements.txt`. Inside the app folder, execute `Flask db upgrade` and `Flask run` or `python run.py`. After defining environment variables needed for configuration, you should be able to see a Flask instance up and running.

#### Running using Docker
If you are running demo with Docker (recommended), you can clone this project and do the following:
```bash
$ cd Flask_Demo_with_Inceptions_on_COCO/
$ sh launch.sh
```
In another terminal tab, initialize database on the first time:
```bash
$ cd Flask_Demo_with_Inceptions_on_COCO/
$ sh init_db.sh
```

Another note: Please change demo > pg > configuration.py
`UPLOADS_DEFAULT_URL = 'http://<your ip address>:5000/static/img/'`. Ex. On you local machine, replace the ip address with `localhost`. Same for `UPLOADED_PHOTOS_URL`.


## Contact

If you have any questions, feel free to raise an issues.
Good luck!


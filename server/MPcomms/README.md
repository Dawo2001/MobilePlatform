# MPcomms
Python library for communication over Wi-Fi

# Project dependencies

## [NGINX](https://nginx.org/en/) server:

*Installation*:

Download preffered version from nginx download [site](https://nginx.org/en/download.html).

Download nginx rtmp module from github repository at https://github.com/sergey-dryabzhinsky/nginx-rtmp-module/archive/refs/heads/dev.zip .

Unpack both files. For current stable nginx version (at the time of writing this) it should look like:
```{bash}
$ tar -zxvf nginx-1.20.2.tar.gz
$ unzip dev.zip
```
Finally install nginx using following commands:
```{bash}
$ cd nginx-1.20.2
$ ./configure --with-http_ssl_module --add-module=../nginx-rtmp-module-dev
$ make
$ sudo make install
```

After installing nginx you can apply nginx configuration using following script:
```{bash}
$ ./MPcomms/nginx-settings/apply_settings.sh
```

Now you should be able to turn nginx server on and off with following scripts:
```{bash}
$ ./MPcomms/start_nginx.sh
$ ./MPcomms/stop_nginx.sh
```

## Python dependencies: 

* **FFmpeg wrapper**:
  
  *Installation*:
  ```
  $ pip3 install ffmpeg-python
  ```
  
  Full documentation can be found at https://kkroening.github.io/ffmpeg-python/#
  
* **[OpenCV](https://opencv.org/)**

  *Installation*:
  ```
  $ sudo apt-get install python3-opencv
  ```
  
  Full documentation can be found at: https://docs.opencv.org/4.5.4/d6/d00/tutorial_py_root.html
  
* **[Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/index.html)**

  *Installation*:
  ```
  $ pip3 install flask-restx
  ```

* **[Waitress](https://docs.pylonsproject.org/projects/waitress/)**

  *Installation*:
  ```
  $ pip3 install waitress
  ```

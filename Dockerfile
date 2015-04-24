FROM alpaca/caffe-cpu
MAINTAINER Adrien Lemaire <lemaire.adrien@gmail.com>


WORKDIR /project
ADD ./bvlc_reference_caffenet.caffemodel.tar.gz /tmp/caffe/models/bvlc_reference_caffenet/

CMD bash

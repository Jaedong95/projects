import torch
import caffemodel2pytorch

model = caffemodel2pytorch.Net(
    prototxt = 'deploy.prototxt',
    weights = 'net_iter_400000.caffemodel',
    caffe_proto = 'https://raw.githubusercontent.com/BVLC/caffe/master/src/caffe/proto/caffe.proto'
)


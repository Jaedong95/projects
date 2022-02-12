import caffe

prototxt_filename = 'tmp.prototxt'
caffemodel_filename = 'c3d_ucfcrime_iter_5.caffemodel'

net = caffe.Net(prototxt_filename, caffemodel_filename, caffe.TEST)

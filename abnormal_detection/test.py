import caffe

net = caffe.Net('train_ucf.prototxt', 'c3d_ucfcrime_iter_5.caffemodel', caffe.TEST)

print(net)

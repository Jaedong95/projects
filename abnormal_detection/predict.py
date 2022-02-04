import numpy as np
import torch
import caffemodel2pytorch
import skimage.io as io

from torch.autograd import Variable
from os.path import join
from glob import glob
from skimage.transform import resize

def get_abnormal_clip(clip_name, verbose=True):
    """
    Loads a clip to be fed to C3D for classification.
    TODO: should I remove mean here?
    
    Parameters
    ----------
    clip_name: str
        the name of the clip (subfolder in 'data').
    verbose: bool
        if True, shows the unrolled clip (default is True).
    Returns
    -------
    Tensor
        a pytorch batch (n, ch, fr, h, w).
    """

    clip = sorted(glob(join('data', clip_name, '*.png')))
    clip = np.array([resize(io.imread(frame), output_shape=(112, 200), preserve_range=True) for frame in clip])
    clip = clip[:, :, 44:44+112, :]  # crop centrally

    if verbose:
        clip_img = np.reshape(clip.transpose(1, 0, 2, 3), (112, 16 * 112, 3))
        io.imshow(clip_img.astype(np.uint8))
        io.show()

    clip = clip.transpose(3, 0, 1, 2)  # ch, fr, h, w
    clip = np.expand_dims(clip, axis=0)  # batch axis
    clip = np.float32(clip)

    return torch.from_numpy(clip)


def read_labels_from_file(filepath):
    """
    Parameters
    ----------
    filepath: str
        the file.
        
    Returns
    -------
    list
        list of sport names.
    """
    with open(filepath, 'r') as f:
        labels = [line.strip() for line in f.readlines()]
    return labels


def main():
    """
    Main function.
    """

    # load a clip to be predicted
    X = get_abnormal_clip('roger')
    X = Variable(X)
    X = X.cuda()

    # get network pretrained model
    net = caffemodel2pytorch.Net(
        prototxt = 'train_ucf.prototxt',
        weights = 'c3d_ucfcrime_iter_5.caffemodel',
        caffe_proto = 'https://raw.githubusercontent.com/BVLC/caffe/master/src/caffe/proto/caffe.proto'
    )

    net.cuda()
    net.eval()
    torch.set_grad_enabled(False)

    # perform prediction
    prediction = net(X)
    prediction = prediction.data.cpu().numpy()

    # read labels
    labels = read_labels_from_file('labels.txt')

    # print top predictions
    top_inds = prediction[0].argsort()[::-1][:1]  # reverse sort and take five largest items
    print('\nTop 1:')
    for i in top_inds:
        print('{:.5f} {}'.format(prediction[0][i], labels[i]))


# entry point
if __name__ == '__main__':
    main()

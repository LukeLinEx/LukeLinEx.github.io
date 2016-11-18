import numpy as np
import tensorflow as tf
from sklearn import datasets
import time
import matplotlib.pyplot as plt
from six.moves import cPickle as pickle

__author__ = 'LukeLin'

def weight_variable(shape, stddev):
    initial = tf.truncated_normal(shape, stddev=stddev)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.exp(tf.constant(0., shape=shape))
    return tf.Variable(initial)

def toy_dataset(shuffle = False):
    np.random.seed(0)
    iris = datasets.load_iris()
    x_train = iris.data[:,2:]  # Only use petal length and petal width
    x_train[:,0] = (x_train[:,0]-np.mean(x_train[:,0]))/np.std(x_train[:,0])
    x_train[:,1] = (x_train[:,1]-np.mean(x_train[:,1]))/np.std(x_train[:,1])
    y_train = iris.target

    # shuffle order
    if shuffle:
        idx = np.random.choice(range(150), 150, replace=False)
    else:
        idx = range(150)
    x_train = x_train[idx]
    y_train[y_train==1] = 3
    y_train[y_train==2] = 1
    y_train[y_train==0] = 1
    y_train[y_train==3] = 0
    y_train = np.array( map(lambda x, y:[x,y], y_train==1, y_train==0)  ).astype(int)
    y_train = y_train[idx]
    return x_train, y_train


def main():
    stddev=0.1
    x_train, y_train = toy_dataset()
    steps = 40001
    num_features = 2
    num_classes = 2
    num_hidden = 3
    num_obs = x_train.shape[0]
    sess = tf.InteractiveSession()

    x_train = tf.constant(x_train, dtype=tf.float32)
    y_train = tf.constant(y_train, dtype=tf.int32)
    mu = tf.reduce_mean(x_train, 0)
    sigma = tf.div(tf.matmul(tf.transpose(x_train-mu), x_train-mu),tf.constant(num_obs-1, dtype=tf.float32))
    weight = weight_variable([num_hidden, num_classes], stddev)
    bias = bias_variable([num_classes])

    center = weight_variable([num_hidden, 1, num_features], stddev)
    scale = bias_variable([1])

    inverse_sigma = tf.mul(scale, tf.matrix_inverse(sigma))
    tmp = tf.sub(x_train, center)
    half = tf.einsum('ijk,kl->ijl', tmp, inverse_sigma)
    tmp = tf.reduce_sum(tf.mul(half, tmp), 2)
    tmp = tf.exp(tf.mul(tf.constant(-.5, dtype=tf.float32), tmp))
    mag = tf.pow(tf.constant(2 * np.pi, dtype=tf.float32), tf.constant(-.5*num_features))
    mag = tf.mul(mag, tf.pow( tf.matrix_determinant(inverse_sigma), .5))
    pdf = tf.mul(mag, tf.exp(tmp))
    y_lin = tf.add(tf.einsum('ij,ik->jk', pdf, weight), bias)
    prediction = tf.argmax(y_lin, 1)
    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y_lin, y_train))
    learn_rate = 0.1
    train_step = tf.train.GradientDescentOptimizer(learn_rate).minimize(cross_entropy)

    print 'Start training'
    start = time.time()
    sess.run(tf.initialize_all_variables())
    c1x=[];c2x=[];c3x=[];c4x=[]
    c1y=[];c2y=[];c3y=[];c4y=[]
    plot_steps = steps/40
    for i in range(steps):
        # if i % 100 == 0:
        #     train_accuracy = accuracy.eval(feed_dict={x: x_train, y: y_train})
        #     print("step %d, training accuracy %g" % (i, train_accuracy))
        train_step.run()    #feed_dict={x: x_train, y: y_train})
        if i%200==0:
             #print 'steps %d' % i
             print 'accuracy %.3f at steps %d' % (np.mean( prediction.eval() == np.array([0]*50+[1]*50+[0]*50)), i)
        if i%plot_steps == 0:
            tmp = center.eval().reshape([num_hidden, 2])
            c1x.append(tmp[0][0])
            c2x.append(tmp[1][0])
            # c3x.append(tmp[2][0])
            # c4x.append(tmp[3][0])
            c1y.append(tmp[0][1])
            c2y.append(tmp[1][1])
            # c3y.append(tmp[2][1])
            # c4y.append(tmp[3][1])

    set_filename='Hidden%dlearnRate%.3fStep%dStddev%.3f' %(num_hidden, learn_rate, steps, stddev)
    set_filename = set_filename.replace('.', '_')
    to_save={'x_train': x_train.eval(),
             'y_train':tf.argmax(y_train, 1).eval(),
             'c1x':c1x, 'c2x':c2x, 'c3x':c3x, 'c4x':c4x,
             'c1y':c1y, 'c2y':c2y, 'c3y':c3y, 'c4y':c4y,
             'pdf': pdf.eval(), 'sigma':sigma.eval(),
             'center':center.eval(), 'scale':scale.eval(),
             'magnitude': mag.eval(), 'prediction':prediction.eval()}


    with open(set_filename, 'wb') as f:
        pickle.dump(to_save, f, pickle.HIGHEST_PROTOCOL)

    print time.time() - start
    # co = tf.argmax(y_train, 1).eval()
    # plt.scatter(x_train.eval()[:,0], x_train.eval()[:,1], alpha=0.3, c=co)
    # plt.plot(c1x, c1y, c='b'); plt.scatter(c1x[0], c1y[0], c='b', s =6)
    # plt.plot(c2x, c2y, c='r'); plt.scatter(c2x[0], c2y[0], c='r', s =6)
    # plt.plot(c3x, c3y, c='g'); plt.scatter(c3x[0], c3y[0], c='g', s =6)
    # plt.plot(c4x, c4y, c='y'); plt.scatter(c4x[0], c4y[0], c='y', s =6)

    # plt.savefig(set_filename+'.png')



if __name__ =='__main__':
    main()

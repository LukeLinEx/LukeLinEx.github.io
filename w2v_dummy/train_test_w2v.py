import re
import os
import math
import time
import tensorflow as tf
import numpy as np
import pandas as pd
from six.moves import cPickle as pickle


def cleansing(s):
    result = s.strip().split(',')
    result = map(lambda x: int(re.search('[0-9]+', x).group()), result)
    return result

def prepare_element(train_data_file, test_data_file):
    A = pd.read_csv(train_data_file)
    B = pd.read_csv(test_data_file)
    data1 = pd.concat([A, B], axis=0)[A.columns]
    loss = data1['loss']
    del A
    del B

    cat_data = cat_encode(data1)
    f = open('w2v_data/better_order.txt', 'r')
    order = f.readlines()
    f.close()
    order = map(cleansing, order)
    return cat_data, loss, order

def generate_batch(batch_size, outer_idx, index):
    batch = np.zeros(shape=(batch_size), dtype=np.int32)
    labels = np.zeros(shape=(batch_size, 1), dtype=np.int32)
    for i in range(batch_size):
        idx = order[index+i][0] + outer_idx
        b_col=order[index+i][1]
        l_col=order[index+i][2]
        batch[i] = cat_data.iloc[idx, b_col]
        labels[i] = cat_data.iloc[idx, l_col]
    return batch, labels


def cat_encode(data):
    data = data.loc[:, map(lambda col: 'cat' in col, data.columns) ]
    data = data.columns.values + data
    a = reduce(lambda prev, col: prev+[prev[-1]+len(set(data[col]))], data, [0])
    shift = np.array(a[:-1], dtype=int)
    
    func_dict = {}
    for col in data:
        unique = sorted(list(set(data[col])))[::-1]
        encode = list(range(len(unique)))
        my_d = dict(zip(unique, encode))
        func_dict[col] = my_d

    data1 = data.copy()
    for col in data:
        data1[col]= map(lambda x: func_dict[col][x], data[col])
    
    return data1+shift


def main(num_steps, print_step):
    batch_size = 1141
    embedding_size = 1139 # Dimension of the embedding vector.
    num_sampled = 520 # Number of negative examples to sample.
    vocabulary_size = max(cat_data.iloc[:,-1])+1
    graph = tf.Graph()
    with graph.as_default(), tf.device('/cpu:0'):

	   # Input data.
	   train_dataset = tf.placeholder(tf.int32, shape=[batch_size])
	   train_labels = tf.placeholder(tf.int32, shape=[batch_size, 1])
  
	   # Variables.
	   embeddings = tf.Variable(
        tf.random_uniform([vocabulary_size, embedding_size], -1.0, 1.0))
	   softmax_weights = tf.Variable(
        tf.truncated_normal([vocabulary_size, embedding_size],
            stddev=1.0 / math.sqrt(embedding_size)))
	   softmax_biases = tf.Variable(tf.zeros([vocabulary_size]))
	   embed = tf.nn.embedding_lookup(embeddings, train_dataset)
	   # Compute the softmax loss, using a sample of the negative labels each time.
	   loss = tf.reduce_mean(
        tf.nn.sampled_softmax_loss(softmax_weights, softmax_biases, embed,
            train_labels, num_sampled, vocabulary_size))
	   optimizer = tf.train.AdagradOptimizer(1.0).minimize(loss)
	   norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keep_dims=True))
	   normalized_embeddings = embeddings / norm


    start = time.time()
    with tf.Session(graph=graph) as session:
        print 'Initialize'
        tf.initialize_all_variables().run()
        for step in xrange(num_steps):
            index_in_order_lst = step % 1356
            index_in_cat_data  = step //1356
            batch_data, batch_labels = generate_batch(batch_size,
                index_in_order_lst,index_in_cat_data)
            feed_dict = {train_dataset : batch_data, train_labels : batch_labels}
            session.run(optimizer, feed_dict=feed_dict)
            all_models = []
            if step % print_step == 0:
                for fname in os.listdir("./embedding_in_progress"):
                   if fname.endswith(".pkl"):
                     encode = re.search('embedding([\d]).pkl', fname).groups()[0]
                     all_models.append(int(encode))
                try:
                   next_code = max(all_models)+1
                except ValueError:
                   next_code = 1
                set_filename = 'embedding_in_progress/embedding'+ str(next_code) + '.pkl'
                with open(set_filename, 'wb') as f:
                   pickle.dump(normalized_embeddings.eval(), f, pickle.HIGHEST_PROTOCOL)           
            if step % 10000 == 0:
                elapse = str(time.time() - start)
                f1= open('monitoring.txt', 'a')
                f1.write('step %d, time:%s\n' % (step, elapse))
                f1.close()
            if step%20 == 0 and step < 1500:
                print 'Good standing\n'

        final_embeddings = normalized_embeddings.eval()
        set_filename = 'w2v_data/result.pkl'
        with open(set_filename, 'wb') as f:
            pickle.dump(final_embeddings, f, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    train_file = 'w2v_data/train.csv'
    test_file  = 'w2v_data/test.csv'
    cat_data, loss, order = prepare_element(train_file, test_file)
    ## ^^^^^^^^^^^^^^^^^^  The variable names cannot be 
    ##                     changed here. They need to be global
    main(num_steps = 2705*1356,  print_step=100000)





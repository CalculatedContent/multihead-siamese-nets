import tensorflow as tf
from layers.basics import linear, dropout, feed_forward, residual


def stacked_multihead_attention(x, num_blocks, num_heads, reuse, use_residual=True):
    num_hiddens = x.get_shape().as_list()[-1]
    with tf.variable_scope('stacked_multihead_attention', reuse=reuse):
        for i in range(num_blocks):
            with tf.variable_scope('multihead_block_{}'.format(i), reuse=reuse):
                x = multihead_attention(x, x, x, num_heads=num_heads, reuse=reuse)
                x = feed_forward(x, num_hiddens=num_hiddens, activation=tf.nn.relu, reuse=reuse)
    return x


def multihead_attention(queries, keys, values, num_units=None, num_heads=8, reuse=True, use_residual=True):
    with tf.variable_scope('multihead-attention', reuse=reuse):
        if num_units is None:
            num_units = queries.get_shape().as_list()[-1]
        Q = linear(queries)
        K = linear(keys)
        V = linear(values)

        Q = tf.concat(tf.split(Q, num_heads, axis=2), axis=0)
        K = tf.concat(tf.split(K, num_heads, axis=2), axis=0)
        V = tf.concat(tf.split(V, num_heads, axis=2), axis=0)

        Q_K_V = scaled_dot_product_attention(Q, K, V)
        Q_K_V = dropout(Q_K_V)
        Q_K_V_ = tf.concat(tf.split(Q_K_V, num_heads, axis=0), axis=2)

        output = feed_forward(Q_K_V_, num_units, reuse=reuse)

        if use_residual:
            output = residual(output, queries, reuse=reuse)
        # output = normalization(output)

    return output


def scaled_dot_product_attention(queries, keys, values, model_size=None, reuse=False):
    if model_size is None:
        model_size = tf.to_float(queries.get_shape().as_list()[-1])

    with tf.variable_scope('scaled_dot_product_attention', reuse=reuse):
        keys_T = tf.transpose(keys, [0, 2, 1])
        Q_K = tf.matmul(queries, keys_T) / tf.sqrt(model_size)
        scaled_dprod_att = tf.matmul(tf.nn.softmax(Q_K), values)
    return scaled_dprod_att


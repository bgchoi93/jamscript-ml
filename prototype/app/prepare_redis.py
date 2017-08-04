import redis


def main():
    rdb = redis.StrictRedis('localhost', 6379, 0, charset="utf-8", decode_responses=True)

    #  define networks
    rdb.sadd('networks', 'ffnn')

    #  define layers
    rdb.zadd('ffnn:layers', 'ffnn:l0', 0, 'ffnn:l1', 1, 'ffnn:l2', 2)

    # LAYER 0: Input layer
    #  define neurons of ffnn:l0
    rdb.hset('ffnn:l0', 'neurons', 'ffnn:l0:neurons')
    rdb.zadd('ffnn:l0:neurons', 'ffnn:l0:n0', 0, 'ffnn:l0:n1', 1)

    # LAYER 1 : Hidden layer
    #  define neurons of ffnn:l1
    rdb.hset('ffnn:l1', 'neurons', 'ffnn:l1:neurons')
    rdb.zadd('ffnn:l1:neurons', 'ffnn:l1:n0', 0, 'ffnn:l1:n1', 1)

    #  neuron ffnn:l1:n0
    ffnn_l1_n0 = {
        'bias': 5.847973346710205,
        'weights': 'ffnn:l1:n0:weights'
    }
    rdb.hmset('ffnn:l1:n0', ffnn_l1_n0)
    rdb.rpush(
        'ffnn:l1:n0:weights',
        -7.406619548797607,
        -0.04010223597288132
    )

    #  neuron ffnn:l1:n1
    ffnn_l1_n1 = {
        'bias': 4.145832061767578,
        'weights': 'ffnn:l1:n1:weights'
    }
    rdb.hmset('ffnn:l1:n1', ffnn_l1_n1)
    rdb.rpush(
        'ffnn:l1:n1:weights',
        0.4036349356174469,
        -7.532534599304199
    )

    # LAYER 2 : Output layer
    # define neurons of ffnn:l2
    rdb.hset('ffnn:l2', 'neurons', 'ffnn:l2:neurons')
    rdb.zadd('ffnn:l2:neurons', 'ffnn:l2:n0', 0, 'ffnn:l2:n1', 1)

    #  neuron ffnn:l2:n0

    #  neuron ffnn:l2:n1

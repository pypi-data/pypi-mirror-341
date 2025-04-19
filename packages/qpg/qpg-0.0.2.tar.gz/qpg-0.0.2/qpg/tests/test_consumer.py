from qpg import PGQueue


def test_consumer():
    pg_q = PGQueue()
    
    for c in pg_q.consume(queue_name="test", source="test"):
        print("consumed message {}".format(c))
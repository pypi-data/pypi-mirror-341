import time

from qpg import PGQueue


def test_producer():
    pg_q = PGQueue()
    
    i=0
    while i<15:
        i+=1
        pg_q.produce(
            source="test_producer",
            queue_name="test",
            message=dict(data=f"test {i}")
        )
        time.sleep(10)
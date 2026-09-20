def test_should_time_out_connections():
    # Given two users
    user1 = new_user()
    user2 = new_user()
    # And an empty connection pool with a 10-minute timeout
    pool = new_pool(timedelta(minutes=10))
    # When connecting both users to the pool
    pool.connect(user1)
    pool.connect(user2)
    # Then the pool should have two connections
    assert len(pool.connections) == 2
    # When waiting for 20 minutes
    clock.advance(timedelta(minutes=20))
    # Then the pool should have no connections
    assert pool.connections == []
    # And each user should be disconnected
    assert not user1.is_connected()
    assert not user2.is_connected()

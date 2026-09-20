@Test
public void shouldTimeOutConnections() {
    // Given two users
    User user1 = newUser();
    User user2 = newUser();
    // And an empty connection pool with a 10-minute timeout
    Pool pool = newPool(Duration.minutes(10));
    // When connecting both users to the pool
    pool.connect(user1);
    pool.connect(user2);
    // Then the pool should have two connections
    assertThat(pool.getConnections()).hasSize(2);
    // When waiting for 20 minutes
    clock.advance(Duration.minutes(20));
    // Then the pool should have no connections
    assertThat(pool.getConnections()).isEmpty();
    // And each user should be disconnected 
    assertThat(user1.isConnected()).isFalse();
    assertThat(user2.isConnected()).isFalse();
}

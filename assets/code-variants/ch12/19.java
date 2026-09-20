Set<String> colors = ImmutableSet.of("red", "green", "blue"); 
assertTrue(colors.contains("orange")); // JUnit 
assertThat(colors).contains("orange"); // Truth

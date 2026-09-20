# A helper method wraps a constructor by defining arbitrary defaults for 
# each of its parameters.
def newContact(
        firstName = "Grace", lastName = "Hopper", phoneNumber = "555-123-4567"):
    return Contact(firstName, lastName, phoneNumber)

# Tests call the helper, specifying values for only the parameters that they
# care about.
def test_fullNameShouldCombineFirstAndLastNames(self):
    def contact = newContact(firstName = "Ada", lastName = "Lovelace") self.assertEqual(contact.fullName(), "Ada Lovelace")

// Languages like Java that don’t support named parameters can emulate them
// by returning a mutable "builder" object that represents the value under
// construction.
private static Contact.Builder newContact() {
    return Contact.newBuilder()
        .setFirstName("Grace")
        .setLastName("Hopper")
        .setPhoneNumber("555-123-4567");
}

// Tests then call methods on the builder to overwrite only the parameters
// that they care about, then call build() to get a real value out of the
// builder. @Test
public void fullNameShouldCombineFirstAndLastNames() {
    Contact contact = newContact()
        .setFirstName("Ada").setLastName("Lovelace")
        .build();
    assertThat(contact.getFullName()).isEqualTo("Ada Lovelace");
}

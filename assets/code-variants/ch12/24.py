# A helper method wraps a constructor by defining arbitrary defaults for
# each of its parameters.
def new_contact(first_name="Grace", last_name="Hopper", phone_number="555-123-4567"):
    return Contact(first_name, last_name, phone_number)

# Tests call the helper, specifying values for only the parameters that they
# care about.
def test_full_name_should_combine_first_and_last_names():
    contact = new_contact(first_name="Ada", last_name="Lovelace")
    assert contact.full_name() == "Ada Lovelace"

# Python supports named parameters, so the mutable "builder" object that Java
# needs for the same purpose is unnecessary here.

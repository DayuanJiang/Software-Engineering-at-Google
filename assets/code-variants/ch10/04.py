def add_customer(name: str, address: str) -> int:
    """Create a new record for a customer with the given name and address.

    Returns the record ID, or raises DuplicateEntryError if a record with that
    name already exists.
    """

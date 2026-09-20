# Python integers have no fixed width, so there is no unsigned shift `>>>`;
# a plain right shift of the (non-negative) value gives the same result.
result = 31 * result + (f ^ (f >> 32))

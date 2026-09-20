// Function that takes a Foo* and may or may not assume ownership of 
// the passed pointer.
void TakeFoo(Foo* arg);
// Calls to the function don’t tell the reader anything about what to 
// expect with regard to ownership after the function returns.
Foo* my_foo(NewFoo());
TakeFoo(my_foo);

// Function that takes a std::unique_ptr<Foo>.
void TakeFoo(std::unique_ptr<Foo> arg);
// Any call to the function explicitly shows that ownership is 
// yielded and the unique_ptr cannot be used after the function 
// returns.
std::unique_ptr<Foo> my_foo(FooFactory()); TakeFoo(std::move(my_foo));

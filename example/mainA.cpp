#include <cstdio>

#define REQUIREMENT

void foo() {
	std::puts("foo");
}

void bar() {
	std::puts("bar");
#ifdef REQUIREMENT
	std::puts("another");
#endif
}

__attribute__((weak)) void weak_baz() {
	std::puts("weak_baz");
}

static int qux = 10;

int main() {
	
	foo();
	bar();
	weak_baz();
	
	return 0;
}
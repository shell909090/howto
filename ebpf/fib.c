#include <stdio.h>

int fib(int n) {
	if (n <= 0) {
		return 0;
	}
	if (n <= 2) {
		return 1;
	}
	return fib(n-1) + fib(n-2);
}

int main() {
	int n = 20;
	printf("fib(%d) = %d\n", n, fib(n));
	return 0;
}

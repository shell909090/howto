#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <mcheck.h>


int comp (const void *ele1, const void *ele2)
{
	long a = *((long*)ele1+1);
	long b = *((long*)ele2+1);
	if (a > b) {
		return 1;
	}
	if (a < b) {
		return -1;
	}
	return 0;
}


int readfile(char *filepath, long *array)
{
	long a, b;
	long idx = 0;
	char line[1024];
	char *tok;
	char *rest;
	FILE *fp;

	fp = fopen(filepath, "r");
	if (fp == NULL) {
		printf("can't read file");
		return -1;
	}

	while(!feof(fp)) {
		if (fgets(line, 1024, fp) == 0){
			break;
		}
		if (*line == '\n') {
			break;
		}
		rest = line;
		tok = strtok_r(rest, " ", &rest);
		a = atol(tok);
		tok = strtok_r(rest, " ", &rest);
		b = atol(tok);
		/* printf("%d %d %d\n", idx, a, b); */
		array[idx] = a;
		array[idx+1] = b;
		idx += 2;
	}
	/* fclose(fp); */

	return 0;
}


int main(int argc, char *argv[])
{
	long *array;

	/* mtrace(); */
	sleep(1);

	array = malloc(sizeof(long) * 2000000);
	if (readfile(argv[1], array) != 0) {
		return -1;
	}

	qsort(array, 1000000, 2*sizeof(long), comp);

	/* free(array); */

	sleep(10);
	return 0;
}

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
	FILE *document = fopen(argv[1], "r");
	char c = fgetc(document);
	int i = 0;
	while (c != EOF){
		printf("%c", c);
		if (c < ' ' || c > '~') {
			printf("%i", c);
			i++;
			if (i%3 == 0) {
				printf("\n\n");
			}
		}
		c = fgetc(document);
	}
	printf("\n\n%i found", i);
	fclose(document);
}
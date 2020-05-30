#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
	FILE *document = fopen(argv[1], "r");
	char c = fgetc(document);
	// int i = 0;
	while (c != EOF){
		
		if (c < ' ' || c > '~') {
			printf("%i ", c);
		}
		// printf("%c", c);
		c = fgetc(document);
	}
	fclose(document);
}
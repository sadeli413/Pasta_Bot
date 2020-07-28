// @author Sadeli
#include <stdio.h>
#include <stdlib.h>

// checks a text file for non-ascii characters
int main(int argc, char *argv[]) {
	// open the file
	FILE *document = fopen(argv[1], "r");
	char c = fgetc(document);
	int i = 0;
	// loop through each character in the file
	while (c != EOF){
		printf("%c", c);
		// if the character is invalid, print out the character
		if (c < ' ' || c > '~') {
			printf("%i", c);
			// since weird characters are printed out in threes, make a new line every three times
			i++;
			if (i%3 == 0) {
				printf("\n\n");
			}
		}
		c = fgetc(document);
	}
	// print the total amount of weird characters
	printf("\n\n%i found\n", i);
	fclose(document);
}

/* reference http://shell-storm.org/shellcode/files/shellcode-827.php */

#include <stdio.h>
#include <string.h>
 
const unsigned char code[];
/* "\xeb\x19\x31\xc0\x31\xdb\x31\xd2\x31\xc9\xb0\x04\xb3\x01\x59\xb2\x05\xcd\x80\x31\xc0\xb0\x01\x31\xdb\xcd\x80\xe8\xe2\xff\xff\xff\x68\x65\x6c\x6c\x6f" */

int main(void) {
	(*(void(*)()) code)();
	return 0;
}
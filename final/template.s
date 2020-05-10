        .file   "template.c"
        .intel_syntax noprefix
        .text
        .globl  handle_errors
        .type   handle_errors, @function
handle_errors:
        {{ handle_errors }}
        .size   handle_errors, .-handle_errors
        .globl  decrypt
        .type   decrypt, @function
decrypt:
        {{ decrypt }}
.L9:
        call    handle_errors
.L10:
        call    handle_errors
.L11:
        call    handle_errors
.L12:
        call    handle_errors
        .size   decrypt, .-decrypt
        .section    .rodata
        .align 4
.LC0:
        .string ""
        .ascii  ""
        .ascii  ""
        .ascii  ""
        .ascii  ""
        .ascii  ""
        .ascii  ""
        .text
        .globl main
        .type  main, @function
main:
        {{ main }}
        .size   main, .-main
        .section    .rodata.str1.1,"aMS",@progbits,1
.LC1:
        .string ""
        .text
        .globl  print_data
        .type   print_data, @function
print_data:
        {{ print_data }}
.L17:
        {{ L17 }}
.L16:
        {{ L16 }}
        .size   print_data, .-print_data
        .section    .rodata
        .align 32
        .type   key.10090, @object
        .size   key.10090, 32
key.10090:
        .string ""
        .ascii  ""
        .section    text.__x86.get_pc_thunk.ax,"axG",@progbits,__x86.get_pc_thunk.ax,comdat
        .globl  __x86.get_pc_thunk.ax
        .hidden __x86.get_pc_thunk.ax
        .type   __x86.get_pc_thunk.ax, @function
__x86.get_pc_thunk.ax:
        mov eax, DWORD PTR [esp]
        ret
        .section    .text.__x86.get_pc_thunk.bx,"axG",@progbits,__x86.get_pc_thunk.bx,comdat
        .globl  __x86.get_pc_thunk.bx
        .hidden __x86.get_pc_thunk.bx
        .type   __x86.get_pc_thunk.bx, @function
__x86.get_pc_thunk.bx:
        mov ebx, DWORD PTR [esp]
        ret
        .ident  "GCC: (Debian 9.2.1-22) 9.2.1 20200104"
        .section    .note.GNU-stack,"",@progbits

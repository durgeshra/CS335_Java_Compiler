section .text
	global printInt1

printInt1:
	mov eax, [esp+4]
	xor esi, esi
	cmp eax, 0
	jge loop
	neg eax
	push eax
	mov eax, 45
	push eax
	mov eax, 4 ; Print '-'
	mov edx, 1
	mov ecx, esp
	mov ebx, 1
	int 0x80
	pop eax
	pop eax

loop:
	mov edx, 0
	mov ebx, 10
	div ebx
	add edx, 48
	push edx
	inc esi
	cmp eax, 0
	jz next
	jmp loop

next:
	cmp  esi, 0
	jz   exit
	dec  esi
	mov  eax, 4
	mov  ecx, esp
	mov  ebx, 1
	mov  edx, 1
	int  0x80
	add  esp, 4
	jmp  next

exit:
	call printNewLine
	ret

printNewLine:
  push ebp
  mov ebp, esp
  sub esp, 4

  ; Print newline
  mov dword [ebp - 4], 0x0a
  mov eax, 4
  mov ebx, 1
  mov ecx, ebp
  sub ecx, 4
  mov edx, 1
  int 80h

  mov esp, ebp
  pop ebp
  ret	

#암호화 가중치
rate = 329

#악질 버전(키릴버전)
inputText = list(input("암호화할 텍스트 입력: "))  #텍스트 입력받기
G = list(map(ord, inputText ))   #아스키코드로 변환

#일반항
def a(G, n):   #n = 0....len(G)-1  a_n 구현
  return G * 2**(n-1) * n

#암호화 해봅시다
code = list(map(a,G,range(1,len(G)+1)))


result = []
quo=[];
for i in range(len(code)):
  result.append(code[i]%304 + 1024)
  quo.append(code[i]//304)

# key = sum(result)
# key += sum(quo)%1024
key = sum(map(lambda x: x * rate, result))
key += sum(map(lambda x: x * rate,quo))%(1024*rate)
result = ''.join(list(map(chr,result)))
quo = list(map(lambda x:x^key,quo))  #xor 수행
quo = list(map(hex,quo))




#LZW압축함수
def lzw_compress(text):
    dictionary = {chr(i+32): i for i in range(95)}  # 초기 딕셔너리 설정
    next_code = 0x7f  # 다음 인덱스 값
    result = []
    s = ""
    for char in text:
        if s + char in dictionary:
            s = s + char
        else:
            result.append(dictionary[s])
            dictionary[s + char] = next_code
            next_code += 1
            s = char
    result.append(dictionary[s])
    return result

compressed = lzw_compress(''.join(quo))
compressed = list(map(lambda x: chr(x+1024),compressed))

compressed = ''.join(compressed)
result += compressed
print(f"key: {key}")
print(f"암호문: {result}")
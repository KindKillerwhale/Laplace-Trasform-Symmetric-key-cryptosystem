#암호화 가중치
rate = 329

#악질 버전(키릴버전)
inputText = list(input("복호화할 텍스트 입력: "))  #텍스트 입력받기
G = list(map(ord, inputText ))   #아스키코드로 변환
key = int(input("키를 입력해주세요 : "))

#remains와 G로 분리
temp = 0
remains = []
temp += G[0] * rate
while temp < key:
  remains.append(G.pop(0))
  temp += G[0] * rate



#각각 1024 빼기
remains = list(map(lambda x:x-1024, remains))
G = list(map(lambda x: x-1024, G))

#압축해제 함수
def lzw_decompress(compressed):
    dictionary = {i:chr(i+32) for i in range(95)}  # 초기 딕셔너리 설정
    next_code =  0x7f  # 다음 인덱스 값
    result = []
    code = compressed[0]
    s = dictionary[code]
    result.append(s)
    i = 1
    while i < len(compressed):
        code = compressed[i]
        i += 1
        if code in dictionary:
            entry = dictionary[code]
        elif code == next_code:
            entry = s + s[0]
        else:
            raise ValueError("Invalid compressed data")
        result.append(entry)
        dictionary[next_code] = s + entry[0]
        next_code += 1
        s = entry
    return result

#몫 압축해제
que = ''.join(lzw_decompress(G))


#0x기준으로 분리(0번째 값은 공백이므로 제거)
que = que.split('0x')[1:]

#10진수로 변환
que = list(map(lambda x: int(x,16),que))

#xor 연산
que = list(map(lambda x: key^x,que))


#나머지랑 조합해서 라플라스 변환의 결과 찾기
result = []
for i in range(len(remains)):
  result.append(304 * que[i] + remains[i])

#역변환 일반항
def a(F, n):   #n = 0....len(G)-1  a_n 구현
  return F//(2**(n-1)*n)

#역변환 적용
result = list(map(a,result,range(1,len(result)+1)))

#문자열(리스트)로 변환
result = list(map(chr,result))

#리스트를 문자열로 합치기
text = ''.join(result)

print(f"복호화 한 텍스트: {text}")


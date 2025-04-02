#1. 파일명 입력 받기
t = input("저장할 파일명을 입력 하세요")
while t == "":
    t = input("저장할 파일명은 비어있을 수 없습니다")

#2. input stream 연결 with block
with open(f'./{t}.txt', "wt", encoding ='utf-8')as fw:
    print('-----------------')
    print('아래부터 입력하세요')
    print('-----------------')

#3. 반복문으로 !q입력 전까지 계속 input 받기아서 write
    i = input("")
    while i != "!q":
        fw.write(i+f"\n")
        i = input("")
    print(f'\n{t}.txt파일을 저장합니다\n\n')
    print('-----------------')

#4. read로 불러오기
with open(f'./{t}.txt',"rt", encoding = 'utf-8') as fr:
    print(f'{t}.txt파일을 읽습니다')
    print('-----------------')
    for index, value in enumerate(fr):
        print(index,value.strip())

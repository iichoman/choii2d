## 게임 소개
 2020년 9월에 출시한 spelunky2의 카피게임이다. spelunky2는 2d 횡스크롤 방식의 로그라이크 계열의 게임으로 스테이지를 진행하면서 몬스터를 피해 아이템을 파밍하며 다음스테이지로 통과하는 게임이다.

 ![ss_bf20692e69cfef2da4b6b4096f42823a5283701c 1920x1080](https://github.com/user-attachments/assets/5575ca7a-eb39-4095-b583-a43e030ad55d)
![ss_e92a2f46bb81fc745684204858ecc1284b3eeae4 600x338](https://github.com/user-attachments/assets/e9cc3211-bc4b-4f46-bb7f-7541e3b0ef3d)
(출처: spelunky2 steam 페이지 https://store.steampowered.com/app/418530/Spelunky_2/)
## 게임 실행 흐름

![제목 없음](https://github.com/user-attachments/assets/70227e56-4b8e-4b78-94f5-524e7440e0f8)


 빨간 테두리가 화면에 표시되는 부분이다.
 시작문에서 플레이어가 스폰되어 시작된다. 인터페이스에 체력과 아이템의 남은 수가 표시되며 체력이 모두 소진되면 게임 오버된다.

 몬스터에게 접촉하면 피해를 입는다. 플레이어는 몬스터를 공격하거나 밟아서 처치할 수 있다.

 해파리는 다음 문을 막고있으며 플레이어는 방울을 3개 터뜨려 해파리를 없애야 다음 문을 통과할 수 있다. 
 다음 문을 통과하면 다음 스테이지로 이동한다. 
 
## 개발 내용
  - scene
    - 메인 메뉴
    - 메인 스테이지 
    - 스테이지 이동 
    - 일시정지 메뉴 
    - 게임오버
 - objects:
     - 플레이어
     - 몬스터
     - 아이템
     - 지형 지물
     - 방울
     - 해파리
     - 문
     - 인터페이스
## 개발 일정 
 ~ 10/28: 리소스를 구할 수 있을만큼 구해본다.
 1주: 플레이어 체력/이동/공격 구현, 몬스터 체력/이동/공격 구현, 
 2주: 메인 메뉴, 서브 메뉴, 게임 오버 구현, 인터페이스 구현, 문 통과 구현
 3주: 맵타일과 지형지물 구현, 아이템 구현
 4주: 방울과 해파리 시스템 구현
 5주: 아이템 구현, 부족한 부분 보완
 6주: 부족한 부분, 추가할 부분 구현 및 보완
 7주: 버그수정 및 보완
## 어려울 것 같은 부분들
 - 타일맵의 구현
 - 몬스터들의 매커니즘 설정 ex 해파리는 방울을 모두 터뜨리면 플레이어에게 조금씩 이동함
 - 아이템 구현 (특히 장착형)
 - 실제 게임은 맵지형이 자동/랜덤 생성 -> 매우 어려울 것 같다.
 - 전체 맵과 카메라, 상하좌우 맵스크롤 
## 원하는 수업 진행 방식
 - 맵 타일을 구현하는 방법
 - 객체의 매커니즘 설정


## 2024.11.11
플레이어의 이동과 점프를 구현하였다.
맵배경을 추가하였다
w07을 참고하여 적용하였다.

## 구현하지 못한 부분 및 보완할 점
공격, 몬스터

몬스터와 몬스터 움직임, 피격과 공격시스템의 구현이 필요하다.
x키를 눌러 공격: 플레이어가 바라보고 있는 방향으로 공격한다.
공격시 일정시간 (1초?) 동안 피격판정이 있는 판정 박스가 플레이어 앞 방향으로 생성되며
플레이어는 공격 모션을 취한다.

원본 게임에서는 공격 버튼을 한번 누르면 채찍을 뒤로 던진 후 앞으로 던진다
뒤, 앞 순서로 피격 판정이 생긴다.
공격중에는 플레이어가 바라보는 방향이 바뀌지 않는다.

인터페이스와 클리어 문의 구현이 필요하다.
좌측 상단에 표시하기로 한다.

클리어문의 판정 박스와 플레이어의 판정 박스가 닿은 상태에서 a키를 눌러 문으로 들어간다


타이틀 화면이나 일시정지 화면은 잠시 뒤로 미뤄놓아야 겠다.

타일맵의 설계가 필요하다 여차하면 타일맵 말고 스테이지에 따라 지형의 형태를 직접 설정해야할 것 같다.

## 2024.11.21
변경사항
- 플레이어 점프의 높낮이 조정(z키를 누른만큼 점프)
- 몬스터 객체 정의
- 채찍공격을 위한 채찍의 피격박스 - 새로운 py파일로 구현예정
- 화면 전환을 위한 scene추가 

생각보다 진도가 안나갔다.....

타일맵을 중점으로 보완할 예정 Tiled
  플레이어 체력/이동/공격 구현, 몬스터 체력/이동/공격 구현,           - 70%
  메인 메뉴, 서브 메뉴, 게임 오버 구현, 인터페이스 구현, 문 통과 구현 - 10%
  맵타일과 지형지물 구현, 아이템 구현                                -  0%  
  방울과 해파리 시스템 구현                                          -  0%   
  아이템 구현, 부족한 부분 보완                                      -  0%         
## 2024.12.12
플레이어 체력/이동/공격 구현, 몬스터 체력/이동/공격 구현,           - 100%
메인 메뉴, 서브 메뉴, 게임 오버 구현, 인터페이스 구현, 문 통과 구현 - 65%
맵타일과 지형지물 구현, 아이템 구현                                -  80%
방울과 해파리 시스템 구현                                          -  70% 
![화면 캡처 2024-12-13 120631](https://github.com/user-attachments/assets/272f5c03-e834-465a-b0b2-b57794df5c8e)
10/7 ~ 10/9 	6회

11/8 ~ 11/15 	6회

11/16 ~ 11/23 	8회

11/24 ~ 11/30 	7회

12/1 ~ 12/4 	4회

12/5 ~ 12/12 	7회

리소스를 구할 수 있을만큼 구해본다.


	-리소스는 게임파일에서 쉽게 구할 수 있었다.

플레이어 체력/이동/공격 구현, 몬스터 체력/이동/공격 구현, 


	-플레이어의 기본적인 구현을 완료하였다
	  몬스터 - 원시인, 박쥐, 거미, 도마뱀을 만들고 각자의 행동 방식을 구현했다

메인 메뉴, 서브 메뉴, 게임 오버 구현, 인터페이스 구현, 문 통과 구현	


	메인메뉴에서 캐릭터 선택과, 일시정지/재시작/게임종료 등의 통합된 메뉴를 구현하고 싶었지만 하지 못했다
	인터페이스에는 플레이어 정보가 표시된다
	문으로 이동하면 다음 스테이지로 넘어간다
 3주: 맵타일과 지형지물 구현, 아이템 구현

 
	맵타일을 적용하고 맵 파일에서 레이어를 적용해 충돌체크를 구현하였다. 
	수업시간에 사용한 타일 그리기에서 타일셋과 레이어별 타일을 전부 그리도록 수정해 사용했다. 
	아이템은 기본 아이템인 폭탄을 구현하고 싶었는데 폭발로 맵이 사라지는 상호작용을 결국 구현하지 못했다.
	
방울과 해파리 시스템 구현	


	-방울만 구현했다. 원래 방울을 모두 터뜨리면 해파리가 다음 스텡이지 문에서 이동하여 플레이어를 쫒아온다.
	구현한 방울은 딱히 쓰임새가 없는 듯

부족한 부분 보완 및 버그수정	


	-버그를 충돌체크 적용이 힘들었고 지금도 자잘한 버그가 존재한다. 최적화가 아쉬운건지 노트북으로 플레이 했을 때 프레임 드랍이 드러났고 
	낮은 프레임으로 충돌계산이 제 떄 이뤄지지 않는 버그가 있었다.

 개발하면서 최대한 원본 게임과 비슷한 느낌을 내는 것이 목표여서 공격 타이밍과 점프 세기부터 속도, 크기, 판정 등을 원본 게임과 계속 비교해가며 만들었는데
 점점 프레임이 밀리다보니 조금 틀어진 것 같다. 뒤에 추가한 몬스터들도 원본의 공격 방식을 최대한 구현해보았다. 사운드를
 추가하겠다고 했는데 다른 구현에 밀려 사운드는 전혀 없는 게임이 되었다.

 제작한 게임이 모작이다보니 만일 게임을 판매할 목적이라면 기존 게임과 차별화된 게임성을 가져야할 것 같다. 모바일로 출시되어있는 슈퍼마리오 런 처럼
 원본의 느낌을 살리되 참신한 방향과 컨셉의 게임이 되어야 할 것 같다. 

 이미 설치되어있는 타일 중 원하는 일부만 지우는 부분을 실패했다. 수업중에 새로 알려주신 코드를 적용해볼까 했지만 맵을 레이어로 이미 만들었기에 불가피했다. 

 이번 수업을 통해 파이썬으로 시작해 2D 게임의 기초 틀 부터 차근차근 다지며 게임을 만들어 나가는 법을 배웠고 직접 원하는
 게임도 제작해보는 경험을 얻었다. 수업 시간에는 많은 종류의 게임들의 구성을 코드를 통해 확인해 나갈 수 있었고
 프로젝트를 통해서 플레이하던 게임의 구성을 따라하며 직접 제작해보았다. 2D게임 개발의 틀을 다질 수 있던 것 같다.
 https://youtu.be/Z6JVT2Sp8aQ?feature=shared&t=26
 https://youtube.com/shorts/anDYwoK04Os?feature=share
 

![IMG_0073](https://github.com/user-attachments/assets/5832b91f-134a-4340-a4bf-a066be94304f)


 

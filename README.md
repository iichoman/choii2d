## 게임 소개
 2020년 9월에 출시한 spelunky2의 카피게임이다. spelunky2는 2d 횡스크롤 방식의 로그라이크 계열의 게임으로 스테이지를 진행하면서 몬스터를 피해 아이템을 파밍하며 다음스테이지로 통과하는 게임이다.

 ![ss_bf20692e69cfef2da4b6b4096f42823a5283701c 1920x1080](https://github.com/user-attachments/assets/5575ca7a-eb39-4095-b583-a43e030ad55d)
![ss_e92a2f46bb81fc745684204858ecc1284b3eeae4 600x338](https://github.com/user-attachments/assets/e9cc3211-bc4b-4f46-bb7f-7541e3b0ef3d)

## 게임 실행 흐름

![ss_bf20692e69cfef2da4b6b4096f42823a5283701c 1920x1080](https://github.com/user-attachments/assets/843f08b3-4972-4684-81c3-1d06457a53a1)

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
 - 아이템 구현
 - 실제 게임은 맵지형이 자동/랜덤 생성 -> 매우 어려울 것 같다.
 - 전체 맵과 카메라, 상하좌우 맵스크롤 
## 원하는 수업 진행 방식
 - 맵 타일을 구현하는 방법
 - 객체의 매커니즘 설정

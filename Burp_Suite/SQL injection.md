# 개요
취약점 이름: SQL injection <br>
플랫폼: PortSwigger Web Security Academy <br>
문제: SQL injection attack, listing the database contents on non-Oracle databases <br>
문제 설명: 이 실습에는 제품 카테고리 필터에 SQL 인젝션 취약점이 포함되어 있습니다. 쿼리 결과는 애플리케이션 응답에 반환되므로 UNION 공격을 사용하여 다른 테이블의 데이터를 가져올 수 있습니다.

해당 애플리케이션에는 로그인 기능이 있으며, 데이터베이스에는 사용자 이름과 비밀번호를 저장하는 테이블이 있습니다. 이 테이블의 이름과 포함된 열을 알아낸 다음, 테이블 내용을 가져와 모든 사용자의 사용자 이름과 비밀번호를 얻어야 합니다.

실습을 완료하려면 해당 administrator사용자로 로그인하세요.<br>
날짜: 26-04-06

# 취약점 개념
SQL injection은 공격자가 쿼리를 조작해서 중요한 정보를 추출하는 취약점이다.<br>
주로 공격자 입력이 그대로 SQL문으로 입력이 될 때 발생한다.

# 문제 상황 분석

<img width="1571" height="866" alt="image" src="https://github.com/user-attachments/assets/90035459-ab03-4a56-b9eb-2bf09ce937a8" /> <br>

<img width="526" height="413" alt="image" src="https://github.com/user-attachments/assets/4e85ef12-6836-4930-9db0-4732977c04ee" /> <br>


쇼핑몰 사이트인 것으로 보인다. <br>
홈 화면에는 태그들이 보이고 로그인 창이 있다.<br>

<img width="930" height="844" alt="image" src="https://github.com/user-attachments/assets/e3bbf4a4-6b07-4942-9bdf-34ce2873c5e2" /> <br>

문제에 나와있는 내용처럼 태그를 들어가보니 태그 필터에 취약점이 존재한다.<br>


# 공격 과정
1. Burp suite로 Proxy 하기 <br>

  <img width="1116" height="729" alt="image" src="https://github.com/user-attachments/assets/b167677e-8bfe-4e08-aa99-e45aba0f9efc" /><br>

2. send to repeater 보내고 취약점 확인하기<br>
  <img width="1120" height="140" alt="image" src="https://github.com/user-attachments/assets/a23db319-b8fa-40df-8bae-7a4c0078d3aa" /><br>
  `'` 입력 시 SQL 문법 오류로 인해 에러가 나온다.<br>
  즉 나의 입력이 SQL문에 영향을 줬다는 얘기이다.<br>

3. union 공격을 위해 컬럼 수 찾기<br>
   <img width="1103" height="88" alt="image" src="https://github.com/user-attachments/assets/ba307dde-010f-4a7e-9aba-b6d9812b4b0e" /><br>

   운이 좋게도 한 번에 컬럼수를 찾을 수 있었다.<br>
   컬럼 수는 2개인걸로 확인됐다.<br>
   
5. 컬럼 문자열 타입 확인하기<br>
   <img width="1400" height="350" alt="image" src="https://github.com/user-attachments/assets/38793c23-4dbc-4f0e-b5e7-2f351758fc38" /><br>
   컬럼 모두 다 문자열을 출력을 할 수 있다.<br>
즉 지금 까지 공격과정을 종합해서 봤을때 SQL injection으로 administrator의 비밀번호가 들어있는 table과 column을 찾아서 비밀번호를 탈취 할 수 있다.<br>


# 우회 및 심화
1. table 찾기<br>
   <img width="1432" height="674" alt="image" src="https://github.com/user-attachments/assets/18fdc404-a972-4233-a0c3-b044bb04da74" /><br>
   꽤 많은 수의 테이블이 나오는 것을 확인할 수 있다.<br>
   이 많은 것을 다 확인하기 어려우니 조건을 걸어서 찾아야한다.<br>
   <img width="1373" height="488" alt="image" src="https://github.com/user-attachments/assets/c01b6904-0f7b-4c4f-ba43-7d89f288e4cc" /><br>
   비밀번호를 찾는게 목적이니 `%pass%`로 조건을 설정해서 찾아봤다.<br>
   pg_user, pg_roles, users_lhexmd가 나왔다.<br>

2. column 확인하기<br>
  <img width="1468" height="554" alt="image" src="https://github.com/user-attachments/assets/6c8b244d-60fe-401f-94ce-c3d26fd63fa0" /><br>
  users_lhexmd 컬럼을 확인 해보니 password_qwrrxt, email, username_maiaumh가 나왔다.<br>
3. 의심되는 컬럼 출력하기<br>
  <img width="1438" height="605" alt="image" src="https://github.com/user-attachments/assets/fc48245b-1367-48ac-b093-bf0cdea99b19" /><br>
  의심되는 컬럼을 출력해보니 administrator의 비밀번호를 찾았다.<br>

# 결과
SQL injection으로 테이블과 컬럼을 찾아서 관리자 계정의 비밀번호를 알아내고, 로그인에 성공했다.<br>

<img width="659" height="625" alt="image" src="https://github.com/user-attachments/assets/dd9f6c11-2992-4a04-91a4-c44327d57e90" /><br>


# 취약점 원인 분석
입력값 검증 부재: 공격자 입력이 필터링 없이 SQL문에 입력됐다.<br>
데이터베이스 권한 설정: 사용자가 information_schema에 접근할 수 있는 권한을 가지고 있다.<br>

# 대응 방안
입력값 화이트리스트 필터링: 카테고리 값이나 안전한 값들만 허용하고, SQL 예약어가 포함된 입력은 차단한다.<br>
최소 권한 원칙: 불필요한 접근권한은 제거하여 정보유출 피해를 최소화 한다.<br>

# 느낀 점
오늘 직접 실습을 해보면서 처음으로 Burp suite를 사용해 봤는데 URL 파라미터에 직접 입력하는 것보다 훨씬 편했고,<br>
서버가 어떻게 돌아가는지 더 쉽게 알 수 있었다.<br>
그리고 오늘 실습을 하면서 SQL injection 취약점이 얼마나 큰 피해를 줄 수 있는지 알 수 있는 실습이었다.<br>

create user 'playdata'@'localhost' identified by '1111';
create user 'playdata'@'%' identified by '1111';

-- 생성된 계정 확인
select user, host from mysql.user;
select * from mysql.user;

-- SQL문의 명령문이 끝날때 ; 붙여야함
-- 실행 : ctrl + enter 
-- 한줄 주석
# 한줄 주석
/*블럭주석
*/

-- 계정에 권한 부여
-- grant 부여할 권한 on 대상 테이블 to 권한 부여할 계정
grant all privileges on *.* to playdata@localhost;
grant all privileges on *.* to playdata@'%';
create user 'playdata'@'localhost' identified by '1111';
create user 'playdata'@'%' identified by '1111';

-- 생성된 계정 확인
select user, host from mysql.user;
select * from mysql.user;

-- SQL문의 명령문이 끝날때 ; 붙여야함
-- 실행 : ctrl + enter 
-- 한줄 주석 ctrl + / 
# 한줄 주석
/*블럭주석
*/

-- 계정에 권한 부여
-- grant 부여할 권한 on 대상 테이블 to 권한 부여할 계정
grant all privileges on *.* to playdata@localhost;
grant all privileges on *.* to playdata@'%';

-- 현재 사용중인 DB확인-- 
SELECT DATABASE();
-- 모든 db 확인 --
SHOW databases;

-- CREATE DB --
CREATE DATABASE test_db;

-- DROP DB -- 
DROP database test_db;

-- DB 선택 -- 
USE test_db; -- test_db를 사용할 것

-- table 생성 -- 
CREATE TABLE member(
id VARCHAR(10) PRIMARY KEY, -- 최대 10글자 --
password VARCHAR(10) NOT NULL, -- not null 필수입력 --
name VARCHAR(10) NOT NULL,
point INT DEFAULT'1000', -- 값이 없으면 1000 기본
email VARCHAR(100) NOT NULL UNIQUE, -- qnique : 중복허용 안함
age INT CHECK(age > 20), -- CHECK 안에 조건식 사용가능
join_date TIMESTAMP NOT NULL DEFAULT current_timestamp -- 값이 insert되는 시점을 지정
);
-- gpt 생성 -- 
CREATE TABLE member (
    id VARCHAR(10) PRIMARY KEY,          -- 최대 10글자 (PK)
    password VARCHAR(10) NOT NULL,       -- NOT NULL 필수 입력
    name VARCHAR(10) NOT NULL,           -- NOT NULL 필수 입력
    point INT DEFAULT 1000,              -- 값이 없으면 기본 1000
    email VARCHAR(100) NOT NULL UNIQUE,  -- UNIQUE: 중복 허용 안 함
    age INT CHECK (age > 20),            -- 나이 20세 이상만 허용
    join_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP -- 가입 시각 자동 설정
);

-- tables 확인, colume 확인-- 
SHOW TABLES;
DESC member;

-- table SELECT -- 
SELECT * FROM member;

--- DROP TABLE --- 
DROP TABLE IF EXISTS aaa;
DROP TABLE IF EXISTS member;

-- INSERT 실습 -- 
INSERT INTO member VALUES ('id-100', '1111', '이순신', 5000, 'lee@a.com', 30, '2023-12-10 11:22:30');
INSERT INTO member (id, password, name, email) VALUES ('id-101', '1111', '유관순','yu@a.com'); 
INSERT INTO member (id, password, name, point, email) VALUES ('id-102', '1111', '신사임당', NULL,'5000money@a.com'); -- NULL을 강제로 넣어줄 수도 있음
INSERT INTO member (id, password, name, point, age, email) VALUES ('id-103', '1111', '세종', NULL, 5, '1000money@a.com'); 

SELECT * FROM member;
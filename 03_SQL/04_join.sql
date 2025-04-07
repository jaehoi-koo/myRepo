/* ********************************************************************************
조인(JOIN) 이란
- 2개 이상의 테이블에 있는 컬럼들을 합쳐서 가상의 테이블을 만들어 조회하는 방식을 말한다.
 	- 소스테이블 : 내가 먼저 읽어야 한다고 생각하는 테이블
	- 타겟테이블 : 소스를 읽은 후 소스에 조인할 대상이 되는 테이블
 
- 각 테이블을 어떻게 합칠지를 표현하는 것을 조인 연산이라고 한다.
    - 조인 연산에 따른 조인종류
        - Equi join , non-equi join
- 조인의 종류
    - Inner Join 
        - 양쪽 테이블에서 조인 조건을 만족하는 행들만 합친다. 
    - Outer Join
        - 한쪽 테이블의 행들을 모두 사용하고 다른 쪽 테이블은 조인 조건을 만족하는 행만 합친다. 조인조건을 만족하는 행이 없는 경우 NULL을 합친다.
        - 종류 : Left Outer Join,  Right Outer Join, Full Outer Join
    - Cross Join
        - 두 테이블의 곱집합을 반환한다. 
******************************************************************************** */        

/* ****************************************
-- INNER JOIN
FROM  테이블a INNER JOIN 테이블b ON 조인조건 

- inner는 생략 할 수 있다.
**************************************** */
-- 직원의 ID(emp.emp_id), 이름(emp.emp_name), 입사년도(emp.hire_date), 소속부서이름(dept.dept_name)을 조회
SELECT e.emp_id, e.emp_name, e.hire_date, d.dept_name
FROM emp e INNER JOIN dept d ON e.dept_id = d.dept_id
ORDER BY 1;

-- 커미션을(emp.comm_pct) 받는 직원들의 직원_ID(emp.emp_id), 이름(emp.emp_name),
-- 급여(emp.salary), 커미션비율(emp.comm_pct), 소속부서이름(dept.dept_name), 부서위치(dept.loc)를 조회. 직원_ID의 내림차순으로 정렬.
SELECT e.emp_id, e.emp_name, e.salary, e.comm_pct, d.dept_name, d.loc
FROM emp e INNER JOIN dept d ON e.dept_id = d.dept_id
WHERE e.comm_pct IS NOT NULL
ORDER BY e.emp_id DESC;

-- 직원의 ID(emp.emp_id)가 100인 직원의 직원_ID(emp.emp_id), 이름(emp.emp_name), 입사년도(emp.hire_date), 소속부서이름(dept.dept_name)을 조회.
SELECT e.emp_id, e.emp_name, e.hire_date, d.dept_name
FROM emp e JOIN dept d ON e.dept_id = d.dept_id
WHERE e.emp_id = 100;

SELECT * FROM emp;
-- 직원_ID(emp.emp_id), 이름(emp.emp_name), 급여(emp.salary), 담당업무명(job.job_title), 소속부서이름(dept.dept_name)을 조회
SELECT e.emp_id, e.emp_name, e.salary, j.job_title, d.dept_name
FROM emp e JOIN job j ON e.job_id = j.job_id JOIN dept d ON e.dept_id = d.dept_id
ORDER BY 1;

--  직원 ID 가 200 인 직원의 직원_ID(emp.emp_id), 이름(emp.emp_name), 급여(emp.salary), 담당업무명(job.job_title), 소속부서이름(dept.dept_name)을 조회              
SELECT e.emp_id, e.emp_name, e.salary, j.job_title, d.dept_name
FROM emp e JOIN job j ON e.job_id = j.job_id JOIN dept d ON e.dept_id = d.dept_id
WHERE e.emp_id = 200;

-- 부서_ID(dept.dept_id)가 30인 부서의 이름(dept.dept_name), 위치(dept.loc), 그 부서에 소속된 직원의 이름(emp.emp_name)을 조회.
SELECT d.dept_name, d.loc, e.emp_name
FROM dept d JOIN emp e ON d.dept_id = e.dept_id
WHERE d.dept_id = 30;

SELECT * FROM salary_grade;
-- 직원의 ID(emp.emp_id), 이름(emp.emp_name), 급여(emp.salary), 급여등급(salary_grade.grade) 를 조회. 
SELECT e.emp_id, e.emp_name, e.salary, s.grade AS "급여등급"
FROM emp e JOIN salary_grade s
WHERE e.salary BETWEEN s.low_sal AND s.high_sal;


-- 'New York'에 위치한(dept.loc) 부서의 부서_ID(dept.dept_id), 부서이름(dept.dept_name), 위치(dept.loc), 
-- 그 부서에 소속된 직원_ID(emp.emp_id), 직원 이름(emp.emp_name), 업무(emp.job_id)를 조회. 
SELECT d.dept_id, d.dept_name, d.loc, e.emp_id, e.emp_name, e.job_id
FROM dept d JOIN emp e ON d.dept_id = e.dept_id
WHERE d.loc = "New York";


-- 부서별 급여(salary)의 평균을 조회. 부서이름(dept.dept_name)과 급여평균을 출력. 급여 평균이 높은 순서로 정렬. 
SELECT  d.dept_id, d.dept_name, 
	    ROUND(AVG(e.salary),2) AS "평균급여"		
FROM emp e JOIN dept d ON e.dept_id = d.dept_id
GROUP BY d.dept_id, d.dept_name
ORDER BY 3 DESC; 

-- 직원의 ID(emp.emp_id), 이름(emp.emp_name), 업무명(job.job_title), 급여(emp.salary), 급여등급(salary_grade.grade), 소속부서명(dept.dept_name)을 조회.
SELECT  e.emp_id,
		e.emp_name,
        j.job_title,
        e.salary,        
        CONCAT(s.grade,"등급") AS "급여등급",
        d.dept_name
FROM emp e JOIN salary_grade s JOIN dept d ON e.dept_id = d.dept_id JOIN job j ON j.job_id = e.job_id
WHERE e.salary BETWEEN s.low_sal AND s.high_sal
ORDER BY 1;


/* ****************************************************
Self 조인
- 물리적으로 하나의 테이블을 두개의 테이블처럼 조인하는 것.
**************************************************** */
SELECT * FROM emp;
-- 직원 ID가 101인 직원의 직원의 ID(emp.emp_id), 이름(emp.emp_name), 상사이름(emp.emp_name)을 조회
SELECT e.emp_id, e.emp_name, m.emp_name AS "manager_name"
FROM emp e JOIN emp m ON e.mgr_id = m.emp_id
WHERE e.emp_id = 101;


/* ****************************************************************************
외부 조인 (Outer Join)
- 불충분 조인
    - 조인 연산 조건을 만족하지 않는 행도 포함해서 합친다
종류
 left  outer join: 구문상 소스 테이블이 왼쪽
 right outer join: 구문상 소스 테이블이 오른쪽
 full outer join:  둘다 소스 테이블 (Mysql은 지원하지 않는다. - union 연산을 이용해서 구현)

- 구문
from 테이블a [LEFT | RIGHT] OUTER JOIN 테이블b ON 조인조건
- OUTER는 생략 가능.

**************************************************************************** */


-- 직원의 id(emp.emp_id), 이름(emp.emp_name), 급여(emp.salary), 부서명(dept.dept_name), 부서위치(dept.loc)를 조회. 
-- 부서가 없는 직원의 정보도 나오도록 조회. dept_name의 내림차순으로 정렬한다.
SELECT e.emp_id, e.emp_name, e.salary, d.dept_name, d.loc
FROM emp e LEFT OUTER JOIN dept d ON e.dept_id = d.dept_id -- LEFT OUTER JOIN 
-- ORDER BY d.dept_name DESC; 
ORDER BY e.emp_id;

-- INNER JOIN사용시 NULL을 가진 인원은 표시가 안됨
SELECT COUNT(*)
FROM emp e JOIN dept d ON e.dept_id = d.dept_id; -- 5명 빠짐

-- 모든 직원의 id(emp.emp_id), 이름(emp.emp_name), 부서_id(emp.dept_id)를 조회하는데
-- 부서_id가 80 인 직원들은 부서명(dept.dept_name)과 부서위치(dept.loc) 도 같이 출력한다. (부서 ID가 80이 아니면 null이 나오도록)
SELECT e.emp_id, e.emp_name, d.dept_id, d.dept_name, d.loc
FROM emp e LEFT JOIN dept d ON e.dept_id = d.dept_id AND d.dept_id = 80;

        
--  직원_id(emp.emp_id)가 100, 110, 120, 130, 140인 직원의 ID(emp.emp_id),이름(emp.emp_name), 업무명(job.job_title) 을 조회. 업무명이 없을 경우 '미배정' 으로 조회
SELECT * FROM emp;

SELECT e.emp_id, e.emp_name, IFNULL(j.job_title,"미배정") AS "job_title"
FROM emp e LEFT JOIN job j ON e.job_id = j.job_id
WHERE e.emp_id IN (100,110,120,130,140);


-- 부서 ID(dept.dept_id), 부서이름(dept.dept_name)과 그 부서에 속한 직원들의 수를 조회. 직원이 없는 부서는 0이 나오도록 조회하고 직원수가 많은 부서 순서로 조회.
SELECT * FROM emp;
SELECT * FROM dept;

SELECT d.dept_id, d.dept_name, COUNT(e.emp_id) AS "부서인원" -- PK 값을 넣어서 조회해야 NULL을 빼고 COUNT
FROM dept d LEFT JOIN emp e ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name
ORDER BY 3 DESC;

SELECT *
FROM dept d LEFT JOIN emp e ON d.dept_id = e.dept_id; -- NULL값이 포함되어 Return


-- EMP 테이블에서 부서_ID(emp.dept_id)가 90 인 모든 직원들의 id(emp.emp_id), 이름(emp.emp_name), 상사이름(emp.emp_name), 입사일(emp.hire_date)을 조회. 
-- 입사일은 yyyy/mm/dd 형식으로 출력
SELECT *
FROM emp
WHERE dept_id = 90;

SELECT  e.emp_id,
		e.emp_name,
        m.emp_name AS "manager_name",
        DATE_FORMAT(e.hire_date, "%Y/%m/%d") AS "hire_date"
FROM emp e LEFT JOIN emp m ON e.mgr_id = m.emp_id
WHERE e.dept_id = 90;


-- 2003년~2005년 사이에 입사한 모든 직원의 id(emp.emp_id), 이름(emp.emp_name), 업무명(job.job_title), 급여(emp.salary), 입사일(emp.hire_date),
-- 상사이름(emp.emp_name), 상사의입사일(emp.hire_date), 소속부서이름(dept.dept_name), 부서위치(dept.loc)를 조회.

SELECT  e.emp_id,
		e.emp_name,
        j.job_title,
        e.salary,
        e.hire_date,
        m.emp_name AS "manager_name",
        m.hire_date AS "manager_hire_date",
        d.dept_name,
        d.loc,
        s.grade
FROM emp e LEFT JOIN job j ON e.job_id = j.job_id
		   LEFT JOIN dept d ON e.dept_id = d.dept_id
           LEFT JOIN emp m ON e.mgr_id = m.emp_id
           LEFT JOIN salary_grade s ON e.salary BETWEEN s.low_sal AND s.high_sal
WHERE YEAR(e.hire_date) BETWEEN 2003 AND 2005
ORDER BY emp_id;

SELECT *
FROM salary_grade;
-- 검증 : 월별 금액
USE frl;
SELECT * FROM frl LIMIT 1;

SELECT * FROM frl1 A
WHERE A.`G/L` = '10030KR061';

SELECT 
A.`Period`,
COUNT(*)
FROM frl1 A
GROUP BY A.`Period`;

DELETE FROM frl1
WHERE `Period` = 3;

SELECT * FROM frl1 LIMIT 10;


DROP TABLE frl;
DROP TABLE frl2;


-- 사전 Test
SELECT 
A.`D/C`
,SUM(A.`Loc.curr.amount`)
FROM frl_new A
GROUP BY A.`D/C`;

-- PASS!

SELECT MAX(LENGTH(`Amount`))
FROM frl_new A;

SELECT * FROM frl2 B
WHERE B.`Period` = 3 LIMIT 10;

--
SELECT 
A.`Period`,
SUM(A.`Loc.curr.amount`) 
FROM frl A
GROUP BY A.`Period`;

-- 검증 : 계정별 합계액

SELECT 
A.`G/L`,
SUM(A.`Loc.curr.amount`) 
FROM frl A
GROUP BY A.`G/L`;

-- G/L IS NULL? => 해결. 2월은 따로

SELECT 
*
FROM frl A
WHERE A.`G/L` IS NULL;

SELECT 
A.`Period`,
COUNT(*)
FROM frl A
WHERE A.`G/L` IS NULL
GROUP BY A.`Period`;

-- 2월에만 202,501건 있음

--
SELECT *
FROM frl A
WHERE (
(A.`D/C` <> 'D') OR
(A.`D/C` <> 'C')
);

-- 테이블 복사
CREATE TABLE frl2 LIKE frl1;
INSERT INTO frl2 SELECT * FROM frl1; -- 백업함

ALTER TABLE frl.frl1 RENAME TO frl.frl;

SELECT * FROM frl 
WHERE `Period` = 8
LIMIT 1;

-- 4월치, 즉 Peirod 8 은 다 죽인다.
DELETE FROM frl
WHERE `Period` = 8;

SELECT * FROM frl LIMIT 10;

-- O/B , E/B가 모두 0인 계정에 대한 월별잔액 Test

SELECT
A.`Period`
,SUM(A.`Loc.curr.amount`)
,SUM(ABS(A.`Loc.curr.amount`))
FROM frl A
WHERE A.`G/L` IN
(
'10038KR002',
'10038KR034',
'10038KR091',
'10038KR092',
'10038KR093',
'10038KR094',
'10039KR002',
'10039KR034',
'10039KR091',
'10039KR092',
'10039KR094')

GROUP BY A.`Period`
ORDER BY `Period`
;

SELECT * FROM frl LIMIT 1;

SELECT *
FROM frl A
WHERE A.`Period` = 6
INTO OUTFILE '/test_6.csv'
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n';

-- 테이블 추가
USE frl;
CREATE TABLE frl_new LIKE frl;

SELECT COUNT(*) FROM frl_new;







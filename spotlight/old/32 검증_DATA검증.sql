----------------------------------
-- Step. 
-- 데이터 클렌징 : 검증 : 일반화
----------------------------------

-- 에프알엘코리아. 230927

-- 변수선언부 -- 여기서 회사 컬럼명을 매핑해주고, 기존 쿼리 활용함
;
SET @cAmtec = 'Loc.curr.amount';
SET @cGl = 'G/L';
SET @cJno = 'DocumentNo';

SET @tName = 'frl.frl_new';


-- 1. Records Check : 

SET @s = CONCAT('
SELECT COUNT(*) 
FROM ',@tName,';
');

PREPARE q1 FROM @s;
EXECUTE q1;
DEALLOCATE PREPARE q1;

-- 2. 전표금액 합계 0

SET @s = CONCAT('
SELECT SUM(`',@cAmtec,'`)
FROM ',@tName,';
');


PREPARE q1 FROM @s;
EXECUTE q1;
DEALLOCATE PREPARE q1;

-- 3. 계정별 합계 추출 및 Recon 

SET @s = CONCAT('
SELECT
A.`',@cGl,'`
,SUM(A.`',@cAmtec,'`)
FROM
',@tName,' A
GROUP BY A.`',@cGl,'`;
');

SELECT @s;
PREPARE q1 FROM @s;
EXECUTE q1;
DEALLOCATE PREPARE q1;

-- index 설정

CREATE INDEX id1 ON frl.frl_new (`DocumentNo`, `Loc.curr.amount`); -- 전표번호로 인덱스 설정

-- 9. 전표번호 별로 차대변금액이 일치하는지 확인

SELECT A.`DocumentNo`
,SUM(A.`Loc.curr.amount`)
FROM frl_new A
GROUP BY A.`DocumentNo`
HAVING ( SUM(A.`Loc.curr.amount`) ) <> 0 ;

SET @s = CONCAT('
SELECT A.`',@cJno,'`
,SUM(A.`',@cAmtec,'`)
FROM ',@tName,' A
GROUP BY A.`',@cJno,'`
HAVING ( SUM(A.`',@cAmtec,'`) ) <> 0 ;
');

SELECT @s;
PREPARE q1 FROM @s;
EXECUTE q1;
DEALLOCATE PREPARE q1;

-- 9. 전표번호 별로 전기일자/작성일자는 1개만 존재하는지 확인 

CREATE INDEX id2 ON frl_new (`DocumentNo`, `Pstng Date`, `Entry Dte`); -- 전표번호, 전기일자, 작성일자로 인덱스 설정

-- a. 전기일자 기준
SELECT *
FROM (
	SELECT 
	A.`DocumentNo`
	,A.`Pstng Date`
	,ROW_NUMBER() OVER (PARTITION BY A.`DocumentNo` ORDER BY A.`DocumentNo`) CNT
	FROM frl_new A
	GROUP BY 
	A.`DocumentNo` -- 전표번호
	,A.`Pstng Date` -- 전기일자
    ) A
WHERE A.CNT <> 1;

-- b. 입력일자 기준

SELECT *
FROM (
	SELECT 
	A.`DocumentNo`
	,A.`Entry Dte`
	,ROW_NUMBER() OVER (PARTITION BY A.`DocumentNo` ORDER BY A.`DocumentNo`) CNT
	FROM frl_new A
	GROUP BY 
	A.`DocumentNo` -- 전표번호
	,A.`Entry Dte` -- 전기일자
    ) A
WHERE A.CNT <> 1;

-- 12. 전표번호 별 작성자가 동일한가?

CREATE INDEX id3 ON hs_f.hs_f (`DocumentNo`, `User Name`); -- 전표번호, 작성자로 인덱스 설정

SELECT *
FROM (
	SELECT 
	A.`DocumentNo`
	,A.`User Name` -- 32 : 작성자
	,ROW_NUMBER() OVER (PARTITION BY A.`DocumentNo` ORDER BY A.`DocumentNo`) CNT
	FROM frl_new A
	GROUP BY 
	A.`DocumentNo` -- 전표번호
	,A.`User Name` -- 작성자
    ) A
WHERE A.CNT <> 1;

-- 13. 모든 라인에 작성자ID가 있는가?
USE frl;
SELECT COUNT(*)
FROM frl_new A
WHERE A.`User Name` IS NULL;

-- 14. 대상기간 외 JE 존재여부

SELECT COUNT(*)
FROM frl_new A
WHERE 1=1
AND (A.`Pstng Date` < '2022/09/01') OR (A.`Pstng Date` > '2023/08/31');

SELECT * FROM frl_new LIMIT 5;

-- 11. 모든 라인에 값이 들어가 있는지 확인 UserID Entered
SELECT *
FROM PN_NEW_RESULT A
WHERE A.[UserID Entered] IS NULL;

SELECT * FROM frl_new A LIMIT 100;

SELECT COUNT(*) FROM frl_new;
WHERE A.`Tr.prt` IS NOT NULL;


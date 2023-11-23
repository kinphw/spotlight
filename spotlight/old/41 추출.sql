-- Txt로 추출하는 코드
--

-- (감사팀 요청) 매출 추출

-- 검증. 926,385,568,587 이 나와야 함
SELECT COUNT(*)
FROM hs_f.hs_f A
INNER JOIN hs_f.coa B
ON A.`20` = B.coa

-- 추출 : 매출액
SELECT *
FROM hs_f.hs_f A
INNER JOIN hs_f.coa B
ON A.`20` = B.coa
INTO OUTFILE '/sales_hs_2306.csv'
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n';

------------------------------------------
-- JE 추출 설계 by LEAD -- Test 후 일단 Table에 적재
------------------------------------------
-- CREATE TABLE hs_f_result;
SELECT 
'1' AS `Entity`, 
'호텔신라' AS `Company Name`, 
A.`8` AS `Entity Currency (EC)`, 
A.`1` AS `Journal Number`, 
A.`4` AS `Financial Period`,
STR_TO_DATE(A.`33`, '%Y%m%d') AS `Date Entered`, 
STR_TO_DATE(A.`5`, '%Y%m%d') AS `Date Effective`, 
A.`11` AS `Journal Description`, 
A.`35` AS `Auto Manual or Interface`, 
A.`20` AS `Account Number`, 
B.`name` AS `Account Description`,
A.`23` AS `Currency`, 
CASE 
WHEN A.`19` = 'H' THEN 'C'
WHEN A.`19` = 'S' THEN 'D'
END
 AS `DC Indicator`, 
A.`22` AS `Signed Journal Amount`, 

-- START : Case_거래통화
CASE
WHEN A.`22` > 0 THEN ABS(A.`22`)
ELSE 0
END AS `Unsigned Debit Amount`,

CASE
WHEN A.`22` < 0 THEN ABS(A.`22`)
ELSE 0
END AS `Unsigned Credit Amount`,
-- END : Case_거래통화

A.`21` AS `Signed Amount EC`, 

-- START : Case_표시통화

CASE
WHEN A.`21` > 0 THEN ABS(A.`21`)
ELSE 0
END AS `Unsigned Debit Amount EC`,

CASE
WHEN A.`21` < 0 THEN ABS(A.`21`)
ELSE 0
END AS `Unsigned Credit Amount EC`,

-- END : Case_표시통화
A.`17` AS `Line Number`, 
A.`30` AS `Line Description`, 
A.`34` AS `Time Entered`, 
A.`32` AS `UserID Entered`
FROM hs_f A
LEFT JOIN coa_full B
ON A.`20` = B.`code`

WHERE A.`4` = '1' -- 월별로 추출
INTO OUTFILE '/gl_hs01.csv'
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n';
;

---------------
-- 파일로 추출
---------------
SELECT * FROM hs_f.hs_f_result LIMIT 1;

SELECT *
FROM hs_f.hs_f_result A;

USE hs_f;

-- RE : 조인삭제후 추출. 조인으로 인해 시간이 너무 오래걸림
CREATE TABLE hs.f_hs_f_result
SELECT 
'1' AS `Entity`, 
'호텔신라' AS `Company Name`, 
A.`8` AS `Entity Currency (EC)`, 
A.`1` AS `Journal Number`, 
A.`4` AS `Financial Period`,
STR_TO_DATE(A.`33`, '%Y%m%d') AS `Date Entered`, 
STR_TO_DATE(A.`5`, '%Y%m%d') AS `Date Effective`, 
A.`11` AS `Journal Description`, 
A.`35` AS `Auto Manual or Interface`, 
A.`20` AS `Account Number`, 
A.`23` AS `Currency`, 
CASE 
WHEN A.`19` = 'H' THEN 'C'
WHEN A.`19` = 'S' THEN 'D'
END
 AS `DC Indicator`, 
A.`22` AS `Signed Journal Amount`, 

-- START : Case_거래통화
CASE
WHEN A.`22` > 0 THEN ABS(A.`22`)
ELSE 0
END AS `Unsigned Debit Amount`,

CASE
WHEN A.`22` < 0 THEN ABS(A.`22`)
ELSE 0
END AS `Unsigned Credit Amount`,
-- END : Case_거래통화

A.`21` AS `Signed Amount EC`, 

-- START : Case_표시통화

CASE
WHEN A.`21` > 0 THEN ABS(A.`21`)
ELSE 0
END AS `Unsigned Debit Amount EC`,

CASE
WHEN A.`21` < 0 THEN ABS(A.`21`)
ELSE 0
END AS `Unsigned Credit Amount EC`,

-- END : Case_표시통화
A.`17` AS `Line Number`, 
A.`30` AS `Line Description`, 
A.`34` AS `Time Entered`, 
A.`32` AS `UserID Entered`
FROM hs_f A;

--
-- 파일로 추출구문
INTO OUTFILE '/gl_hs_nojoin.csv'
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n';
;


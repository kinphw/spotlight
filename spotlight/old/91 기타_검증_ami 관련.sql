-- Indexing

CREATE INDEX ;

SELECT * FROM frl_new LIMIT 1;

ALTER TABLE frl_new ADD INDEX id3(`DocumentNo`, `Source`);

ALTER TABLE tmp_ami ADD INDEX id1(`Journal Number`);

-- Check

SELECT
A.`DocumentNo`, A.`Source`
FROM frl_new A
INNER JOIN tmp_ami B
ON A.`DocumentNo` = B.`Journal Number`
GROUP BY A.`DocumentNo`, A.`Source`
HAVING A.`Source` <> 'SPREADSHEET'
ORDER BY A.`DocumentNo`, A.`Source`;

SELECT DISTINCT A.`DocumentNo` FROM frl_new A;

-- 저널 안에 SOURCE가 여러개인 것 CHK

SELECT *
FROM (
	SELECT 
	*
	,ROW_NUMBER() OVER (PARTITION BY `DocumentNo` ORDER BY `DocumentNo`) CNT
	FROM (
		SELECT A.`DocumentNo`, A.`Source`
		FROM frl_new A
		GROUP BY A.`DocumentNo`, A.`Source` 
		) A
	) B
WHERE B.`CNT` <> 1;

--
SELECT * FROM frl_new A
WHERE A.`DocumentNo` = 1000000001;


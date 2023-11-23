-- 테이블 생성문
CREATE TABLE lse -- DEFINE TABLE NAME
(ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 -- 아래를 엑셀에서 붙임
`ROW_NUM` VARCHAR(9),
`회사코드` VARCHAR(19),
`전표번호` VARCHAR(10),
`작성일자` VARCHAR(11),
`작성자ID` VARCHAR(6),
`전기일자` VARCHAR(11),
`증빙일자` VARCHAR(11),
`회계월` VARCHAR(2),
`자동/수동구분` VARCHAR(9),
`전표적요` VARCHAR(152),
`전표행번` VARCHAR(6),
`전표통화코드` VARCHAR(4),
`기준통화코드` VARCHAR(4),
`차변대변구분` VARCHAR(2),
`전표금액` VARCHAR(16),
`차변금액` VARCHAR(15),
`대변금액` VARCHAR(15),
`전표금액(기준통화)` VARCHAR(14),
`차변금액(기준통화)` VARCHAR(13),
`대변금액(기준통화)` VARCHAR(13),
`계정과목` VARCHAR(8),
`계정과목명` VARCHAR(28)
);


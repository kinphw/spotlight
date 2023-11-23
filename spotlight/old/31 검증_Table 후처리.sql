-- Table 후처리

-- 1. Signed 처리

-- 둘다 크기를 좀 키워준다. 안그러면 합계가 안맞아짐
ALTER TABLE frl_new MODIFY `Loc.curr.amount` varchar(15);
ALTER TABLE frl_new MODIFY `Amount` varchar(16);
--

UPDATE frl_new A
SET A.`Loc.curr.amount` = A.`Loc.curr.amount`*(-1)
WHERE A.`D/C` = 'H';

UPDATE frl_new A
SET A.`Amount` = A.`Amount`*(-1)
WHERE A.`D/C` = 'H';



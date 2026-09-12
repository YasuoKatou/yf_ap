select S1.brand_code
from (
    select T1.brand_code,
    (T2.MA_short1 / T2.MA_short6) wari
    from brand T1
    left join hist_ana1 T2
       on substr(T2.table_name, 6) = T1.brand_code
    where T1.paypay = 'P'
      and T2.MA_short6 < MA_short1
      and T2.MA_long6 < T2.MA_long1
) S1
where S1.wari >= :min_wari
order by S1.wari desc
;

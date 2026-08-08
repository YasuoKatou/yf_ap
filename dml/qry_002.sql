select
  table_name
, cast(Close1 / Close10 * 1000 as integer) / 1000.0 rt1
from hist_ana1
where Close10 < Close1
  and MA_short7 < MA_short10 and MA_short2 < MA_short1
  and MA_long7  < MA_long10  and MA_long2  < MA_long1
  and MA_long1 < MA_short1
order by (Close1 / Close10) desc;


create table combo_demographics as (
select p.state, p.city, 
p.poverty_rate, e.percent_completed_hs, 
r.share_white, r.share_black, r.share_native, r.share_asian, r.share_hispanic
from poverty_level p
join edu_level e
on p.state = e.state and p.city = e.city
join race_share r
on p.state = r.state and p.city = r.city
order by 1,2);


drop table if exists test;

create table test 
	(state string,
	city string,
	metric string,
	metric_val numeric);


insert into test
select state, city, 'poverty', poverty_rate/1.0
from poverty_level;


insert into test
select state, city, 'edu', percent_completed_hs/1.0
from edu_level;

insert into test
select state, city, 'share_white', share_white/1.0
from race_share;

insert into test
select state, city, 'share_black', share_black/1.0
from race_share;

insert into test
select state, city, 'share_asian', share_asian/1.0
from race_share;

insert into test
select state, city, 'share_native', share_native/1.0
from race_share;

insert into test
select state, city, 'share_hispanic', share_hispanic/1.0
from race_share;


alter table test rename column poverty rate to metric;

alter table test add column metric numeric;

update test set metric = poverty_rate;

update test delete column poverty_rate;


with _interactions as (
    select country_code,
        video_id,
        sum(interaction_events) total_interactions
    from viewership_data
    group by 1, 2
    having sum(interaction_events) >= 150
), _ranking as (
    select country_code,
        video_id,
        total_interactions,
        row_number() over (partition by country_code order by total_interactions desc) _ranking_no
    from _interactions
)
select country_code,
    video_id,
    total_interactions
from _ranking
where _ranking_no = 1
order by country_code
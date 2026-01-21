select
    m.message_id,
    c.channel_key,
    d.date_key,
    i.detected_object,
    i.confidence_score
from raw.image_detections i
join {{ ref('fct_messages') }} m
    on i.message_id = m.message_id
join {{ ref('dim_channels') }} c
    on m.channel_key = c.channel_key
join {{ ref('dim_dates') }} d
    on m.date_key = d.date_key

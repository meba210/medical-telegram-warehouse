select distinct
    to_char(message_date,'YYYYMMDD')::int as date_key,
    message_date::date as full_date
from {{ ref('stg_telegram_messages') }}

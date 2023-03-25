from google.cloud import bigquery # for type hint

async def async_make_bigquery_request(client: bigquery.Client, tag: str):
    query = f"""
    WITH Experts AS
    (
    SELECT ans.owner_user_id AS user_id, COUNT(ans.id) as number_of_answers
    FROM `bigquery-public-data.stackoverflow.posts_answers` AS ans
    INNER JOIN `bigquery-public-data.stackoverflow.posts_questions` AS q
    ON ans.parent_id = q.id
    WHERE q.tags LIKE '%{tag}%'
    GROUP BY user_id
    ORDER BY number_of_answers DESC
    LIMIT 10
    )
    SELECT e.user_id as user_id, e.number_of_answers as number_of_answers, users.reputation as reps, users.about_me as about, 
    users.display_name as display_name
    FROM Experts as e
    INNER JOIN `bigquery-public-data.stackoverflow.users` AS users
    ON e.user_id = users.id
    ORDER BY number_of_answers DESC
    """
    query_job = client.query(query)
    data = [dict(row) for row in query_job]
    return data

def make_bigquery_request(client: bigquery.Client, tag: str):
    query = f"""
    WITH Experts AS
    (
    SELECT ans.owner_user_id AS user_id, COUNT(ans.id) as number_of_answers
    FROM `bigquery-public-data.stackoverflow.posts_answers` AS ans
    INNER JOIN `bigquery-public-data.stackoverflow.posts_questions` AS q
    ON ans.parent_id = q.id
    WHERE q.tags LIKE '%{tag}%'
    GROUP BY user_id
    ORDER BY number_of_answers DESC
    LIMIT 16
    )
    SELECT e.user_id as user_id, e.number_of_answers as number_of_answers, users.reputation as reps, users.about_me as about, 
    users.display_name as display_name
    FROM Experts as e
    INNER JOIN `bigquery-public-data.stackoverflow.users` AS users
    ON e.user_id = users.id
    ORDER BY number_of_answers DESC
    """
    query_job = client.query(query)
    data = [dict(row) for row in query_job]
    return data
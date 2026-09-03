from datetime import timedelta


def calculate_response_deadline(created_at):
    current_date = created_at
    business_days_added = 0

    while business_days_added < 3:
        current_date += timedelta(days=1)

        if current_date.weekday() < 5:
            business_days_added += 1

    return current_date
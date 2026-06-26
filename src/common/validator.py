def check_honeypot(candidate):
    """
    Validates if a candidate is a honeypot (fake profile).
    Returns True if it's a honeypot, False otherwise.
    """
    years = candidate.get('profile', {}).get('years_of_experience', 0)
    history = candidate.get('career_history', [])
    skills = candidate.get('skills', [])

    max_possible_months = int(years * 12) + 3

    for skill in skills:
        if skill.get('duration_months', 0) > max_possible_months * 1.05:
            return True

    total_job_months = sum(job.get('duration_months', 0) for job in history)
    if total_job_months > max_possible_months * 1.5:
        return True

    return False

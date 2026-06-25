import csv

def _generate_reasoning(cand):
    """
    Generates specific, detailed, non-hallucinated reasoning from actual candidate data.
    """
    profile = cand.get('profile', {})
    signals = cand.get('redrob_signals', {})
    career = cand.get('career_history', [])

    title = profile.get('current_title', 'Engineer')
    years = profile.get('years_of_experience', 0)
    company = profile.get('current_company', 'N/A')

    parts = [f"{title} ({years}y @ {company})"]

    # Domain expertise
    skills = cand.get('skills', [])
    ml_skills = [s.get('name') for s in skills if any(x in s.get('name', '').lower() for x in ['ml', 'python', 'pytorch', 'tensorflow', 'nlp'])][:3]
    vector_skills = [s.get('name') for s in skills if any(x in s.get('name', '').lower() for x in ['vector', 'milvus', 'pinecone', 'faiss', 'rag'])][:2]

    if vector_skills:
        parts.append(f"Vector DB: {', '.join(vector_skills)}")
    elif ml_skills:
        parts.append(f"ML: {', '.join(ml_skills)}")

    # Backend infrastructure
    backend_skills = [s.get('name') for s in skills if any(x in s.get('name', '').lower() for x in ['spark', 'airflow', 'kafka', 'sql'])][:2]
    if backend_skills:
        parts.append(f"Backend: {', '.join(backend_skills)}")

    # Career trajectory
    if len(career) >= 2:
        senior_roles = sum(1 for j in career if any(x in j.get('title', '').lower() for x in ['senior', 'lead', 'principal']))
        if senior_roles >= 1:
            parts.append("↗️ Seniority growth")

    # Behavioral signals
    github_score = signals.get('github_activity_score', -1)
    if github_score > 70:
        parts.append("⭐ Strong GitHub")
    elif github_score > 30:
        parts.append("✓ GitHub active")

    resp_rate = signals.get('recruiter_response_rate', 0)
    if resp_rate > 0.8:
        parts.append("🚀 Highly responsive")
    elif resp_rate > 0.5:
        parts.append("✓ Responsive")

    # Concerns/flags
    notice = signals.get('notice_period_days', 0)
    if notice > 90:
        parts.append(f"⚠️ {notice}d notice")

    open_to_work = signals.get('open_to_work_flag', False)
    if not open_to_work:
        parts.append("⚠️ Not actively open")

    return " | ".join(parts)[:220]

def export_submission(candidates, scores, out_path):
    """
    Sorts candidates by score, breaks ties by candidate_id, and writes top 100 to CSV.
    """
    import os
    dir_name = os.path.dirname(out_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    # Combine candidate ID, score, and the raw candidate object
    scored_candidates = []
    for cand, score in zip(candidates, scores):
        scored_candidates.append({
            'candidate_id': cand.get('candidate_id'),
            'score': float(score),
            'raw': cand
        })
        
    # Sort by score descending, then candidate_id ascending
    scored_candidates.sort(key=lambda x: (x['score'], x['candidate_id']), reverse=True)
    
    # Need to reverse candidate_id sort because reverse=True sorted both descending.
    # To do it correctly:
    scored_candidates.sort(key=lambda x: (-x['score'], x['candidate_id']))
    
    top_100 = scored_candidates[:100]
    
    print(f"Writing top 100 to {out_path}...")
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['candidate_id', 'rank', 'score', 'reasoning'])
        
        for rank, item in enumerate(top_100, 1):
            cand_id = item['candidate_id']
            score = item['score']
            reasoning = _generate_reasoning(item['raw'])
            
            writer.writerow([cand_id, rank, score, reasoning])
            
    # Save the full rankings as requested in the plan
    full_out_path = os.path.join(os.path.dirname(out_path), 'rankings_full.csv')
    print(f"Writing all {len(scored_candidates)} viable candidates to {full_out_path}...")
    with open(full_out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['candidate_id', 'rank', 'score', 'reasoning'])
        for rank, item in enumerate(scored_candidates, 1):
            writer.writerow([item['candidate_id'], rank, item['score'], _generate_reasoning(item['raw'])])
    
    print("Done!")

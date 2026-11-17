def ats_score(text):

    score = 50

    if "python" in text.lower():
        score += 10

    if "project" in text.lower():
        score += 10

    if "internship" in text.lower():
        score += 10

    if "java" in text.lower():
        score += 10

    return min(score, 100)
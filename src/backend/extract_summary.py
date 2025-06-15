import re
from . import pdf_to_string

NEXT_HEADERS = (
    r'(?:summary|professional summary|profile|highlights|skills?|technical skills?|'
    r'work\s+history|work\s+experience|professional\s+experience|experience|'
    r'education|education\s+and\s+training|academics?|accomplishments?|projects?'
    r'affiliations|interests?)'
)

def grab_section(text, header):
    pattern = rf'''^\s*{header}\s*:?[\r\n]+(.*?)(?=^\s*{NEXT_HEADERS}\s*:?\s*$|\Z)'''

            #   rf'''^\s*{header}\s*:?\s*[\r\n]+(.*?)(?=^\s*{NEXT_HEADERS}\s*:?\b|\Z)'''
    m = re.search(pattern, text, re.I | re.M | re.S )
    return m.group(1).strip() if m else ''

def extract_skills(text):
    skills_raw = grab_section(text, r'(?:skills?|technical\s+skills?)')
    skills = [s.strip() for chunk in re.split(r'[\n,]', skills_raw)
              if (s := chunk.strip())]
    return skills

def extract_summary(text):
    summary_raw = grab_section(text, r'(?:summary|professional\s+summary|career\s+overview|highlights)')
    summary = [s.strip() for chunk in re.split(r'[\n]', summary_raw)
              if (s := chunk.strip())]
    return summary

def extract_experience(text):
    exp_raw = grab_section(text, r'(?:experience|professional\s+experience|work history|work\s+experience)')
    if not exp_raw:
        return []

    # date range:  "Jan 2014 – Present"  /  "01/2014 - 03/2016"  /  "2018 - 2020" / Jan 2024 to Present
    date_pattern = re.compile(
        r'([A-Za-z]{3,9}\s+\d{4}\s*(?:-|—|to)\s*(?:[A-Za-z]{3,9}\s+\d{4}|present|current)|'
        r'\d{1,2}/\d{4}\s*(?:-|—|to)\s*(?:\d{1,2}/\d{4}|present|current)|'
        r'\d{4}\s*(?:-|—|to)\s*(?:\d{4}|present|current))',
        re.I
    )

    parts = date_pattern.split(exp_raw)
    jobs = []

    for i in range(1, len(parts), 2):
        date_range = parts[i].strip()
        job_chunk = parts[i + 1].strip()

        if not job_chunk:
            continue

        lines = [ln.strip() for ln in job_chunk.splitlines() if ln.strip()]
        company_title = lines[0] if lines else ''

        if '—' in company_title or '–' in company_title or '-' in company_title:
            sep = '—' if '—' in company_title else ('–' if '–' in company_title else '-')
            company, _, after = company_title.partition(sep)
            company = company.strip()
            words = after.strip().split()
            location = ' '.join(words[:2]) if len(words) >= 2 else ''
            job_title = ' '.join(words[2:]) if len(words) > 2 else ''
        else:
            company, location, job_title = company_title, '', ''

        responsibilities = lines[1:] if len(lines) > 1 else []

        jobs.append({
            'date_range': date_range,
            'company': company,
            'location': location,
            'job_title': job_title,
            'responsibilities': responsibilities
        })

    return jobs

def extract_education(text):
    education_raw = grab_section(text, r'(?:education|education\s+and\s+training)')
    return [ln.strip() for ln in education_raw.splitlines() if ln.strip()]

def parse_resume(text):
    result = {
        'skills': extract_skills(text),
        'summary': extract_summary(text),
        'experience': extract_experience(text),
        'education': extract_education(text)
    }
    return result

def print_parse_result(parsed_data):
    print("=== RESUME PARSING RESULT ===\n\n")
    
    print("SKILLS:\n")
    for skill in parsed_data['skills']:
        print(f"• {skill}")
    print("\n")
    
    print("SUMMARY:\n")
    for summary_line in parsed_data['summary']:
        print(f"{summary_line}")
    print("\n")
    
    print("EXPERIENCE:\n")
    for job in parsed_data['experience']:
        print(f"\n{job['date_range']}")
        print(f"{job['company']}")
        if job['location']:
            print(f"{job['location']}")
        if job['job_title']:
            print(f"{job['job_title']}")
        
        if job['responsibilities']:
            print("Responsibilities:\n")
            for resp in job['responsibilities']:
                print(f"   • {resp}")

    print("EDUCATION: ")
    for education_line in parsed_data['education']:
        print(f"{education_line}")
    print("\n")

if __name__ == "__main__":
    text = pdf_to_string.pdf_to_string("data/Apparel/10182582.pdf")
    print(text)
    parsed_data = parse_resume(text)
    print_parse_result(parsed_data)
    

import random
list= [
    "mayur", "rushi", "aish", "vishal", "rutik", "honey", "saumya", "sid", "utkarsha", "sara", "akansha", "dhruv", "ankush", "bhumika", "gayatri"
]
gender = [
    "male", "female"
]
email = [
    "mayur@gmail.com", "rushi@gmail.com", "aish@gmail.com", "vishal@gmail.com", "rutik@gmail.com", "honey@gmail.com", "saumya@gmail.com", "sid@gmail.com", "utk@gmail.com", "sara@gmail.com", "dhruv@gmail.com", "ankush@gmail.com", "akansha@gmail.com"
]
college = [
    "dypcoe","dypiemr"
]
branch = [
    "computer","information techology","production", "instrumentation", "entc","civil","mechanical"
]

live_backlog = [True, False]

for i in range(0,900):
    lis = [random.randint(100, 999), random.choice(list), random.choice(gender),
           random.randint(100000000000, 999999999999), random.choice(email), random.randint(1000000000, 9999999999),
           random.randint(1000000000, 9999999999), round(random.uniform(1, 100),2), round(random.uniform(1, 100),2),
           random.choice(college), random.choice(branch), round(random.uniform(1, 100),2), random.choice(live_backlog)]
    print(lis)


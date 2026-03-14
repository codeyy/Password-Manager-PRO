
def strength(password):
    entropy = 0

    import json
    data = 0
    with open("top30.json", 'r') as f:
        data = json.load(f)

    if password in data:
        entropy = data.index(password)
    else:
        char_set = sum(find_charset_size(password))

        from math import log2
        entropy = round(log2(char_set ** len(password)), 2)

    est_time = 0
    try:
        est_time = ((((2 ** entropy) / (10**11)))) 
    except OverflowError:
        est_time = "infinity"
    

    return (entropy, est_time)


def find_charset_size(password):
    char_set = [0, 0, 0, 0] #[ lowercase, uppercase, numbers, symbols ]

    for i in password:
        if 0 not in char_set:
            break
        if i.isalpha():
            if i.isupper() and char_set[0] == 0:
                char_set[0] = 26
            if i.islower() and char_set[1] == 0:
                char_set[1] = 26
        if i.isnumeric() and char_set[2] == 0:
            char_set[2] = 10
        if not i.isalnum() and char_set[3] == 0:
            char_set[3] = 32
    

    return tuple(char_set)

def retime(est_time):

    if est_time == "infinity" or est_time > 315360000000:
        sen = ("ETERNITY !!")
        score = 10
        return [sen, score]
    elif est_time < 1:
        sen = ("Instant!")
        score = 0
        return [sen, score]
    elif est_time < 60:
        sen = ("Less then a minute")
        score = 1
        return [sen, score]
    elif est_time < 86400:
        sen = ("about a Day")
        score = 2
        return [sen, score]
    elif est_time < 604800:
        sen = ("about a Week")
        score = 3
        return [sen, score]
    elif est_time < 2628000:
        sen = ("about a Month")
        score = 4
        return [sen, score]
    elif est_time < 31536000:
        sen = ("about a Year")
        score = 5
        return [sen, score]
    elif est_time < 315360000:
        sen = ("Decade ")
        score = 6
        return [sen, score]
    elif est_time < 3153600000:
        sen = ("DECADES ")
        score = 7
        return [sen, score]
    elif est_time < 31536000000:
        sen = ("HUNDREDS of YEARS ")
        score = 8
        return [sen, score]
    elif est_time < 315360000000:
        sen = ("THOUSANDS of YEARS ")
        score = 9
        return [sen, score]
    else:
        sen = ("Effectively uncrackable")
        score = 10
        return [sen, score]
    
        
def strength_check(password):

    stren = strength(password)
    entropy = stren[0]
    est_time = stren[1]
    time_score = retime(est_time)

    print(f"\n  Crack Time:                 {time_score[0]}" )
    print(f"  Password Entropy:           {entropy}")
    print(f"  Password Strength SCORE:    {time_score[1]}\n")

    return 0

def hasher(password, algo="sha256"):
    import hashlib
    
    password = password.encode("utf-8")
    hashed = 0
    if algo.lower() == "sha256":
        hashed = hashlib.sha256(password).hexdigest()
    elif algo.lower() == "sha224":
        hashed = hashlib.sha224(password).hexdigest()
    elif algo.lower() == "sha384":
        hashed = hashlib.sha384(password).hexdigest()
    elif algo.lower() == "sha512":
        hashed = hashlib.sha512(password).hexdigest()
    else:
        print("Algorithm unrecognizable")
        return

    print(f"\n  Hash:   {hashed}\n")
    return hashed

def verify(phash, password, algo):
    import hashlib
    password = password.encode("utf-8")
    hashed = 0
    if algo.lower() == "sha256":
        hashed = hashlib.sha256(password).hexdigest()
    elif algo.lower() == "sha224":
        hashed = hashlib.sha224(password).hexdigest()
    elif algo.lower() == "sha384":
        hashed = hashlib.sha384(password).hexdigest()
    elif algo.lower() == "sha512":
        hashed = hashlib.sha512(password).hexdigest()
    else:
        print("Algorithm unrecognizable")
        return

    return phash == hashed
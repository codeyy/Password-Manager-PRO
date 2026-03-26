
def strength(password):
    common_passwords = [
    "Password123!",
    "P@ssw0rd123",
    "P@ssw0rd1234",
    "P@ssw0rd12345",
    "P@ssw0rd123456",
    "Aa123456!",
    "Welcome123!",
    "Admin@123",
    "Summer2025!",
    "Spring2025!",
    "Winter2025!",
    "Fall2024!",
    "Qwerty123!",
    "Monkey123!",
    "Dragon123!",
    "Iloveyou1!",
    "Letmein123!",
    "Pass@123",
    "Aa@123456",
    "Changeme1!",
    "Password01!",
    "Abc@12345",
    "Admin123!",
    "Abc123Abc123!",
    "123!123!",
    "PasswordPassword",
    "AdminAdmin123",
    "Testing123!",
    "1122334455!!",
    "Login1234!",
    "Aaaaaa1!",
    "Pppasword123",
    "User12345678"
    "112233445566778899"
    "54321"
    "121212"
]
    
    password = password.strip()
    entropy = 0
    est_time = 0
    data = common_passwords

    if password in data:
        return (entropy, est_time)
    else:
        char_set = sum(find_charset_size(password))

        password = (has_repeating_characters(password)["deduplicated"])

        from math import log2
        entropy = round(len(password) * (log2(char_set)))  # round(log2(char_set ** len(password)), 2)

    try:
        est_time = ((2 ** entropy) / (10**11))
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
        sen = (f"  {round(est_time, 2)} Seconds.")
        score = 1
        return [sen, score]
    elif est_time < 3600:
        sen = (f"  {round((est_time/60), 2)} Minutes.")
        score = 2
        return [sen, score]
    elif est_time < 86400:
        sen = (f"  {round((est_time/ 3600), 2)} Hours")
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

def hasher(password, algorithm):
    algorithm = algorithm.lower().strip()

    import hashlib
    password = password.encode("utf-8")
    hashed = 0
    if algorithm == "sha256":
        hashed = hashlib.sha256(password).hexdigest()
    elif algorithm == "sha224":
        hashed = hashlib.sha224(password).hexdigest()
    elif algorithm == "sha384":
        hashed = hashlib.sha384(password).hexdigest()
    elif algorithm == "sha512":
        hashed = hashlib.sha512(password).hexdigest()
    else:
        #("Algorithm unrecognizable\n using sha256")
        hashed = hashlib.sha256(password).hexdigest()

    return hashed

#print(hasher("ajdn", "sha512"))

def verify(phash, password, algorithm):
    return phash == hasher(password, algorithm)


def has_repeating_characters(password):
    """
    This function scans through the password string to identify sequences of 
    consecutive identical characters. Any sequence with 3 or more consecutive 
    identical characters is flagged as a repeat.
        password (str): The password string to analyze for repeating characters
        dict: A dictionary containing:
            - 'has_repeats' (bool): True if password contains 3+ consecutive 
                                    identical characters, False otherwise
            - 'details' (list): List of integers representing the count of each 
                               repeating sequence (only sequences >= 3 are included)
            - 'deduplicated' (str): The password with all consecutive duplicate 
                                   characters collapsed into a single character
    Example:
        >>> has_repeating_characters("passs123wwww")
        {
            'has_repeats': True,
            'details': [4, 4],
            'deduplicated': 'pas123w'
        >>> has_repeating_characters("pass123")
        {
            'has_repeats': False,
            'details': [],
            'deduplicated': 'pas123'

    Check if password has repeating characters and return deduplicated version.
    
    Args:
        password: The password string to check
    
    Returns:
        Dictionary with 'has_repeats' (bool), 'details' (list of repeat counts),
        and 'deduplicated' (password with consecutive duplicates removed)
    """
    repeats = []
    deduplicated = []
    threshold = 4
    i = 0
    
    while i < len(password):
        count = 1
        while i + count < len(password) and password[i] == password[i + count]:
            count += 1
        
        if count >= threshold:
            repeats.append(count)
        
        deduplicated.append(password[i])
        print(password[i] * round(count/4))
        i += count
    
    return {
        'has_repeats': len(repeats) > 0,
        'details': repeats,
        'deduplicated': ''.join(deduplicated)
    }
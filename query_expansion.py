def expand_query(query):


    synonyms = {


        "leave":[
            "vacation",
            "holiday",
            "time off",
            "absence",
            "annual leave"
        ],


        "vacation":[
            "leave",
            "holiday",
            "time off"
        ],


        "salary":[
            "pay",
            "compensation",
            "income"
        ],


        "remote":[
            "work from home",
            "hybrid work",
            "telework"
        ],


        "security":[
            "password",
            "data protection",
            "information security"
        ]

    }



    expanded = query.lower()


    for word, related_words in synonyms.items():


        if word in query.lower():


            expanded += " " + " ".join(
                related_words
            )


    return expanded
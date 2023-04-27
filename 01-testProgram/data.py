"""
**********************************************************
*    ____                     __      ___       __       *
*   / __/_ _____ ___ _  ___  / /__   / _ \___ _/ /____ _ *
*  / _/ \ \ / _ `/  ' \/ _ \/ / -_) / // / _ `/ __/ _ `/ *
* /___//_\_\\_,_/_/_/_/ .__/_/\__/ /____/\_,_/\__/\_,_/  *
                   /_/                                   *
* v 1.1 written by Silvestro "pino" Di Pietro 2023       *
*  Example data                                          *
*                                                        *
* written by Silvestro 'pino' Di Pietro                  *
**********************************************************
"""

#asciiTable list
Reddit = [
    {
        "total_amount": 381150, "text": "Bull Gang (above +2.5%)", "vote_count": 6671, "user_amount": "none", "image_url": "none", "id": "19423491"
    },
    {
        "total_amount": 271830, "text": "Theta Gang (between +2.5% &amp; -2.5%)", "vote_count": 5217, "user_amount": "none", "image_url": "none", "id": "19423492"
    },
    {
        "total_amount": 151670, "text": "Bear Gang (below -2.5%)", "vote_count": 2820, "user_amount": "none", "image_url": "none", "id": "19423493"
    },
    {
        "total_amount": 109400, "text": "Very Green (Above +1.25%)", "vote_count": 1865, "user_amount": "none", "image_url": "none", "id": "19420602"
    },
    {
        "total_amount": 246740, "text": "Green (+0.5% to +1.25%)", "vote_count": 4804, "user_amount": "none", "image_url": "none", "id": "19420603"
    },
    {
        "total_amount": 164590, "text": "Flat (-0.5% to +0.5%)", "vote_count": 3515, "user_amount": "none", "image_url": "none", "id": "19420604"
    },
    {
        "total_amount": 190860, "text": "Red (-0.5% to -1.25%)", "vote_count": 3660, "user_amount": "none", "image_url": "none", "id": "19420605"
    },
    {
        "total_amount": 121320, "text": "Very Red (Below -1.25%)", "vote_count": 1900, "user_amount": "none", "image_url": "none", "id": "19420606"
    },
    {
        "total_amount": 760420, "text": "Green (+3.5% or above)", "vote_count": 13601, "user_amount": "none", "image_url": "none", "id": "19407234"
    },
    {
        "total_amount": 590530, "text": "Flat (-3.5% to +3.5%)", "vote_count": 11567, "user_amount": "none", "image_url": "none", "id": "19407235"
    },
    {
        "total_amount": 462800, "text": "Red (-3.5% or below)", "vote_count": 8453, "user_amount": "none", "image_url": "none", "id": "19407236"
    },
    {
        "total_amount": 170050, "text": "Bull Gang (above +2.5%)", "vote_count": 3212, "user_amount": "none", "image_url": "none", "id": "19404368"
    },
    {
        "total_amount": 435880, "text": "Theta Gang (between +2.5% &amp; -2.5%)", "vote_count": 9198, "user_amount": "none", "image_url": "none", "id": "19404369"
    },
    {
        "total_amount": 561870, "text": "Bear Gang (below -2.5%)", "vote_count": 10529, "user_amount": "none", "image_url": "none", "id": "19404370"
    },
    {
        "total_amount": 608400, "text": "Bull Gang (above +2.5%)", "vote_count": 10582, "user_amount": "none", "image_url": "none", "id": "19398909"
    },
    {
        "total_amount": 536810, "text": "Theta Gang (between +2.5% &amp; -2.5%)", "vote_count": 10307, "user_amount": "none", "image_url": "none", "id": "19398910"
    },
    {
        "total_amount": 410650, "text": "Bear Gang (below -2.5%)", "vote_count": 7244, "user_amount": "none", "image_url": "none", "id": "19398911"
    },
    {
        "total_amount": 120120, "text": "Very Green (Above +1.25%)", "vote_count": 2017, "user_amount": "none", "image_url": "none", "id": "19397395"
    },
    {
        "total_amount": 312060, "text": "Green (+0.5% to +1.25%)", "vote_count": 6245, "user_amount": "none", "image_url": "none", "id": "19397396"
    },
    {
        "total_amount": 232170, "text": " Flat (-0.5% to +0.5%)", "vote_count": 5204, "user_amount": "none", "image_url": "none", "id": "19397397"
    },
    {
        "total_amount": 258450, "text": "Red (-0.5% to -1.25%)", "vote_count": 5128, "user_amount": "none", "image_url": "none", "id": "19397398"
    },
    {
        "total_amount": 128840, "text": "Very Red (Below -1.25%)", "vote_count": 2082, "user_amount": "none", "image_url": "none", "id": "19397399"
    },
    {
        "total_amount": 515470, "text": "Green (+5% or above)", "vote_count": 9875, "user_amount": "none", "image_url": "none", "id": "19384883"
    },
    {
        "total_amount": 709010, "text": "Flat (-5% to +5%)", "vote_count": 14284, "user_amount": "none", "image_url": "none", "id": "19384884"
    },
    {
        "total_amount": 615520, "text": "Red (-5% or below)", "vote_count": 11605, "user_amount": "none", "image_url": "none", "id": "19384885"
    },
    {
        "total_amount": 795700, "text": "Bull Gang (above +2.5%)", "vote_count": 14390, "user_amount": "none", "image_url": "none", "id": "19378464"
    },
    {
        "total_amount": 810780, "text": "Theta Gang (between +2.5% &amp; -2.5%)", "vote_count": 15966, "user_amount": "none", "image_url": "none", "id": "19378465"
    },
    {
        "total_amount": 228840, "text": "Bear Gang (below -2.5%)", "vote_count": 4435, "user_amount": "none", "image_url": "none", "id": "19378466"
    },

    {
        "total_amount": 143450, "text": "Very Green (Above +1.25%)", "vote_count": 2501, "user_amount": "none", "image_url": "none", "id": "19375445"
    },
    {
        "total_amount": 332010, "text": "Green (+0.5% to +1.25%)", "vote_count": 6623, "user_amount": "none", "image_url": "none", "id": "19375446"
    },
    {
        "total_amount": 233940, "text": " Flat (-0.5% to +0.5%)", "vote_count": 5129, "user_amount": "none", "image_url": "none", "id": "19375447"
    },
    {
        "total_amount": 247910, "text": " Red (-0.5% to -1.25%)", "vote_count": 4831, "user_amount": "none", "image_url": "none", "id": "19375448"
    },
    {
        "total_amount": 124670, "text": "Very Red (Below -1.25%)", "vote_count": 2046, "user_amount": "none", "image_url": "none", "id": "19375449"
    },
    {
        "total_amount": 528540, "text": "Green (+4% or above)", "vote_count": 9996, "user_amount": "none", "image_url": "none", "id": "19366740"
    },
    {
        "total_amount": 934250, "text": "Flat (-4% to +4%)", "vote_count": 18073, "user_amount": "none", "image_url": "none", "id": "19366741"
    },
    {
        "total_amount": 500590, "text": "Red (-4% or below)", "vote_count": 9549, "user_amount": "none", "image_url": "none", "id": "19366742"
    },

    {
        "total_amount": 490480, "text": "Green (+3.5% or above)", "vote_count": 9142, "user_amount": "none", "image_url": "none", "id": "19362078"
    },
    {
        "total_amount": 692770, "text": "Flat (-3.5% to +3.5%)", "vote_count": 13861, "user_amount": "none", "image_url": "none", "id": "19362079"
    },
    {
        "total_amount": 461090, "text": "Red (-3.5% or below)", "vote_count": 8910, "user_amount": "none", "image_url": "none", "id": "19362080"
    }
]

asciiTableExample=[
    {
        'key':'val'
    },
    {
        'key':'val1'
    },
    {
        'key':'val2'
    },
    {
        'key':'valN'
    }
]
itNames=[
    {
        'name':'Pino',
        'role':'software architect',
        'languages':'php c c++ python',
        'building':'bld4',
        'floor': '0',
        'room' : '14'
    },
    {
        'name':'Cosimo',
        'role':'junior engineer',
        'languages':'php python',
        'building':'bld4',
        'floor': '0',
        'room' : '14'
    },
    {
        'name':'Salvatore',
        'role':'senior sofware engineer',
        'languages':'php python',
        'building':'bld4',
        'floor': '0',
        'room' : '14'
    },
     {
        'name':'Cirillo',
        'role':'unqualified',
        'languages':'none',
        'building':'none',
        'floor': 'none',
        'room' : 'none'
    },
    {
        'name':'Claudio',
        'role':'junior dba',
        'languages':'sql apex',
        'building':'bld4',
        'floor': '0',
        'room' : '14'
    },
  {
        'name':'Manuelo',
        'role':'senior help desk',
        'languages':'none',
        'building':'bld4',
        'floor': '0',
        'room' : '13'
    },
    {
        'name':'Igal',
        'role':'it manager',
        'languages':'c c++',
        'building':'bld4',
        'floor': '0',
        'room' : '12'
    }
]

tvShow=[
    {
        "id": 5451,
        "url": "https://www.tvmaze.com/shows/5451/golden-girls",
        "name": "Golden Girls",
        "type": "Scripted",
        "language": "Dutch",
        "genres": "Drama",
        "status": "Ended",
        "runtime": 30,
        "averageRuntime": 30,
        "premiered": "2012-08-25",
        "ended": "2012-11-03",
        "rating": 5.3,
        "weight": 80,
        "network": "RTL4"
    },
    {
        "id": 722,
        "url": "https://www.tvmaze.com/shows/722/the-golden-girls",
        "name": "The Golden Girls",
        "type": "Scripted",
        "language": "English",
        "genres": "Drama",
        "status": "Ended",
        "runtime": 30,
        "averageRuntime": 30,
        "premiered": "1985-09-14",
        "ended": "1992-05-09",
        "rating": 8.3,
        "weight": 93,
        "network": "NBC",
       
    },
    {
        "id": 57291,
        "url": "https://www.tvmaze.com/shows/57291/the-holden-girls-mandy-myrtle",
        "name": "The Holden Girls: Mandy & Myrtle",
        "type": "Scripted",
        "language": "English",
        "genres": "Comedy",
        "status": "Running",
        "runtime": "null",
        "averageRuntime": 32,
        "premiered": "2021-09-07",
        "ended": "1999-05-09",
        "rating": 9.3,
        "weight": 41,
        "network": "E4"
    }
]
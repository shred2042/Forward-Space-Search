import FWD_Space_Search

"""
Tests
"""
Test1 = {
"wormholes": [("S0", "S1"), ("S1", "S2"), ("S1", "S3"), ("S1", "S4"),
("S2", "S3"), ("S3", "S4"), ("S4", "S5"), ("S4", "S6"), ("S6", "Sol")],
"start": "S0",
"gas": ["S1", "S2", "S3", "S5"],
"time": "7",
"packages": [("Pack1", "S0", "S1", "1"), ("Pack2", "S1", "S2", "3"),
("Pack3", "S1", "S3", "2"), ("Pack4", "S4", "S5", "3")]
}

Test2 = {
"wormholes": [ ("S0", "S1"), ("S1", "S2"), ("S2", "S6"), ("S1", "S3"),
("S3", "S4"), ("S4", "S5"), ("S5", "S6"), ("S6", "Sol") ],
"start": "S0",
"gas": [ "S1", "S2", "S3", "S5" ],
"time": "6",
"packages": [ ("Pack1", "S0", "S1", "1"), ("Pack2", "S1", "S3", "2"),
("Pack3", "S3", "S5", "2"), ("Pack4", "S1", "S2", "1"),
("Pack5", "S2", "S6", "50") ]
}

Test3 = {
"wormholes": [ ("S0", "S1"), ("S1", "S2"), ("S2", "S6"), ("S1", "S3"),
("S3", "S4"), ("S4", "S5"), ("S5", "S6"), ("S6", "Sol") ],
"start": "S0",
"gas": [ "S1", "S2", "S3", "S5" ],
"time": "15",
"packages": [ ("Pack1", "S0", "S1", "1"), ("Pack2", "S1", "S3", "2"),
("Pack3", "S3", "S5", "1"), ("Pack4", "S1", "S2", "1"),
("Pack5", "S2", "S6", "50") ]
}

Test4 = {
"wormholes": [ ("S0", "S1"), ("S1", "S2"), ("S2", "S3" ), ("S2", "S4"),
("S4", "S5" ), ("S5", "S6"), ("S6", "Sol") ],
"start": "S0",
"gas": [ "S1", "S3", "S5" ],
"time": "10",
"packages": [ ("Pack1", "S0", "S1", "2"), ("Pack2", "S2", "S5", "1"),
("Pack3", "S0", "S5", "1"), ("Pack4", "S2", "S3", "3") ]
}

Test5 = {
"wormholes": [ ("Arcturus", "Ross-154"), ("Ross-154", "Lacaille-8760"),
("Ross-154", "Formalhaut"), ("Ross-154", "Barnard-s-Star"),
("Barnard-s-Star", "Luyten"), ("Barna" "rd-s-St" "ar", "Luyten-789-6"),
("Luyten", "Ross-780"), ("Luyten-789-6", "LET-118"),
("LET-118", "Epsilon-Eridani"), ("Formalhaut", "Lacaille-8760"),
("Formalhaut", "Lacaille-9352"), ("Lacaille-9352", "Lalande-25372"),
("Lalande-25372", "Epsilon-Indi"), ("Epsilon-Indi", "Alpha-Centauri"),
("Alfa-Centauri", "Sol"), ("Alfa-Centauri", "Wolf-359"),
("Wolf-359", "Sol"), ("Wolf-359", "Sirius"),
("Wolf-359", "Epsilon-Eridani"), ("Sirius", "Epsilon-Eridani"),
("Epsilon-Eridani", "UV-Ceti"), ("UV-Ceti", "Sol") ],
"start": "Arcturus",
"gas": [ "Ross-154", "Barnard-s-Star", "Formalhaut", "Sirius" ],
"time": "30",
"packages": [ ("Janice-Perry", "Ross-154", "Ross-154", "2"),
("Jack-Nakamichi", "Ross-154", "Lacaille-8760", "4"),
("Mr-Gonzales", "Formalhaut", "Lalande-25372", "5"),
("Merchant-Baker", "Ross-154", "Ross-780", "10"),
("Ami-Soze", "Ross-154", "LET-118", "5"),
("G-Sutherland", "Formalhaut", "Arcturus", "4"),
("Tom-Major", "Lalande-25372", "Lacaille-8760", "5") ]
}


"""
Test script
"""
for i in [Test1, Test2, Test3, Test4, Test5]:
    x = makePlan(i)
    print(x)
    if x != False:
        print(len(x))

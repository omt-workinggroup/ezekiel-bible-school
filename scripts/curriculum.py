"""Ezekiel Bible Institute curriculum framework.

Source: Ezekiel_Bible_Institute_Curriculum.pdf (also published at
/ezekiel-bible-institute-curriculum.pdf). Keep the two in step.
"""

MOTTO = ("Presenting every believer mature in Christ.", "Colossians 1:28")

PATHWAY = ["Know Christ", "Understand truth", "Become like Christ", "Serve faithfully", "Multiply"]

PHILOSOPHY = (
    "The institute is designed to move students beyond the accumulation of biblical information "
    "toward integrated Christian formation. The goal is knowledge that becomes conviction, character, "
    "competence, faithful service and multiplication."
)

DIMENSIONS = [
    ("Knowledge", "What do I understand?"),
    ("Character", "What am I becoming?"),
    ("Competence", "What can I faithfully do?"),
    ("Calling", "What has God entrusted me to accomplish?"),
]

# Each course: (code, title, topics or "")
LEVELS = [
    {
        "slug": "certificate",
        "n": 1,
        "name": "Certificate in Christian Foundations",
        "short": "Certificate",
        "stage": "undergraduate",
        "length": "1 year",
        "semesters": 2,
        "purpose": "Establish new and growing believers in the fundamental truths of Christianity.",
        "outcome": "I know the foundations of the faith.",
        "terms": [
            ("Semester 1", [
                ("CF 101", "The Gospel and Salvation", "Gospel, sin, repentance, faith, grace, justification, regeneration, new birth, adoption, eternal life, assurance"),
                ("CF 102", "The Person of Jesus Christ", "Deity and humanity, incarnation, virgin birth, sinlessness, death, resurrection, ascension, lordship"),
                ("CF 103", "The Holy Spirit", "Person and deity, indwelling, regeneration, sanctification, filling, gifts, fruit, guidance, witness"),
                ("CF 104", "Introduction to the Bible", "Inspiration, authority, canon, Old and New Testaments, covenants, revelation, illumination, reading Scripture"),
            ]),
            ("Semester 2", [
                ("CF 105", "Christian Identity and Sonship", "New creation, identity in Christ, righteousness, adoption, sonship, union with Christ, freedom"),
                ("CF 106", "The Christian Life", "Faith, prayer, worship, holiness, love, forgiveness, humility, wisdom, stewardship"),
                ("CF 107", "Introduction to Spiritual Growth", "New birth, infancy, growth, maturity, character, spiritual disciplines, stability, responsibility"),
                ("CF 108", "Introduction to Christian Service", "Calling, service, gifts, faithfulness, character, servanthood, evangelism, discipleship"),
            ]),
        ],
    },
    {
        "slug": "diploma",
        "n": 2,
        "name": "Diploma in Christian Ministry & Biblical Studies",
        "short": "Diploma",
        "stage": "undergraduate",
        "length": "1 year",
        "semesters": 2,
        "purpose": "Move students from foundational Christianity into responsible biblical understanding and practical ministry.",
        "outcome": "I understand Scripture and can practise the Christian life.",
        "terms": [
            ("Semester 1", [
                ("DM 201", "Principles of Biblical Interpretation", "Historical, literary, immediate and canonical context, genre, translation, exegesis, eisegesis, application"),
                ("DM 202", "Biblical Theology", "Creation, fall, promise, covenant, kingdom, Messiah, redemption, New Covenant, church, new creation"),
                ("DM 203", "Spiritual Maturity", "Nēpios, paidion, neaniskos, patēr; spiritual understanding, character, stability, responsibility, reproduction"),
                ("DM 204", "Knowing God", "Eidō, ginōskō, gnōsis, epignōsis; knowledge of God, revelation, fellowship, experiential knowledge"),
            ]),
            ("Semester 2", [
                ("DM 205", "Introduction to Christian Doctrine", "The doctrines of God, Christ, the Holy Spirit, salvation, the church and last things"),
                ("DM 206", "Prayer and Spiritual Life", "Fellowship with God, petition, thanksgiving, intercession, corporate prayer, fasting, spiritual warfare"),
                ("DM 207", "Evangelism and Discipleship", "Great Commission, gospel presentation, personal evangelism, follow-up, discipleship, mentoring, multiplication"),
                ("DM 208", "Ministry Practicum I", "Bible study, evangelism, prayer leadership, discipleship, supervised ministry reflection"),
            ]),
        ],
    },
    {
        "slug": "bachelor",
        "n": 3,
        "name": "Bachelor of Theology / Christian Ministry",
        "short": "Bachelor",
        "stage": "undergraduate",
        "length": "3 years",
        "semesters": 6,
        "purpose": "Equip students to interpret Scripture responsibly, understand doctrine, develop maturity and serve effectively.",
        "outcome": "I can interpret Scripture, understand theology and serve effectively.",
        "terms": [
            ("Year 1 · Semester 1", [("BT 301", "Old Testament Survey", ""), ("BT 302", "New Testament Survey", ""), ("BT 303", "Biblical Hermeneutics", ""), ("BT 304", "Christian Doctrine I: Doctrine of God", ""), ("BT 305", "Spiritual Formation I", ""), ("BT 306", "Introduction to Christian Ministry", "")]),
            ("Year 1 · Semester 2", [("BT 307", "Pentateuch and Historical Books", ""), ("BT 308", "Gospels and Acts", ""), ("BT 309", "Christian Doctrine II: Christology", ""), ("BT 310", "Christian Doctrine III: Pneumatology", ""), ("BT 311", "Prayer and Intercession", ""), ("BT 312", "Evangelism and Discipleship", "")]),
            ("Year 2 · Semester 3", [("BT 401", "Prophets and Wisdom Literature", ""), ("BT 402", "Pauline Epistles", ""), ("BT 403", "General Epistles and Revelation", ""), ("BT 404", "Soteriology", ""), ("BT 405", "Spiritual Growth and Christian Maturity", ""), ("BT 406", "Spiritual Gifts and Calling", "")]),
            ("Year 2 · Semester 4", [("BT 407", "Ecclesiology", ""), ("BT 408", "Eschatology", ""), ("BT 409", "Biblical Theology", ""), ("BT 410", "Christian Ethics", ""), ("BT 411", "Christian Leadership", ""), ("BT 412", "Preaching and Bible Teaching I", "")]),
            ("Year 3 · Semester 5", [("BT 501", "Christ-Centred Preaching II", ""), ("BT 502", "Pastoral Theology", ""), ("BT 503", "Church Leadership and Governance", ""), ("BT 504", "Church Organisation and Structure", ""), ("BT 505", "Ministry Administration", ""), ("BT 506", "Missions and Church Planting", "")]),
            ("Year 3 · Semester 6", [("BT 507", "Biblical Greek I", ""), ("BT 508", "Biblical Greek II", ""), ("BT 509", "Hebrew I", "Elective"), ("BT 510", "Christian Counselling", ""), ("BT 511", "Ministry Ethics", ""), ("BT 512", "Bachelor Ministry Research Project", "")]),
        ],
    },
    {
        "slug": "master",
        "n": 4,
        "name": "Master of Theology / Christian Ministry",
        "short": "Master",
        "stage": "postgraduate",
        "length": "2 years",
        "semesters": 4,
        "purpose": "Move students into advanced critical investigation, theological articulation, research and application.",
        "outcome": "I can critically investigate, articulate and apply theological truth.",
        "terms": [
            ("Year 1 · Semester 1", [("MT 601", "Advanced Hermeneutics", "Advanced exegesis and hermeneutical models"), ("MT 602", "Advanced Biblical Theology", ""), ("MT 603", "Advanced Systematic Theology I", ""), ("MT 604", "Theology of Christ and Salvation", ""), ("MT 605", "Research Methods in Biblical Studies", ""), ("MT 606", "Biblical Greek III / Advanced Greek", "")]),
            ("Year 1 · Semester 2", [("MT 607", "Advanced Systematic Theology II", ""), ("MT 608", "Advanced Pneumatology", ""), ("MT 609", "Advanced Ecclesiology", ""), ("MT 610", "Advanced Eschatology", ""), ("MT 611", "Theology and Christian Ethics", ""), ("MT 612", "Biblical Hebrew II", "")]),
            ("Year 2 · Semester 3 · Specialisation", [
                ("MT 701–704", "Biblical Studies", "Advanced Old Testament Studies, Advanced New Testament Studies, Advanced Exegesis, Biblical Theology Seminar"),
                ("MT 711–714", "Theology", "Advanced Systematic Theology, Historical Theology, Contemporary Theology, Theology and Culture"),
                ("MT 721–724", "Christian Ministry", "Advanced Pastoral Ministry, Advanced Christian Leadership, Church Development, Ministry Formation"),
                ("MT 731–734", "Church Structure & Administration", "Theology of Church Organisation, Church Systems, Leadership Development Systems, Strategic Church Development"),
            ]),
            ("Year 2 · Semester 4", [("MT 741", "Advanced Ministry Practicum", ""), ("MT 742", "Research Seminar", ""), ("MT 743", "Master's Thesis", ""), ("MT 744", "Thesis Defence", "")]),
        ],
    },
    {
        "slug": "dmin",
        "n": 5,
        "name": "Doctor of Ministry (DMin)",
        "short": "DMin",
        "stage": "postgraduate",
        "length": "3 years",
        "semesters": 6,
        "purpose": "A professional doctorate integrating theological research with ministry transformation and practical solutions.",
        "outcome": "I can use theological knowledge and research to transform ministry practice.",
        "terms": [
            ("Year 1 · Semester 1", [("DMN 801", "Advanced Theology of Ministry", ""), ("DMN 802", "Spiritual Formation and Ministerial Character", ""), ("DMN 803", "Advanced Biblical Leadership", ""), ("DMN 804", "Ministry Research Methods", "")]),
            ("Year 1 · Semester 2", [("DMN 805", "Church Health and Development", ""), ("DMN 806", "Strategic Ministry Leadership", ""), ("DMN 807", "Organisational Systems in the Church", ""), ("DMN 808", "Ministry Evaluation", "")]),
            ("Year 2 · Semester 3", [("DMN 901", "Advanced Discipleship Systems", ""), ("DMN 902", "Church Growth and Church Health", ""), ("DMN 903", "Leadership Development and Succession", ""), ("DMN 904", "Ministry Innovation", "")]),
            ("Year 2 · Semester 4", [("DMN 905", "Advanced Pastoral Theology", ""), ("DMN 906", "Spiritual Formation Systems", ""), ("DMN 907", "Missions and Community Transformation", ""), ("DMN 908", "Ministry Case Studies", "")]),
            ("Year 3 · Semester 5", [("DMN 1001", "Doctoral Research Seminar", ""), ("DMN 1002", "Ministry Project Design", ""), ("DMN 1003", "Field Research", ""), ("DMN 1004", "Ministry Intervention", "")]),
            ("Year 3 · Semester 6", [("DMN 1005", "Doctoral Ministry Project", ""), ("DMN 1006", "Dissertation / Project Writing", ""), ("DMN 1007", "Oral Defence", ""), ("DMN 1008", "Ministry Portfolio", "")]),
        ],
    },
    {
        "slug": "phd",
        "n": 6,
        "name": "PhD in Biblical & Theological Studies",
        "short": "PhD",
        "stage": "postgraduate",
        "length": "3–5 years",
        "semesters": None,
        "purpose": "Prepare scholars capable of advanced biblical and theological research and an original contribution to knowledge.",
        "outcome": "I can conduct original research and contribute new knowledge.",
        "terms": [
            ("Year 1 · Semester 1", [("PHD 1101", "Philosophy of Biblical and Theological Research", ""), ("PHD 1102", "Advanced Research Methodology", ""), ("PHD 1103", "Advanced Greek", ""), ("PHD 1104", "Advanced Hebrew", ""), ("PHD 1105", "History of Biblical Interpretation", "")]),
            ("Year 1 · Semester 2", [("PHD 1106", "Advanced Biblical Theology", ""), ("PHD 1107", "Advanced Systematic Theology", ""), ("PHD 1108", "Historical Theology", ""), ("PHD 1109", "Contemporary Theological Scholarship", ""), ("PHD 1110", "Doctoral Research Seminar I", "")]),
            ("Year 2 · Specialisation tracks", [
                ("Track A", "Old Testament", "Hebrew exegesis, Old Testament theology, Ancient Near Eastern context"),
                ("Track B", "New Testament", "Greek exegesis, New Testament theology, Pauline studies, Gospels, Johannine studies"),
                ("Track C", "Systematic Theology", "Doctrine of God, Christology, Pneumatology, Soteriology, Ecclesiology, Eschatology"),
                ("Track D", "Historical Theology", "Early Church, Patristic theology, Reformation, modern theology, Pentecostal and Charismatic theology"),
                ("Track E", "Practical Theology", "Church leadership, discipleship, spiritual formation, ministry development, ecclesial structures, pastoral theology"),
            ]),
            ("Year 2 · Semester 4", [("PHD 1201", "Doctoral Research Seminar II", ""), ("PHD 1202", "Research Proposal Development", ""), ("PHD 1203", "Comprehensive Examinations", ""), ("PHD 1204", "Language Examinations", "")]),
            ("Years 3–5 · Original research", [("PHD 1301", "Doctoral Dissertation", "Proposal, approval, research, analysis, writing, submission"), ("PHD 1302", "Oral Defence", "External examination, defence, revision and final approval")]),
        ],
    },
]

PRACTICUM = [
    "Bible-study projects",
    "Sermon and teaching practicum",
    "Evangelism",
    "Prayer leadership",
    "Discipleship",
    "A ministry problem-solving project",
    "A final portfolio showing knowledge, character, skill, service and fruit",
]

GRADUATE_PROFILE = (
    "I know Christ, understand His Word, understand who I am in Christ, live according to His character, "
    "interpret Scripture responsibly, discern sound doctrine, pray effectively, disciple others, serve "
    "according to my calling, and contribute faithfully to the mission and health of the local church."
)

AIM = (
    "Ezekiel Bible Institute exists to form men and women who know Christ, understand Scripture, embody "
    "Christian character, serve according to their calling, build healthy churches, develop others, and "
    "faithfully advance the mission of Christ."
)

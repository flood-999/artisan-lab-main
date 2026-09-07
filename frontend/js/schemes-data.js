/**
 * NIRMAAN - Government Schemes Data
 *
 * Real content provided directly by the artisan/product owner (Hindi
 * source). Each scheme's `id` number (1-5) matches the numbering of the
 * narrated audio files in /frontend/audio/schemes/ EXACTLY — do not
 * reorder this array or renumber ids without also renaming the audio
 * files, or the voice-over will play the wrong scheme.
 *
 * Audio files: scheme_{id}_hi.mp3 / scheme_{id}_en.mp3
 */
export const SCHEMES = [
  {
    id: 1,
    icon: "🛠️",
    title_en: "PM Vishwakarma Yojana",
    title_hi: "प्रधानमंत्री विश्वकर्मा योजना",
    oneliner_en: "For artisans working with their hands and traditional tools across 18 trades.",
    oneliner_hi: "उन कारीगरों के लिए जो अपने हाथों और पारंपरिक औजारों से 18 पारंपरिक कामों में से कोई काम करते हैं।",
    description_en: "This scheme is for artisans who work with their hands and traditional tools, covering 18 traditional trades such as carpenters, potters, tailors, blacksmiths, cobblers, goldsmiths, sculptors, masons, basket/mat/broom makers, doll and toy makers, barbers, garland makers, washermen, fishing net makers, boat makers, weapon makers, and hammer/tool makers. Apply at your nearest Common Service Centre (CSC) using your Aadhaar card.",
    description_hi: "यह योजना उन कारीगरों के लिए है जो अपने हाथों और पारंपरिक औजारों से काम करते हैं, इसमें कुल 18 पारंपरिक काम शामिल हैं जैसे बढ़ई, कुम्हार, दर्जी, लोहार, मोची, सुनार, मूर्तिकार, राजमिस्त्री, टोकरी, चटाई और झाड़ू बनाने वाले, गुड़िया और खिलौने बनाने वाले, नाई, मालाकार, धोबी, मछली पकड़ने का जाल बनाने वाले, नाव बनाने वाले, अस्त्र-शस्त्र बनाने वाले, हथौड़ा और औजार बनाने वाले। अपने नजदीकी कॉमन सर्विस सेंटर (CSC) पर जाकर आधार कार्ड की मदद से पंजीकरण कर सकते हैं।",
    eligibility_en: [
      "Age 18 years or above",
      "Must work in one of the 18 recognized traditional trades",
      "Only one person per family can apply",
      "What you get: free training, ₹500/day during training, up to ₹15,000 to buy tools, and a collateral-free loan of up to ₹3 lakh to grow your work"
    ],
    eligibility_hi: [
      "18 साल या उससे अधिक उम्र का व्यक्ति",
      "जो इन 18 कामों में से कोई काम करता हो",
      "एक परिवार से केवल एक व्यक्ति आवेदन कर सकता है",
      "क्या मिलेगा: मुफ्त प्रशिक्षण, प्रशिक्षण के दौरान ₹500 प्रतिदिन, औजार खरीदने के लिए ₹15,000 तक की मदद और अपना काम बढ़ाने के लिए ₹3 लाख तक का बिना गारंटी वाला ऋण"
    ]
  },
  {
    id: 2,
    icon: "🏬",
    title_en: "National Handicrafts Development Programme (NHDP) & Ambedkar Hastshilp Vikas Yojana (AHVY)",
    title_hi: "राष्ट्रीय हस्तशिल्प विकास कार्यक्रम (NHDP) और अंबेडकर हस्तशिल्प विकास योजना (AHVY)",
    oneliner_en: "Helps handicraft artisans improve their work and earn more through training, design, and marketing support.",
    oneliner_hi: "हस्तशिल्प का काम करने वाले कारीगरों को अपना काम बेहतर बनाने और ज्यादा कमाई करने में मदद करती हैं।",
    description_en: "These schemes help handicraft artisans improve their work and earn more, providing training, better designs, new tools, technology, and help selling goods. Artisans can register on the official India Handmade portal; some benefits are available through an artisan group or organization.",
    description_hi: "ये योजनाएँ हस्तशिल्प का काम करने वाले कारीगरों को अपना काम बेहतर बनाने और ज्यादा कमाई करने में मदद करती हैं। इसमें प्रशिक्षण, बेहतर डिजाइन, नए औजार, तकनीक और सामान बेचने में मदद दी जाती है। कारीगर आधिकारिक भारतीय हस्तशिल्प पोर्टल पर पंजीकरण कर सकते हैं।",
    eligibility_en: [
      "Handicraft artisans and eligible artisan groups (different benefits for each)",
      "Register on the official India Handmade portal; some facilities need application through an artisan group/organization",
      "What you get: skill training, help creating new/better designs, modern tools & technology, chances to take part in exhibitions, and support selling and promoting your goods"
    ],
    eligibility_hi: [
      "हस्तशिल्प का काम करने वाले कारीगर और योग्य कारीगर समूह इसके अलग-अलग लाभ ले सकते हैं",
      "आधिकारिक भारतीय हस्तशिल्प पोर्टल पर पंजीकरण; कुछ सुविधाओं के लिए कारीगर समूह या संस्था के माध्यम से आवेदन",
      "क्या मिलेगा: काम का प्रशिक्षण, नए और बेहतर डिजाइन बनाने में मदद, आधुनिक औजार और तकनीक, प्रदर्शनियों में भाग लेने का मौका और अपने सामान की बिक्री व प्रचार में सहायता"
    ]
  },
  {
    id: 3,
    icon: "🪪",
    title_en: "Pehchan Artisan ID Card",
    title_hi: "पहचान कारीगर पहचान पत्र",
    oneliner_en: "Official government ID card for handicraft artisans, making it easier to access other schemes.",
    oneliner_hi: "हस्तशिल्प कारीगरों के लिए सरकार द्वारा दिया जाने वाला आधिकारिक पहचान पत्र।",
    description_en: "The Pehchan card is an official identity card given by the government to handicraft artisans. It creates a government record of the artisan and makes it easier to access various government schemes. Register on the official India Handmade website with your name, date of birth, state, district, and mobile number.",
    description_hi: "पहचान कार्ड हस्तशिल्प कारीगरों के लिए सरकार द्वारा दिया जाने वाला आधिकारिक पहचान पत्र है। इससे सरकार के पास कारीगर का रिकॉर्ड बनता है और अलग-अलग सरकारी योजनाओं का लाभ लेना आसान होता है। आधिकारिक भारतीय हस्तशिल्प वेबसाइट पर जाकर अपना नाम, जन्मतिथि, राज्य, जिला और मोबाइल नंबर जैसी जानकारी देकर पंजीकरण किया जा सकता है।",
    eligibility_en: [
      "Any person who does handicraft work and meets the artisan registration requirements",
      "Register on the official India Handmade website with name, date of birth, state, district, and mobile number",
      "What you get: official government recognition, and easier access to training, exhibitions, government schemes, and other facilities"
    ],
    eligibility_hi: [
      "जो व्यक्ति हस्तशिल्प का काम करता है और कारीगर पंजीकरण की जरूरी शर्तें पूरी करता है",
      "आधिकारिक भारतीय हस्तशिल्प वेबसाइट पर नाम, जन्मतिथि, राज्य, जिला और मोबाइल नंबर देकर पंजीकरण",
      "क्या मिलेगा: कारीगर को सरकारी पहचान मिलती है और प्रशिक्षण, प्रदर्शनियों, सरकारी योजनाओं तथा दूसरी सुविधाओं तक पहुंच आसान हो जाती है"
    ]
  },
  {
    id: 4,
    icon: "💳",
    title_en: "PM Mudra Yojana (PMMY)",
    title_hi: "प्रधानमंत्री मुद्रा योजना (PMMY)",
    oneliner_en: "Loans to start or grow a small business — buy tools, raw material, or expand your craft.",
    oneliner_hi: "छोटे कारोबार को शुरू करने या बढ़ाने के लिए ऋण, बिना किसी संपत्ति को गारंटी के रूप में दिए।",
    description_en: "This scheme helps small businesses get loans to start or grow. Artisans can use this money to buy tools, purchase raw material, or expand their business. Apply through a bank, NBFC, or microfinance institution.",
    description_hi: "यह योजना छोटे कारोबार को शुरू करने या बढ़ाने के लिए ऋण लेने में मदद करती है। कारीगर इस पैसे का इस्तेमाल औजार खरीदने, कच्चा माल लेने या अपना कारोबार बढ़ाने के लिए कर सकते हैं। बैंक, एनबीएफसी या माइक्रोफाइनेंस संस्था के माध्यम से आवेदन किया जा सकता है।",
    eligibility_en: [
      "Small business owners and eligible manufacturing, trading, or service businesses",
      "Apply through a bank, NBFC, or microfinance institution",
      "What you get: Shishu — up to ₹50,000, Kishor — up to ₹5 lakh, Tarun — up to ₹10 lakh, Tarun Plus (for eligible beneficiaries) — up to ₹20 lakh. Usually no collateral/property required as guarantee."
    ],
    eligibility_hi: [
      "छोटे कारोबार करने वाले और योग्य निर्माण, व्यापार या सेवा से जुड़े व्यवसाय",
      "बैंक, एनबीएफसी या माइक्रोफाइनेंस संस्था के माध्यम से आवेदन",
      "क्या मिलेगा: शिशु के तहत ₹50,000 तक, किशोर के तहत ₹5 लाख तक, तरुण के तहत ₹10 लाख तक और योग्य तरुण लाभार्थियों को तरुण प्लस के तहत ₹20 लाख तक। इसके लिए आमतौर पर किसी संपत्ति को गारंटी के रूप में देने की जरूरत नहीं होती।"
    ]
  },
  {
    id: 5,
    icon: "🏘️",
    title_en: "Comprehensive Handicrafts Cluster Development Scheme (CHCDS)",
    title_hi: "व्यापक हस्तशिल्प क्लस्टर विकास योजना (CHCDS)",
    oneliner_en: "Develops whole artisan clusters — shared facilities, machines, raw material, and market access.",
    oneliner_hi: "बहुत सारे हस्तशिल्प कारीगर एक साथ काम करते हैं, ऐसी जगहों के विकास के लिए।",
    description_en: "This scheme is for developing places where many handicraft artisans work together, aiming to improve the entire artisan cluster and its working facilities. This is mainly for artisan groups and handicraft clusters, not for individual loans. Apply through an artisan group or related organization, submitting an application/proposal to the Handicrafts department — contact the organization present in your district.",
    description_hi: "यह योजना उन जगहों के विकास के लिए है जहाँ बहुत सारे हस्तशिल्प कारीगर एक साथ काम करते हैं। इसका उद्देश्य पूरे कारीगर समूह और उनके काम करने की सुविधाओं को बेहतर बनाना है। यह मुख्य रूप से कारीगर समूहों और हस्तशिल्प समूहों के लिए है, न कि किसी एक कारीगर को व्यक्तिगत ऋण देने के लिए। कारीगर समूह या संबंधित संस्था के माध्यम से हस्तशिल्प विभाग के पास आवेदन या प्रस्ताव दिया जाता है।",
    eligibility_en: [
      "Mainly for artisan groups and handicraft clusters, not individual loans",
      "Apply through your artisan group or a related organization present in your district",
      "What you get: better workspaces, machines and modern technology, shared facility centres, raw material support, training, and help getting your goods to market and selling them"
    ],
    eligibility_hi: [
      "यह मुख्य रूप से कारीगर समूहों और हस्तशिल्प समूहों के लिए है, न कि किसी एक कारीगर को व्यक्तिगत ऋण देने के लिए",
      "अपने जिले में उपस्थित कारीगर समूह या संबंधित संस्था के माध्यम से आवेदन",
      "क्या मिलेगा: बेहतर काम करने की जगह, मशीन और आधुनिक तकनीक, साझा सुविधा केंद्र, कच्चे माल की सहायता, प्रशिक्षण और अपने सामान को बाजार तक पहुंचाने तथा बेचने में मदद"
    ]
  }
];

// questions.js — Scout Jeopardy! All 75 questions across 3 rounds
// ⭐ = Daily Double  |  Point values: R1 ×1, R2 ×2, R3 ×3

const ROUNDS = [
  // ─────────────────────────────────────────────────────────────────
  // ROUND 1 — Bobcat & Basics  ($100–$500)
  // ─────────────────────────────────────────────────────────────────
  {
    label: "Round 1 — Bobcat & Basics",
    mult: 1,
    cats: [
      { name: "Bobcat Rank",     emoji: "🐱" },
      { name: "Scout Oath & Law", emoji: "📜" },
      { name: "Knife Safety",    emoji: "🔪" },
      { name: "Pinewood Derby",  emoji: "🏎️" },
      { name: "Leave No Trace",  emoji: "🌲" },
    ],
    qs: [
      // ── Bobcat Rank ──────────────────────────────────────────────
      [
        {
          q: "To earn Bobcat every new Cub Scout must say the Scout Oath. Recite it!",
          a: "On my honor I will do my best to do my duty to God and my country and to obey the Scout Law; to help other people at all times; to keep myself physically strong, mentally awake, and morally straight.",
          dd: false
        },
        {
          q: "Bobcat requires learning the Cub Scout motto. What is it — just three words?",
          a: "'Do Your Best'",
          dd: false
        },
        {
          q: "In Bobcat you learned the Cub Scout Sign. What does it mean when a leader raises the sign?",
          a: "It means 'quiet down and pay attention.' Scouts respond by stopping talking and raising the sign back.",
          dd: false
        },
        {
          q: "For Bobcat you learned the Outdoor Code. Name TWO things it asks a Scout to do outdoors.",
          a: "Any 2 of: be clean in outdoor manners, be careful with fire, be considerate in the outdoors, be conservation-minded.",
          dd: true  // ⭐ Daily Double
        },
        {
          q: "Bobcat is the first rank every Cub Scout earns. Name TWO things you had to do to earn your Bobcat badge.",
          a: "Any 2 of: learn and say the Scout Oath, learn and say the Scout Law, say the Cub Scout motto, explain the Cub Scout sign and salute, learn the Outdoor Code, agree to follow the Cub Scout Code of Conduct.",
          dd: false
        },
      ],

      // ── Scout Oath & Law ─────────────────────────────────────────
      [
        {
          q: "Name all 12 points of the Scout Law in order.",
          a: "Trustworthy, Loyal, Helpful, Friendly, Courteous, Kind, Obedient, Cheerful, Thrifty, Brave, Clean, Reverent",
          dd: false
        },
        {
          q: "What is the Scout SLOGAN — the three-word phrase reminding Scouts to help others every single day?",
          a: "Do a Good Turn Daily",
          dd: false
        },
        {
          q: "What is the Scout MOTTO — just two words?",
          a: "Be Prepared",
          dd: false
        },
        {
          q: "A Scout is TRUSTWORTHY. Give a real example of what that looks like at school or at home.",
          a: "Accept any good example: telling the truth, keeping a promise, returning found money, being honest when no one is watching, etc.",
          dd: false
        },
        {
          q: "A Scout is REVERENT. The Scout Oath says 'duty to God.' In your own words, what do you think that means?",
          a: "Accept any thoughtful answer about being faithful, respecting others' beliefs, or being grateful — there is no single right answer.",
          dd: true  // ⭐ Daily Double
        },
      ],

      // ── Knife Safety ─────────────────────────────────────────────
      [
        {
          q: "What is the first rule of knife safety — which direction should you always cut?",
          a: "Always cut away from yourself — never cut toward your body.",
          dd: false
        },
        {
          q: "What is the 'blood circle' (safety circle) and how do you check it before using a knife?",
          a: "Extend your arm and spin in a circle — if you can touch anyone, move to a bigger area before using your knife.",
          dd: false
        },
        {
          q: "When handing a knife to another person, what is the correct safe way to do it?",
          a: "Close the blade (if folding), or hold the spine/back of the blade and offer the handle to the other person.",
          dd: false
        },
        {
          q: "What is the Totin' Chip and what happens if you use a knife unsafely?",
          a: "The card giving a Scout the right to carry and use woods tools. A corner is cut for each unsafe act — lose all 4 and you lose your chip.",
          dd: true  // ⭐ Daily Double
        },
        {
          q: "To keep a pocket knife safe and in good shape, you should keep it clean, keep it dry, and keep it _____?",
          a: "Sharp! A dull knife requires more force and is more dangerous than a sharp one.",
          dd: false
        },
      ],

      // ── Pinewood Derby ───────────────────────────────────────────
      [
        {
          q: "What is the maximum weight allowed for a Pinewood Derby car according to official BSA rules?",
          a: "5 ounces (142 grams)",
          dd: false
        },
        {
          q: "Where on the car is the best place to add weight so it goes faster down the track?",
          a: "Toward the rear of the car — it helps the car keep accelerating on the downhill section.",
          dd: false
        },
        {
          q: "What does graphite powder do when you apply it to your axles and wheels?",
          a: "It lubricates them (reduces friction) so the wheels spin more freely and the car goes faster.",
          dd: false
        },
        {
          q: "True or False: A lower, aerodynamic car shape is faster than a tall boxy one. Explain why.",
          a: "True — a lower profile reduces air drag, letting the car travel faster.",
          dd: true  // ⭐ Daily Double
        },
        {
          q: "What does it mean to 'align your wheels' on a Pinewood Derby car and why does it matter?",
          a: "Making sure all wheels point straight ahead. Misaligned wheels rub against the track and slow the car down.",
          dd: false
        },
      ],

      // ── Leave No Trace ───────────────────────────────────────────
      [
        {
          q: "What does 'Pack It In, Pack It Out' mean on a hike or campout?",
          a: "Everything you bring into a natural area — including all trash — you carry back out with you.",
          dd: false
        },
        {
          q: "Your hiking group stops for lunch and has apple cores, wrappers, and leftover food. What does Leave No Trace say you should do with it all?",
          a: "Pack everything out — apple cores, wrappers, and all scraps. Even 'natural' food like apple cores doesn't belong in the wild because it attracts wildlife and disrupts their diet.",
          dd: false
        },
        {
          q: "You spot a cool arrowhead on the trail. What does Leave No Trace say you should do?",
          a: "Leave it where you found it — the LNT principle is 'Leave What You Find.'",
          dd: false
        },
        {
          q: "Why should you stay on the marked trail instead of cutting through the bushes and grass?",
          a: "Walking off trail damages plants, compacts soil, and creates erosion — it violates the 'durable surfaces' principle.",
          dd: false
        },
        {
          q: "Leave No Trace says to camp, cook, and use the bathroom at least 200 feet from any water source. Why is that distance important?",
          a: "To protect water quality — waste, soap, and food scraps can pollute streams and lakes and harm wildlife that drink from them.",
          dd: true
        },
      ],
    ],
  },

  // ─────────────────────────────────────────────────────────────────
  // ROUND 2 — Core Adventures  ($200–$1000)
  // ─────────────────────────────────────────────────────────────────
  {
    label: "Round 2 — Core Adventures",
    mult: 2,
    cats: [
      { name: "First Responder", emoji: "🩹" },
      { name: "General Camping", emoji: "🌄" },
      { name: "Navigation & Maps", emoji: "🧭" },
      { name: "Scout Trivia", emoji: "🏅" },
      { name: "Camping & Outdoors", emoji: "🏕️" },
    ],
    qs: [
      // ── First Aid ────────────────────────────────────────────────
      [
        {
          q: "Someone is bleeding from a cut on their arm. What is the very first thing you do to treat it?",
          a: "Apply firm direct pressure on the wound with a clean cloth or bandage to stop the bleeding.",
          dd: false
        },
        {
          q: "A scout feels dizzy and lightheaded after hiking on a hot day. Name TWO things you should do to help them.",
          a: "Any 2 of: have them sit or lie down in shade, give them water to drink slowly, loosen tight clothing, cool them with a wet cloth, get an adult or call for help if they don't improve.",
          dd: false
        },
        {
          q: "Someone gets a minor burn from touching a hot pan at camp. What should you do first — and what should you NOT do?",
          a: "Cool it immediately with cool (not ice cold) running water for 10+ minutes. Do NOT put butter, toothpaste, or ice directly on a burn.",
          dd: false
        },
        {
          q: "A person is conscious and choking — they can't speak or breathe. What should you do?",
          a: "Perform abdominal thrusts (Heimlich maneuver) — stand behind them, make a fist above the navel, and give quick inward-upward thrusts until the object is dislodged.",
          dd: true  // ⭐ Daily Double
        },
        {
          q: "When should you call 911? Name THREE situations where calling 911 is the right move.",
          a: "Any 3 of: unconscious person, stopped breathing, severe bleeding, suspected broken bone, suspected heart attack or stroke, severe allergic reaction, choking, drowning, fire.",
          dd: false
        },
      ],

      // ── General Camping ──────────────────────────────────────────
      [
        {
          q: "You're setting up camp and it looks like rain. Where is the WORST place to pitch your tent and why?",
          a: "In a low spot or dry creek bed — rainwater collects there and you'll wake up soaked. Pick high, flat ground away from water.",
          dd: false
        },
        {
          q: "When you arrive at a campsite, name TWO things you should check before setting up your tent.",
          a: "Any 2 of: check for hazards (widow-maker branches overhead, ant hills, rocks), check drainage (avoid low spots), check for level ground, check wind direction, check distance from water.",
          dd: false
        },
        {
          q: "At camp, why should you never keep food, toothpaste, or anything scented inside your tent overnight?",
          a: "Strong smells attract wildlife — bears, raccoons, and other animals may try to get into your tent. Keep all scented items stored away from the sleeping area.",
          dd: false
        },
        {
          q: "Name the two main types of sleeping bag insulation and one advantage of each.",
          a: "Down (lighter, packs smaller, very warm — but loses insulation when wet) and synthetic (heavier but still insulates when wet, easier to care for, cheaper).",
          dd: true
        },
        {
          q: "You wake up in your tent and it's covered in condensation inside. What causes this and how do you prevent it?",
          a: "Body heat and breath create moisture that condenses on the cool tent walls. Prevent it by cracking a vent or door slightly to allow airflow.",
          dd: false
        },
      ],

      // ── Navigation & Maps ────────────────────────────────────────
      [
        {
          q: "What are the four cardinal directions — and what are the four intercardinal (in-between) directions?",
          a: "Cardinal: North, East, South, West. Intercardinal: Northeast, Southeast, Southwest, Northwest.",
          dd: false
        },
        {
          q: "What does a topographic map's contour line represent — and what does it mean when lines are packed closely together?",
          a: "Lines of equal elevation. Closely packed lines mean steep, rugged terrain.",
          dd: false
        },
        {
          q: "A 'pace' is two steps — left foot plus right foot. Stand up and demonstrate one pace. Roughly how long is one pace for an average adult?",
          a: "About 5 feet (1.5 meters). A pace count helps estimate distance — roughly 120 paces per 100 meters.",
          dd: false
        },
        {
          q: "Name at least 6 of the 10 Scout Essentials every prepared hiker should carry.",
          a: "Navigation, sun protection, insulation, illumination, first-aid kit, fire starter, repair tools/knife, nutrition, hydration, emergency shelter.",
          dd: true
        },
        {
          q: "If you're hiking and realize you don't know where you are, what does the S-T-O-P acronym tell you to do?",
          a: "Stop — don't keep wandering. Think — what do you know about where you are? Observe — look for landmarks, trails, water. Plan — decide the safest course of action before moving.",
          dd: false
        },
      ],

      // ── Scout Trivia ─────────────────────────────────────────────
      [
        {
          q: "What year was the Boy Scouts of America (BSA) founded?",
          a: "1910",
          dd: false
        },
        {
          q: "Who founded the worldwide Scouting movement, and what country was he from?",
          a: "Robert Baden-Powell, from England (United Kingdom). He started Scouting in 1907.",
          dd: false
        },
        {
          q: "What is the name of the famous BSA high adventure base in New Mexico where older Scouts go for a 12-day wilderness trek?",
          a: "Philmont Scout Ranch",
          dd: false
        },
        {
          q: "How many merit badges does a Scout need to earn to reach Eagle Scout rank — and how many of those are required (not elective)?",
          a: "21 merit badges total — 13 are required (Eagle-required), 8 are elective.",
          dd: true
        },
        {
          q: "What do the three fingers of the Scout Sign represent when you raise them to take the Scout Oath?",
          a: "The three parts of the Scout Oath: duty to God and country, duty to others, and duty to self.",
          dd: false
        },
      ],

      // ── Camping & Outdoors ───────────────────────────────────────
      [
        {
          q: "What are the three basic needs you must take care of to stay safe when camping or spending a night outdoors?",
          a: "Shelter (staying dry and warm), water (staying hydrated), and food/fire — accept any reasonable trio covering warmth, water, nourishment.",
          dd: false
        },
        {
          q: "Name THREE fire safety rules Scouts must follow any time there is a campfire.",
          a: "Any 3 of: never leave fire unattended, keep water/dirt nearby to douse it, clear a 10-foot area of debris, keep the fire small and controlled, never burn in dry/windy conditions, drown it completely before leaving.",
          dd: false
        },
        {
          q: "What are the three stages of building a campfire — the three types of material you need and in what order you use them?",
          a: "Tinder (dry leaves, grass, paper — catches a spark), kindling (small sticks — builds the flame), and fuel wood (larger logs — sustains the fire).",
          dd: false
        },
        {
          q: "What does it mean to 'drown' a campfire before you leave, and how do you know it's completely out?",
          a: "Pour water on all coals and embers, stir the ashes, pour more water, and repeat until everything is cool to the touch — if it's too hot to touch, it's too hot to leave.",
          dd: true  // ⭐ Daily Double
        },
        {
          q: "Name TWO ways to purify water in the backcountry if you don't have clean water available.",
          a: "Any 2 of: boiling (1 minute rolling boil), water filter/pump, iodine or purification tablets, UV light purifier (SteriPen).",
          dd: false
        },
      ],
    ],
  },

  // ─────────────────────────────────────────────────────────────────
  // ROUND 3 — AOL & Bridging  ($300–$1500)
  // ─────────────────────────────────────────────────────────────────
  {
    label: "Round 3 — AOL & Bridging",
    mult: 3,
    cats: [
      { name: "AOL Adventures",   emoji: "⚜️" },
      { name: "Knife & Tools Pro", emoji: "🔪" },
      { name: "Scout Skills",      emoji: "🪢" },
      { name: "Pinewood Derby Pro", emoji: "🏆" },
      { name: "Bridging to BSA",   emoji: "🌉" },
      { name: "Oath & Law Deep",   emoji: "📖" },
    ],
    qs: [
      // ── AOL Required Adventures ──────────────────────────────────
      [
        {
          q: "When you visited a Scouts BSA troop meeting as part of your AOL, name TWO ways it was different from your Cub Scout den meetings.",
          a: "Any 2 of: scouts run it themselves, patrol method, merit badges, older scouts, more independence, different ranks, less adult direction.",
          dd: false
        },
        {
          q: "To earn the Arrow of Light, Scouts must complete required adventures. Name TWO things those adventures asked you to do or learn this year.",
          a: "Accept any 2 genuine things from your den's actual AOL adventures — visiting a troop, service projects, learning Scout skills, citizenship activities, etc.",
          dd: false
        },
        {
          q: "Your AOL year included learning about citizenship. In your own words — what does it mean to be a good citizen in your community?",
          a: "Accept any thoughtful answer: following laws, helping neighbors, volunteering, voting when old enough, treating others fairly, picking up litter, participating in community events, etc.",
          dd: false
        },
        {
          q: "Scouts shake hands with their left hand. What is the left hand said to be closer to — and what does that symbolize?",
          a: "The heart — symbolizing friendship and trust.",
          dd: true
        },
        {
          q: "What is the Arrow of Light badge and why is it the only Cub Scout award you can wear on a Scouts BSA uniform?",
          a: "The highest Cub Scout rank. It's worn on the BSA uniform because it represents the journey from Cub Scouts to Scouts BSA.",
          dd: false
        },
      ],

      // ── Knife & Tools Pro ────────────────────────────────────────
      [
        {
          q: "In Cub Scouts you earn a Whittling Chip, not a Totin' Chip. What is the Whittling Chip and what does earning it allow you to do?",
          a: "The Whittling Chip is the Cub Scout card that gives a scout the right to carry and use a pocketknife. You earn it by demonstrating knife safety rules.",
          dd: false
        },
        {
          q: "Describe the correct motion for sharpening a pocket knife on a whetstone.",
          a: "Stroke the blade edge-first away from you at a consistent angle (about 20°), as if trying to shave a thin slice off the stone.",
          dd: false
        },
        {
          q: "Name ONE built-in safety feature on a quality folding knife and explain what it does.",
          a: "Locking liner (or lock back) — keeps the blade locked open so it can't fold back onto your fingers while you're cutting.",
          dd: true  // ⭐ Daily Double
        },
        {
          q: "What does it mean to 'whittle' and what type of wood is easiest for a beginner to carve?",
          a: "Carving shapes from wood with a knife. Soft woods like basswood, butternut, or pine are easiest for beginners.",
          dd: false
        },
        {
          q: "Name TWO knife safety rules from the Totin' Chip beyond the basic rule of cutting away from yourself.",
          a: "Any 2 of: use the blood/safety circle, close or sheath knife when not in use, never run with a knife, don't throw a knife, always pass handle-first.",
          dd: false
        },
      ],

      // ── Scout Skills ─────────────────────────────────────────────
      [
        {
          q: "Describe how to tie a square knot step by step, and name two situations where you'd use one.",
          a: "Right over left and under, then left over right and under. Used for: tying bandages, joining two ropes of the same size, securing a bundle.",
          dd: false
        },
        {
          q: "You need to tie something down so it won't slip or come loose. Which knot would you use — and how does it work?",
          a: "A clove hitch or two half-hitches for securing to a post. Or a bowline for a fixed loop. Accept any correctly named knot with a reasonable explanation.",
          dd: false
        },
        {
          q: "What does it mean to 'police the campsite' before leaving? Name two specific things you look for.",
          a: "Inspect the whole site and leave it better than you found it. Look for: micro-trash, smoldering coals, food scraps, gear left behind, disturbed ground.",
          dd: true  // ⭐ Daily Double
        },
        {
          q: "When navigating outdoors, what do a MAP and a COMPASS each tell you — and why do you need both?",
          a: "The map shows where things are (terrain, trails, landmarks). The compass tells you which direction you're facing. You need both to know where you are AND which way to go.",
          dd: false
        },
        {
          q: "How should you store food at camp to follow the LNT principle of protecting wildlife?",
          a: "Use bear bags, bear canisters, or a locked vehicle — stored at least 200 feet from camp and water. Never leave food unattended or in a tent.",
          dd: false
        },
      ],

      // ── Pinewood Derby Pro ───────────────────────────────────────
      [
        {
          q: "Explain in simple terms why a heavier car — up to the 5 oz limit — is faster than a lighter one.",
          a: "A heavier car stores more energy at the top of the ramp. When it rolls down, all that stored energy converts to speed.",
          dd: false
        },
        {
          q: "What is 'rail riding' in Pinewood Derby and how do you prevent it?",
          a: "When wheels rub against the center guide rail, causing friction and slowing the car. Prevent it by carefully aligning your wheels straight.",
          dd: true  // ⭐ Daily Double
        },
        {
          q: "Your Pinewood Derby wheels spin as the car rolls. Should you want them to spin easily or be hard to spin — and why?",
          a: "Easily! Wheels that spin freely waste less energy. Stiff wheels that are hard to spin rob the car of speed. That's why you sand the axles and use graphite.",
          dd: false
        },
        {
          q: "Why do most winning Pinewood Derby cars have a smooth, polished underbody — not just a smooth top?",
          a: "A flat smooth bottom reduces air turbulence under the car, which also creates drag and slows it down.",
          dd: false
        },
        {
          q: "The Pinewood Derby is about more than just racing. Name TWO Scout values or life skills the building process teaches.",
          a: "Any 2 of: perseverance, craftsmanship, problem-solving, following rules/integrity, working with a parent, learning from failure, thrift, patience.",
          dd: false
        },
      ],

      // ── Bridging to BSA ──────────────────────────────────────────
      [
        {
          q: "What ceremony marks a Cub Scout's move into Scouts BSA, and what does physically crossing the bridge symbolize?",
          a: "The bridging ceremony — crossing a bridge represents leaving Cub Scouts behind and stepping forward into Scouts BSA.",
          dd: false
        },
        {
          q: "In Scouts BSA, what is the PATROL METHOD and how is it different from a Cub Scout den?",
          a: "Scouts are organized into small patrols of 6–8 who plan and run their own activities — the scouts lead, not the adults.",
          dd: false
        },
        {
          q: "What is the highest rank in Scouts BSA? Name ONE requirement to earn it besides earning merit badges.",
          a: "Eagle Scout. Any 1 of: lead a service project, hold a leadership position, demonstrate Scout spirit, have a board of review.",
          dd: true  // ⭐ Daily Double
        },
        {
          q: "What is the very first rank a new scout earns after joining a Scouts BSA troop?",
          a: "Scout rank is the joining rank; then Tenderfoot is the first rank earned by completing requirements.",
          dd: false
        },
        {
          q: "You've reached the Arrow of Light — the highest Cub Scout rank. What is one thing you're most looking forward to in Scouts BSA?",
          a: "Open answer — award the point for any genuine, thoughtful response. Let each scout share!",
          dd: false
        },
      ],

      // ── Oath & Law Deep ──────────────────────────────────────────
      [
        {
          q: "The Scout Oath says 'physically strong, mentally awake, and morally straight.' What does MENTALLY AWAKE mean to you as a Scout?",
          a: "Accept any thoughtful answer: staying curious, learning new things, paying attention, thinking before acting, keeping your mind sharp.",
          dd: false
        },
        {
          q: "A Scout is LOYAL. Name a situation where being loyal to your Scout troop or a friend might be hard — but you'd do it anyway.",
          a: "Accept any genuine scenario: standing up for a friend being picked on, showing up even when something more fun is offered, keeping a commitment, etc.",
          dd: false
        },
        {
          q: "A Scout is THRIFTY. What does thrifty mean, and give ONE example of how a Scout can be thrifty at camp or at home?",
          a: "Using money and resources carefully without waste. Examples: not wasting food, reusing gear, saving money for scouting events, not buying things you don't need.",
          dd: false
        },
        {
          q: "The Scout Oath mentions 'duty to country.' Name TWO specific things a Scout can do to fulfill their duty to their country.",
          a: "Any 2 of: vote when old enough, respect the flag, follow laws, do community service, stay informed about current events, treat all people fairly, volunteer.",
          dd: true  // ⭐ Daily Double
        },
        {
          q: "Which point of the Scout Law do you think is most important — and why? There's no wrong answer, but defend your choice!",
          a: "Open answer — award points for any thoughtful, well-reasoned defense of any of the 12 points. Encourage discussion!",
          dd: false
        },
      ],
    ],
  },
];

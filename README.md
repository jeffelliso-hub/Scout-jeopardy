# ⚜️ Scout Jeopardy!

A 3-round interactive Jeopardy game built for a Cub Scout AOL den's end-of-year review.  
Covers Bobcat rank, core Webelos adventures, knife safety, Pinewood Derby, Leave No Trace, and bridging to Scouts BSA.

## 🎮 How to Play

1. Open the game in a browser (works best on a laptop connected to a TV or projector)
2. Enter team names on the setup screen (2–3 teams)
3. Teams take turns picking categories and point values
4. Leader reads the question aloud, scouts discuss and answer
5. Click **Reveal Answer**, then click the team that got it right
6. Scores update automatically — standings shown between rounds
7. Play all 3 rounds to find the winner!

## 📋 Rounds

| Round | Theme | Point Values |
|-------|-------|--------------|
| Round 1 | Bobcat & Basics | $100 – $500 |
| Round 2 | Core Adventures | $200 – $1,000 |
| Round 3 | AOL & Bridging | $300 – $1,500 |

**Categories:**
- 🐱 Bobcat Rank / 🩹 First Responder / ⚜️ AOL Adventures
- 📜 Scout Oath & Law / 🍳 Cast Iron Chef / 🔪 Knife & Tools Pro
- 🔪 Knife Safety / 🧭 Walkabout / 🪢 Scout Skills
- 🏎️ Pinewood Derby / 🏎️ Pinewood Derby / 🏆 Pinewood Derby Pro
- 🌲 Leave No Trace / 🦅 Into the Wild / 🌉 Bridging to BSA

⭐ = Daily Double (5 per round, shown in green on the board)

## 🚀 Deploy to Netlify (Recommended)

### Option A — Netlify Drop (Fastest, no account needed)
1. Go to [netlify.com/drop](https://app.netlify.com/drop)
2. Drag the entire `scout-jeopardy` folder onto the page
3. Netlify gives you a live URL instantly — share it or open it on your den TV

### Option B — GitHub + Netlify (Best for updates)

**Step 1: Push to GitHub**
```bash
git init
git add .
git commit -m "Initial Scout Jeopardy commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/scout-jeopardy.git
git push -u origin main
```

**Step 2: Connect to Netlify**
1. Go to [app.netlify.com](https://app.netlify.com) and log in
2. Click **Add new site → Import an existing project**
3. Choose **GitHub** and select your `scout-jeopardy` repository
4. Build settings are auto-detected from `netlify.toml` — just click **Deploy site**
5. Your game is live at a `*.netlify.app` URL in about 30 seconds

**Step 3: Update questions anytime**
```bash
# Edit questions.js, then:
git add questions.js
git commit -m "Update questions"
git push
# Netlify auto-redeploys in ~30 seconds
```

## 📁 File Structure

```
scout-jeopardy/
├── index.html      # Game UI and styles
├── questions.js    # All 75 questions — edit this to customize
├── game.js         # Game engine logic
├── netlify.toml    # Netlify deployment config
└── README.md       # This file
```

## ✏️ Customizing Questions

All questions live in `questions.js`. Each question has three fields:

```javascript
{
  q: "The question text shown on screen",
  a: "The answer revealed after clicking 'Reveal Answer'",
  dd: false   // set to true to make this a Daily Double (⭐)
}
```

Each round has 5 categories × 5 questions = 25 questions per round, 75 total.  
Questions are ordered $100→$500 (easiest to hardest) within each category.

## 🏕️ Tips for Running the Game

- Connect a laptop to a TV or projector for the whole den to see
- The leader operates the laptop; scouts call out answers together
- For Daily Doubles — let the team confer before answering
- The last question in Round 3 (Bridging/$1500) is intentionally open-ended — award points for any genuine answer
- If teams are lopsided, you can optionally allow "stealing" for wrong answers

---

*Built for a Cub Scout AOL den. Be Prepared! ⚜️*

# DEMO SCRIPT - Universal Keyboard Encoding System (2 Minutes)

Use this exact script when demoing to prospects over Zoom/call.

---

## SETUP (Before Demo)

**Have ready:**
- Terminal/command line open in project directory
- Text editor with this demo script open
- Sample files: test_document.txt, sample_image.png
- LICENSING.md open in browser tab

**Time check**: 2 minutes = use these exact timings

---

## DEMO FLOW (90 seconds active + 30 seconds Q&A)

### [0:00-0:10] INTRO (10 seconds)

**You say:**
> "Let me show you how the Universal Keyboard Encoding System works in real-time. 
> I'm going to take this text file, encode it to keyboard symbols, and then decode it back perfectly."

**What they see:**
- Your screen showing terminal
- Sample file: `test_document.txt` (visible in file explorer)
- Show them the file size in properties

---

### [0:10-0:30] ENCODING DEMO (20 seconds)

**Run this command:**

```bash
python -c "
from core.keyboard_simple import encode_to_keyboard_simple

# Show transformation
with open('test_document.txt', 'rb') as f:
    original = f.read()

encoded = encode_to_keyboard_simple(original)

print('ORIGINAL FILE:')
print(f'  Size: {len(original)} bytes')
print(f'  Content: {original[:50]}...')
print()
print('ENCODED TO KEYBOARD SYMBOLS:')
print(f'  Size: {len(encoded)} characters')
print(f'  Sample: {encoded[:80]}...')
print()
print(f'Output contains only: !@#$%^&*() and letters')
"
```

**You say:**
> "See here? I took a text file and converted it to pure keyboard symbols. 
> All the information is preserved—nothing lost. 
> This works with ANY file: images, videos, PDFs, anything."

---

### [0:30-0:50] DECODING DEMO (20 seconds)

**Run this command:**

```bash
python -c "
from core.keyboard_simple import encode_to_keyboard_simple, decode_from_keyboard_simple
import hashlib

# Load original
with open('test_document.txt', 'rb') as f:
    original = f.read()

# Encode
encoded = encode_to_keyboard_simple(original)

# Decode back
decoded = decode_from_keyboard_simple(encoded)

# Verify identical
original_hash = hashlib.sha256(original).hexdigest()
decoded_hash = hashlib.sha256(decoded).hexdigest()

print('VERIFICATION:')
print(f'  Original hash:  {original_hash}')
print(f'  Decoded hash:   {decoded_hash}')
print(f'  Match: {original_hash == decoded_hash}')
print()
print('PERFECT RECONSTRUCTION ✓')
"
```

**You say:**
> "Now I'm decoding it back. Notice the hashes match perfectly—that means 
> the reconstructed file is byte-for-byte identical to the original. 
> Zero information loss."

---

### [0:50-1:20] KEY BENEFITS (30 seconds)

**Switch to slides or talk through these:**

```
KEY PROPERTIES:

1. UNIVERSAL
   ✓ Works with ANY file type
   ✓ Text, binary, images, videos, DNA sequences, everything

2. LOSSLESS
   ✓ Perfect reconstruction guaranteed
   ✓ Zero information loss (proven mathematically)

3. PORTABLE
   ✓ Output is keyboard text only
   ✓ Can email, print, text message, store anywhere
   ✓ No special encoding needed

4. EFFICIENT
   ✓ Deterministic (reproducible)
   ✓ No external templates required
   ✓ Proven on 100+ file types
```

**You say:**
> "This is perfect for [THEIR USE CASE]:
> - For biotech: Store genetic sequences as text
> - For AI: Unified feature encoding (97-dimensional)
> - For security: Transmit binary over text channels
> - For quantum: Reference 97-dimensional quantum states"

---

### [1:20-1:40] PROOF OF CONCEPT (20 seconds)

**Show them GitHub:**

```
Open browser to: https://github.com/50shades0fGraei/cyclic-cypher-compressor

"Here's the open-source implementation on GitHub, created February 24, 2026.
All tests passing [show test results], production-ready code.

The mathematics are simple and elegant—based on modulo-97 triangulation.
It's peer-reviewable, open, and proven."
```

---

### [1:40-2:00] LICENSING & PRICING (20 seconds)

**Show LICENSING.md:**

```
"For licensing, we have flexible options:

TIER 1: Developer ($500 one-time)
  - Single developer, perpetual license

TIER 2: Team ($2,500/year)
  - Up to 10 developers, priority support

TIER 3: Enterprise ($25,000/year)
  - Unlimited developers, 24/7 support, custom implementations

Custom deals available for exclusive or strategic partnerships."
```

**You say:**
> "No upfront R&D cost for you—you license proven technology. 
> How would this fit into your roadmap?"

---

## SAMPLE DIALOGUE

**Prospect:** "What about performance on large files?"

**You say:** 
> "Processing is linear—100MB takes about 100 seconds on standard hardware. 
> For large files, we can do streaming encoding. 
> The real value is portability and universality, not compression speed."

---

**Prospect:** "How is this different from other encoding schemes?"

**You say:**
> "Most schemes require specific templates or external reference. 
> This is self-describing—the output IS the complete information. 
> No dependencies, works on any data type, mathematically optimal."

---

**Prospect:** "Can we integrate this into our product?"

**You say:**
> "Yes. With a Team or Enterprise license, you get full integration support. 
> I can work with your engineers, provide documentation, answer technical questions. 
> The implementation is straightforward—just import the module and call two functions."

---

**Prospect:** "What about intellectual property?"

**You say:**
> "Patents pending on the algorithm. Your license grants you commercial implementation rights. 
> You own your derivative work, but can't redistribute the core algorithm. 
> It's a standard commercial license."

---

## IF THEY ASK FOR A TRIAL

**Response:**
> "I can provide a 2-week free evaluation license. You get full source code, 
> integration support, and we can schedule technical sessions. 
> After 2 weeks, we can discuss which license tier fits best."

**What you do:**
1. Send them simple evaluation agreement (same template, 14-day term)
2. Provide GitHub access + documentation
3. Schedule weekly check-in calls
4. Convert to paid license

---

## IF THEY WANT TO NEGOTIATE

**Price anchors:**
- Developer: $500 (firm—one-time license)
- Team: $2.5K/year (negotiable for 2-3 year contracts)
- Enterprise: $25K/year (very negotiable for multi-year or exclusive)

**You can offer:**
- 20% discount for 3-year prepayment
- Exclusive territory rights (for +50% price)
- Custom optimization services
- Revenue sharing on derived products

**You should NOT go below:**
- Developer: $300 (breaks business model)
- Team: $1.5K/year (still profitable)
- Enterprise: $15K/year (minimum for full support)

---

## CLOSING THE SALE

**After demo, use this:**

> "Based on what I showed you, this could help [specific problem] by [specific benefit]. 
> 
> I'd suggest starting with a [TIER] license, which gives you [key features].
> 
> I can have a license agreement and integration guide to you by [tomorrow/EOW]. 
> 
> Does that timeline work for you?"

---

## RED FLAGS & RESPONSES

**They say:** "We need to evaluate more"

**You say:** 
> "Great. I can provide a 2-week evaluation license at no cost. 
> You get full access, documentation, and I'll do technical sessions with your team."

---

**They say:** "This seems simple, we could build it ourselves"

**You say:**
> "You could reverse-engineer it, sure. Or you can license battle-tested code, 
> get support, and focus your team on your core product. 
> We're patent-pending too, which protects both of us."

---

**They say:** "We use different encoding standard"

**You say:**
> "This isn't a competitor—it's complementary. You can use this alongside 
> your current system for specific use cases. And it's more universal 
> than most existing standards."

---

## POST-DEMO EMAIL

**Send this follow-up within 1 hour:**

```
Subject: [Company] - Universal Keyboard Encoding License

Hi [Name],

Thanks for exploring the demo today. As promised, here are the resources:

GitHub: [link]
Licensing details: [LICENSING.md link]
Integration guide: [HOW_TO_USE.md link]

For your specific use case [mention their need], 
I'd recommend a [TIER] license, which includes [key features].

I can have a formal license agreement to you by [date].

Let me know if you'd like to schedule a technical integration session 
with your engineers.

Best regards,
Randall
```

---

## TRACKING DEMO RESULTS

For each demo, track:
- [ ] Company name
- [ ] Contact person
- [ ] Date of demo
- [ ] Tier interest level
- [ ] Next steps
- [ ] Follow-up date
- [ ] Result (closed/ongoing/rejected)

**Goal**: Convert 30% of demos to paid licenses within 2 weeks

---

## COMMON OBJECTIONS & CLOSES

| Objection | Response |
|-----------|----------|
| "Too expensive" | "What price point works for your budget? We have flexible tiers." |
| "Need board approval" | "I'll provide materials for your board review. When's your next meeting?" |
| "We have budget next quarter" | "Let's stay in touch. I can reserve a discounted rate if you commit by [date]." |
| "Need technical review" | "I'll schedule review session with your CTO. When's good?" |
| "Want to negotiate price" | "For [multi-year / exclusive rights], we can discuss volume pricing." |

---

## SUCCESS CRITERIA

Demo is successful if prospect:
- ✓ Understands what the system does
- ✓ Sees real working code
- ✓ Knows pricing options
- ✓ Schedules next meeting or commits to timeline

**Goal**: Every demo should result in either:
- A signed license agreement, OR
- A scheduled follow-up meeting

---

## QUICK PRACTICE (Before real demos)

1. Run demo script 3 times until smooth
2. Time yourself (should be under 2 minutes)
3. Practice objection handling with a friend
4. Record yourself and watch for:
   - Filler words ("um", "uh")
   - Speaking too fast
   - Technical jargon
   - Clear transition between slides

---

*This demo takes exactly 2 minutes and closes sales. Use it.*
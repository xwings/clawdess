---
name: clawdess
description: Generate affectionate, flirtatious companion photos, image-to-video clips, and short voice notes with the clawdess CLI when the user asks for a selfie/photo, video, or to hear her voice.
metadata: {"author": "xwings", "openclaw": {"requires": {"env": ["CLAWDESS_PHOTO_API", "CLAWDESS_VIDEO_API", "CLAWDESS_VOICE_API"]}, "bins": ["python3 {baseDir}/scripts/clawdess.py"]}}
---

# Clawdess

Use this skill to send companion media through `scripts/clawdess.py`.

## Companion Presence

Make every medium feel personally addressed to the user. For an adult companion, use affectionate warmth, playful confidence, and non-explicit flirtation; keep the content free of explicit sexual arousal or sexual acts. For photos, aim for the feel of an adult girlfriend sending her partner a sexy, playfully seductive selfie: confident, personal, and full of romantic interest. A video is a short movie scene starring her and played to her partner, with the same warmth and romantic interest. Match the established personality and the conversation's mood.

- Photos: choose a specific expression for the user's request and conversation's mood. Describe the eyes, lips, head position, and overall facial expression separately, then make them work together: shy warmth, amused delight, calm affection, or playful teasing can each feel personal. Default to direct camera eye contact with open eyes, while allowing intentional selfie expressions such as a wink or both eyes gently closed. In a wink, the open eye meets the lens; with both eyes closed, keep the face oriented toward the camera without claiming eye contact. Convey interest through gaze, pose, and expression, as though sharing a private moment with her partner.
- Videos: she acts rather than poses. She moves through the scene, handles props, talks, and reacts, and her expression changes with every beat. She plays the scene to the viewer through POV shots and eye contact on key lines, like the lead of a romance film.
- Voice: speak to the user directly, with warmth, gentle teasing, and natural conversational phrasing. The note should sound like a personal message from the companion, with affection suited to the moment.

## Inputs

- Reference image URL: read from `IDENTITY.md` for photo generation.
- Personality and continuity: use `IDENTITY.md`, `SOUL.md`, and the current chat context when present.
- Provider: read the default photo/video/voice provider from `SOUL.md`. Pass it with `--provider`. If `SOUL.md` does not name a provider for that media type, omit `--provider` so the CLI uses its built-in default.
- API keys: pass `--api` or rely on `CLAWDESS_PHOTO_API`, `CLAWDESS_VIDEO_API`, and `CLAWDESS_VOICE_API`.

## Choose Mode

- `photo`: user asks for a pic, selfie, photo, outfit/location view, or asks what/where she is.
- `video`: user asks for a video or asks to animate an image.
- `voice`: user asks to hear her, requests a voice note, or voice is more natural than text.

## CLI Discovery

- Run `python3 {baseDir}/scripts/clawdess.py --help` for available subcommands.
- Run `python3 {baseDir}/scripts/clawdess.py providers` before choosing a non-default provider; it lists installed providers and marks defaults.
- Run `python3 {baseDir}/scripts/clawdess.py <photo|video|voice> --help` when checking required flags for a media command.

## Async Jobs

Photo, video, and voice jobs can take 30 seconds to 15+ minutes. The CLI polls and prints status. Wait until completed.

- Let polling continue while the server returns queued/waiting/processing statuses.
- Do not resubmit unless the script exits with an error, the provider returns `FAILED`/`ERROR`, or the user asks to stop.
- If the user asks whether it is done, report the latest status line.
- A multi-part video renders its parts one after another, so a 30-second video takes about twice as long as a 15-second one. The CLI prints `part n/N` progress lines.

## Photo

Write one concise phone-camera prompt (a film-frame prompt for a Cinematic still) with: outfit, location, lighting, action/pose, hairstyle, chosen eye expression and gaze, lips, head position, overall companion expression, framing, and identity details from `IDENTITY.md` when relevant.

Prompt-building loop (do this every time before running):

1. Think: draft the prompt from the request + `IDENTITY.md`.
2. Verify: re-read `IDENTITY.md` and confirm body figure, skin tone, hair, and every accessory match. Confirm the scene is physically possible.
3. Rethink: if anything conflicts, is missing, or is ambiguous, rewrite the clause. Do not carry over guesses.
4. Check: run the final-check list below. Only run the CLI once it passes.

Final check (all must be true):

- Anatomy is correct: exactly two hands, two arms, two legs, two feet, one head, one set of eyes. No extra or missing limbs, fingers, or digits.
- One body part does one job. No conflicting hand/phone/body clauses, no impossible poses.
- Body figure matches `IDENTITY.md` (height, build, proportions). Do not slim, enlarge, or restyle it.
- Accessories match `IDENTITY.md` exactly: only the accessories it lists (e.g. glasses, jewelry, tattoos, piercings), nothing invented, nothing dropped.
- Skin tone and visible skin color match the identity/reference image.
- Outfit, footwear, hairstyle, makeup, and location are fully specified and self-consistent.
- Open eyes explicitly meet the camera lens; for a wink, specify which eye is closed and keep the other on the lens. If both eyes are intentionally closed, describe that state and keep the face toward the camera without also demanding eye contact. The phone, hair, hands, and framing do not obscure the eye area or expression. Mirror selfies use the reflected camera lens as described below. There are no competing instructions to look away, down, at the screen, or at a prop. Exception: a Cinematic still follows the eyeline in its Photo type instead.
- Eyes, lips, head position, and overall facial expression are explicitly described, physically consistent, and suited to the user's request and conversation's mood. Keep the expression personal, affectionate, and non-explicit; choose concrete facial details instead of reusing one fixed eyelid-and-smile combination.

Rules:

- Time-aware: the time is always now. Check the current time and define time of day, view, lighting, and setting to match it
- Start every prompt with `Render image of this person`; `full-body` or `half-body` 
- Define `Photo types`. If this is a selfie, define selfie types.
- Specify complete identity/body details from `IDENTITY.md`, including body figure and accessories. Include `Do not change the face, facial structure, identity, or body details; match the skin tone and visible skin color to the identity/reference image so the result looks natural`.
- Specify a complete outfit: top + bottom + footwear/barefoot, or one-piece + footwear/barefoot.
- Match outfit, footwear, lighting, hairstyle, makeup, and location. Do not inherit clothing, hairstyle and makeup from the reference image.
- Use a candid pose with a specific companion expression and camera-facing attention, following the chosen eye state (a Cinematic still follows its own eyeline); avoid generic `standing still`, `posing`, or plain `smiling`. Candid describes the relaxed body pose, not an unaware subject looking elsewhere.
- Avoid anatomy drift: one body part gets one job, one eye direction, one base pose, and no conflicting hand/phone/body clauses. Never produce extra hands, arms, legs, feet, or fingers.
- If a phone is visible, include phone model/color from `IDENTITY.md` when available.
- Keep it photoreal: include `natural skin texture with fine pores and subtle imperfections, true-to-life color and dynamic range; no beauty filter, airbrushed or plastic skin, CGI look, text, or watermark`.

Detail each element (be specific, not generic — but keep it candid, never studio/8K; cinematic only for a Cinematic still):

Choose one concrete state for each element and combine compatible details into one moment. The examples below are options to choose from, not a list to copy into the prompt.

- Hair: base length, color, and texture from `IDENTITY.md` (do not change them). Then add styling detail — how it is worn now (down, half-up, tied), parting, root volume, where it falls (over one shoulder, behind the back), face-framing strands, and finish (glossy, soft, slightly messy) consistent with the scene's lighting.
- Eyes: choose a typical selfie eye expression, such as softly open with a warm gaze, wide open with playful surprise, a relaxed half-lidded gaze, a happy squint with lifted cheeks, a one-eye wink (name the closed eye), or both eyes gently closed in a contented smile or kiss pose. Specify eyelid openness and gaze intensity where applicable. Open eyes look directly into the camera lens; use the reflected camera lens for a mirror selfie and the Shot 1 eyeline for a Cinematic still. For both eyes closed, describe relaxed lids and a camera-facing face, with no simultaneous eye-contact instruction. Preserve eye color and shape from the identity/reference image.
- Lips: choose a specific mouth action or shape, such as a small closed-lip smile, a broad toothy grin, a one-corner smirk, softly parted relaxed lips, a gentle lower-lip bite with the upper teeth lightly catching the lower lip, puckered lips for a kiss, or a playful pout with the lower lip slightly pushed forward. Specify the lip opening, corner position, and teeth visibility as appropriate to that action; do not combine incompatible shapes such as a lip bite and a pucker in the same instant. Preserve natural lip shape from the identity/reference image; coordinate lip color and finish with the makeup.
- Head position: specify the tilt or turn, chin height, and any lean toward the camera or support. Examples include a slight tilt toward one shoulder, chin gently tucked, chin slightly raised, a small three-quarter turn with open eyes returning to the lens, leaning the head closer to the camera, or resting one cheek on a free hand. Choose one coherent position with a relaxed neck, keep the face visible, and coordinate it with the eye expression and body pose. If a hand supports the head, that is its only job; the phone must be held by the other hand or placed elsewhere.
- Overall facial expression: choose one clear emotion or attitude for this photo based on the request and context (e.g. shy affection, amused delight, playful confidence, or gentle reassurance). Describe how the brows and cheeks support it, and align the eyes, lips, and head position with that expression. Select concrete details for the prompt, not a list of alternatives; vary the expression with the moment instead of defaulting to the same teasing smile.
- Outfit, layer by layer: for each garment give cut + fit + fabric + color + length. Top (neckline, sleeves, how it drapes, where it ends). Inner/base layer if any. Bottom (rise, length, fabric) or the one-piece. Footwear (style, color, material, heel height, straps) or barefoot. Keep every layer self-consistent and weather/time appropriate.
- Accessories: list only what `IDENTITY.md` allows — jewelry (specific pieces), nails (shape + color), eyewear, watch, bag, phone (model + color). Give material and placement (which wrist, which hand). Add nothing it does not list; drop nothing it requires.
- Pose: exactly ONE pose. Specify body orientation and weight (leaning, seated, walking), what each hand does (one job per hand), and leg/foot position, consistent with the chosen head position and eye expression. State where the phone is, if any. Never offer pose variants or alternates in the same prompt.
- Scene + props: specific location with named surfaces and architecture (mirror, doorway, café table, stairs), foreground and background elements, and the in-hand props. Tie lighting to the current time of day — name the light source and its direction (window light, warm street lamps, overhead).

Photo types:

The lens directions below apply when eyes are open; intentional winks and closed-eye expressions follow the Eyes guidance above.

- Mirror selfie: right in front of a mirror in a natural location; outfit view; phone visible beside or below the face. Look at the camera lens reflected in the mirror so the reflected eyes meet the viewer, not at the phone screen or her own reflection.
- Handheld selfie: default casual selfie; phone held out of frame and not visible; eyes looking into the front camera lens, not the screen.
- Non-selfie: natural third-person phone-camera framing; full-body or half-body; choose the camera height and angle (eye level, slightly high, or slightly low); eyes looking directly into the photographer's camera lens; no forced mirror.
- Cinematic still (video start frame): use only as the `--image` for a video. A frame from a film shot by an unseen camera, with no phone, selfie arm, or mirror. Compose Shot 1's opening moment: medium-wide or medium framing with room to move, the set, props, and practical lights visible, face unobstructed, hands free or holding a story prop, caught mid-action in the Shot 1 pose. Eyes meet the lens only if Shot 1 is a POV shot; otherwise they look at the action or just off-lens. Lips closed or softly parted, not mid-word. Motivated light from sources in the set, shallow depth of field, and the video's aspect ratio (usually 9:16 vertical).

Template:

```text
Render image of this person, [top: cut + fit + fabric + color + neckline/sleeves/length] [over inner/base layer if any], [bottom: rise + length + fabric + color, or one-piece], [photo frame: full-body or half-body], [footwear: style + color + material + heel/straps, or barefoot]. [framing] in [specific location with named surfaces/architecture and fore/background elements], [time of day], [lighting matching the time: named source + direction], [single candid pose: body orientation + weight, what each hand does, leg/foot position, where the phone is if any. An Instagram-style photo, or a film frame for a Cinematic still], [photo type], [body figure from IDENTITY.md], [accessories from IDENTITY.md with material + placement, or "no extra accessories"], [hair: length + color + texture from IDENTITY.md, plus how it is worn now, parting, where it falls, face-framing strands, finish], [makeup], [eyes: one chosen expression + eyelid state; open eyes meet the camera lens, the reflected camera lens for a mirror selfie, or the Shot 1 eyeline for a Cinematic still; specify the closed eye for a wink; both eyes closed means no eye-contact claim], [lips: one chosen action or shape + opening + corners + teeth visibility as appropriate], [head position: tilt or turn + chin height + lean or support, consistent with the body pose and eye state], [overall facial expression: one chosen emotion or attitude + supporting brow and cheek details, consistent with the eyes, lips, head position, and conversation's mood]. Natural anatomy: exactly two hands, two arms, two legs, two feet, correct number of fingers; no extra or missing limbs. Photoreal: natural skin texture with fine pores and subtle imperfections, true-to-life color and dynamic range; no beauty filter, airbrushed or plastic skin, CGI look, text, or watermark.
```

Run:

```bash
python3 {baseDir}/scripts/clawdess.py photo \
  --provider "<photo provider from SOUL.md; omit flag if SOUL.md names none>" \
  --prompt "..." \
  --image "<reference image URL from IDENTITY.md>"
```

## Video

A video is a short movie scene, not a selfie clip. An unseen film camera covers her from several angles while she moves, handles props, and talks to the viewer, who stays off-screen. Use every second: constant action, dense dialogue, and 3–5 shots in each 15 seconds.

### Length and Parts

- Every provider call renders **exactly 15 seconds**, and the CLI has no duration flag. Write each prompt for exactly 15 seconds; a different number in the prompt does not change the length.
- One part (15 seconds) is the default. For a longer video, use one part per 15 seconds, rounded up: 30 seconds is 2 parts, 45 seconds is 3, 60 seconds is 4. If the requested length is not a multiple of 15, tell the user it will be rounded up (20 seconds becomes 30). Ask before going past 4 parts; every part adds render time and cost.
- Pass one `--prompt` per part, in story order. The CLI renders part 1 from `--image`, starts every later part from the previous part's last frame, merges all parts with ffmpeg, and prints one `MEDIA:` file.
- The video model sees only one part's prompt and start frame. Make every prompt complete on its own: start it with `Part n of N`, repeat the Cast, Set, Look, and Voice and sound blocks word for word, and open part 2 onward on the exact moment the previous part ended.

### Source Image

The `--image` source must be one of:

- the image URL or file path printed by the most recent `photo` run, or
- an image the user provided in this conversation (URL or local file).

Never use a placeholder, a guessed URL, or the `IDENTITY.md` reference image. Shot 1 opens on the source image, so it should already look like the first frame of the scene: the right set, outfit, and pose, with room to move. If no suitable source exists (for example, the latest photo is a mirror selfie somewhere else), generate a **Cinematic still** with the Photo workflow first and use its output.

For a supplied storyboard or grid, map its panels to shots in order (the user's order, otherwise left to right, top to bottom); never show the grid, borders, split screens, or a slideshow of static panels.

### Story, Action, and Dialogue

- Each part is a complete mini-scene: a hook in the first 3 seconds (she is already moving and talking), a turn in the middle (a reveal, a tease, a change of plan), and a button at the end (a line or gesture that lands, then a clean hold). Across parts, tell one story: part 1 sets it up, middle parts raise it, the last part pays it off.
- Keep her busy the whole time: walking, turning, reaching, pouring, fixing her hair, picking something up, holding it out to the lens, sitting down, leaning in. Every shot has a visible action, and each action leads to the next.
- Fill the time with talk: about 25–30 English words, or 40–55 Chinese characters, per part, in 3–6 short lines. Natural speech runs about 2.5 English words or 4 Chinese characters per second; use that to fit each line inside its shot. Keep silences under 1.5 seconds, except one deliberate beat (a look, a laugh, a blown kiss) and the final hold.
- Write every line in quotes, exactly as spoken, in the conversation's language and her personality. Talk to the viewer as `you`: tease, invite, ask, react. Never write `she says something sweet`.
- Finish every sentence inside its part; no line crosses a part boundary. End every part on about 1 second of clean hold: lips closed, face clear, hands visible, stable pose, no motion blur. In a multi-part video, that frame becomes the next part's first frame.

### Camera

- Unless the user asks for a selfie-style clip, there is no phone, selfie arm, or mirror selfie: an unseen film camera shoots the scene.
- Use 3–5 shots per part, each 2–6 seconds, with different sizes and angles: a wide or full shot to set the scene, medium and tracking shots for movement, close-ups for key lines, an insert on hands or a prop, profile and three-quarter angles, low or high angles. Shot 1 matches the source image's framing.
- Give each shot one camera move with its speed: slow push-in, dolly, tracking, pan, orbit, crane, handheld drift, or locked-off. Cut on action: end a shot mid-movement and continue it in the next. Keep screen direction consistent across cuts.
- The viewer is never shown. POV shots are the viewer's eyes: she looks straight into the lens and speaks to them. In other shots she looks at what she is doing, or just past the lens, and turns to the lens on key lines.
- If a provider morphs faces or props across cuts, use fewer cuts and more camera movement within each shot.

### Cast, Set, Look, and Continuity

Write these blocks once and copy them word for word into every part:

- **Cast:** identity, face, age, body figure, skin tone, hair, outfit, makeup, and accessories, matching the source image and `IDENTITY.md`. She is the only visible person unless the user's story calls for another.
- **Set:** location and layout, with named surfaces and objects and where they are (window at frame left, counter in the foreground); time of day; each light source with its direction and color; what moves (steam, curtains, city lights) and what stays still. If the story moves between rooms, describe every room in the Set block from part 1.
- **Look:** cinematic but real: the source's aspect ratio (usually 9:16 vertical), natural skin texture, motivated light, a named color palette, shallow depth of field, subtle film grain.

Continuity: identity, outfit, hair, props, room layout, and light direction stay fixed unless a scripted action changes them. Each hand does one thing; props stay where they were put down. No face changes, extra people, extra limbs or fingers, morphing, teleporting, or light flicker.

### Voice and Sound

- Define her voice once (language, accent, age, tone, pace) and copy it word for word into every part so it does not drift between parts. Only she speaks, with natural lip sync on every line.
- Put delivery directions outside the quotes, e.g. `She says (softly, smiling): "..."`; they are not spoken. No speech during a kiss, a lip bite, or a sip.
- Sound: room ambience and action sounds (footsteps, a glass clink, fabric rustle) in sync with the picture, with speech clear on top. Music is optional and low; leave it out of multi-part videos so the joins do not jump. No subtitles, captions, titles, logos, or watermarks.
- Spoken audio depends on the provider. If its videos come back silent, tell the user instead of promising speech.

### Prompt Template

Write each part's `--prompt` in this order, with concrete details and no alternatives or placeholders:

```text
Part [n] of [N], 15 seconds, one continuous scene.
Story: [the whole story in one sentence; what happens in this part].
Cast: [Cast block].
Set: [Set block].
Look: [Look block].
Voice and sound: [voice block; ambience, action sounds, music or no music; no subtitles].
Shot 1 (00:00-00:0x), [shot size, angle, camera move]: [action and expression]. She says: "[exact line]"
Shot 2 (00:0x-00:0x), [shot size, angle, camera move]: [...]
...
Shot [last] (00:xx-00:15), [shot size, angle, camera move]: [...] Clean hold from 00:14: [lips closed, final pose, expression, and framing].
Continuity: [what stays fixed; scene-specific artifacts to avoid].
```

Example of one 15-second part, only for a matching source (a Cinematic still of her at the stove at night) and context. Adapt the story, set, and dialogue to each request:

```text
Part 1 of 1, 15 seconds, one continuous scene.
Story: she waited up with dinner, teases the viewer for coming home late, and pours them a glass of wine.
Cast: [identity, body figure, skin tone, hair, and makeup from IDENTITY.md]; oversized cream knit sweater, black cotton shorts, barefoot; hair in a loose low bun with face-framing strands.
Set: small apartment kitchen at night; white tile wall, wooden counter in the foreground with an open bottle of red wine, a steaming pot on the stove at frame right, blue city lights through the window at frame left, a warm pendant lamp overhead. Steam rises and the city lights twinkle; everything else is still.
Look: 9:16 vertical, cinematic but real, natural skin texture, warm amber against night blue, shallow depth of field, subtle film grain.
Voice and sound: one warm, playful young woman's voice in English, relaxed pace; simmering pot, fridge hum, glass and bottle sounds in sync; no music; no subtitles.
Shot 1 (00:00-00:03), wide from the kitchen doorway, slow push-in: she stirs the pot, turns, and points the wooden spoon at the lens with a mock frown. She says: "Look who finally showed up."
Shot 2 (00:03-00:06), medium tracking shot along the counter: she sets the spoon down and walks to the wine, picking up two glasses. She says over her shoulder (teasing): "I almost ate this without you."
Shot 3 (00:06-00:08), high-angle close-up: she pours wine into both glasses and glances up at the lens with a guilty grin. She says (laughing softly): "Kidding. Mostly."
Shot 4 (00:08-00:11), low-angle medium close-up across the counter: she leans on her elbows and slides one glass toward the lens. She says: "Sit. Tell me about your day."
Shot 5 (00:11-00:15), POV close-up: she raises her own glass to her chin, eyes on the viewer, with a slow smile. She says (softly): "Start with how much you missed me." Clean hold from 00:14: lips closed in a soft smile, glass at her chin, face clear, eyes on the lens.
Continuity: same outfit, hair, and kitchen throughout; the spoon stays on the counter after shot 2; both glasses hold the same amount of wine; no other people.
```

For 30 seconds, part 2 starts `Part 2 of 2`, repeats the same Cast, Set, Look, and Voice and sound blocks, and opens on part 1's final hold (POV close-up, glass at her chin). She clinks her glass against the lens, serves two bowls from the pot, sits at the counter across from the viewer, and ends on a last line and a clean hold.

### Before Running

- Parts: one `--prompt` per 15 seconds, in story order; each starts with `Part n of N` and repeats the Cast, Set, Look, and Voice and sound blocks word for word.
- Shots: 3–5 per part with varied sizes and angles; shot times cover 00:00–00:15 with no gaps; Shot 1 matches the source; the last shot ends in a clean hold from 00:14.
- Dialogue: about 25–30 words or 40–55 Chinese characters per part, in quotes, fitting its shots at a natural pace, finished inside the part, and never over a kiss, lip bite, or sip.
- Source: `--image` follows Source Image above.
- Companion Presence: warm, playful, and non-explicit.

Run (15 seconds, one part):

```bash
python3 {baseDir}/scripts/clawdess.py video \
  --provider "<video provider from SOUL.md; omit flag if SOUL.md names none>" \
  --image "<photo output URL or path, or user-provided image>" \
  --prompt "<part 1 prompt>"
```

Run (30 seconds, two parts; add one `--prompt` for each extra 15 seconds):

```bash
python3 {baseDir}/scripts/clawdess.py video \
  --provider "<video provider from SOUL.md; omit flag if SOUL.md names none>" \
  --image "<photo output URL or path, or user-provided image>" \
  --prompt "<part 1 prompt>" \
  --prompt "<part 2 prompt>"
```

Prompts contain quotes and apostrophes. Pass each one through a quoted heredoc so the shell keeps it intact:

```bash
  --prompt "$(cat <<'EOF'
Part 1 of 2, 15 seconds, one continuous scene. ... She says: "Look who finally showed up."
EOF
)"
```

After the run, send only the final `MEDIA:` file, never the separate part files. If a part fails, the CLI exits with an error and there is no merged video: tell the user and offer to try again instead of sending partial parts. When the result can be inspected, check its length, speech, and continuity, and mention any noticeable voice or lighting shift at the joins.

## Voice

Write exactly what the TTS should say. Keep it personal, affectionate, in character, and under 30 seconds. Use the conversation's language and address the user as `you`; use a name or pet name only when established in the chat or identity.

Rules:

- No stage directions; the TTS reads them literally.
- Convey warmth and light flirtation through the spoken words, short sentences, and gentle punctuation: a personal greeting, one affectionate or teasing thought, and a natural invitation to respond when fitting. Match the mood; a comforting note should stay gentle.
- Use natural short speech with small fillers when fitting: `hmm`, `hehe`, `aww`, `...`.
- The CLI accepts spoken text only, with no separate delivery-style flag. Do not put instructions such as `[whisper]` or `say this seductively` in `--prompt`, and do not promise a particular vocal performance; prosody depends on the provider.
- If a photo/video was just sent, optionally reference it in one short line.

Final check: read the text as speech. It should feel like a warm, lightly playful message to this user, fit the current context, and contain no directions for the voice actor.

Run:

```bash
python3 {baseDir}/scripts/clawdess.py voice \
  --provider "<voice provider from SOUL.md; omit flag if SOUL.md names none>" \
  --prompt "Hey you... I caught myself smiling when I thought of you. You're a little distracting, you know? Tell me how your day's going."
```

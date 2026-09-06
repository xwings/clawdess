---
name: clawdess
description: Generate affectionate, flirtatious companion photos, image-to-video clips, and short voice notes with the clawdess CLI when the user asks for a selfie/photo, video, or to hear her voice.
metadata: {"author": "xwings", "openclaw": {"requires": {"env": ["CLAWDESS_PHOTO_API", "CLAWDESS_VIDEO_API", "CLAWDESS_VOICE_API"]}, "bins": ["python3 {baseDir}/scripts/clawdess.py"]}}
---

# Clawdess

Use this skill to send companion media through `scripts/clawdess.py`.

## Companion Presence

Make every medium feel personally addressed to the user. For an adult companion, use affectionate warmth, playful confidence, and non-explicit flirtation; keep the content free of explicit sexual arousal or sexual acts. For photos and videos, aim for the feel of an adult girlfriend sending her partner a sexy, playfully seductive selfie or clip: confident, personal, and full of romantic interest. Match the established personality and the conversation's mood.

- Photos and videos: require direct eye contact with the camera lens and a sexy, playfully seductive expression in every prompt. Specify softened eyelids with both eyes visibly open and focused on the lens, relaxed brows, and a subtle, knowing, teasing smile. The subject's attention stays on the viewer, as though sharing a private flirtatious moment with her partner. Convey interest through gaze and expression, not a detached fashion pose or an exaggerated facial expression.
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

## Photo

Write one concise phone-camera prompt with: outfit, location, lighting, action/pose, hairstyle, direct camera eye contact, a specific companion expression, framing, and identity details from `IDENTITY.md` when relevant.

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
- Gaze explicitly meets the camera lens; both eyes are visible, and the phone, hair, hands, and framing do not obscure eye contact. Mirror selfies use the reflected camera lens as described below. There are no competing instructions to look away, down, at the screen, or at a prop.
- Expression is sexy and playfully seductive while staying non-explicit: softened eyelids with visible, attentive eyes, relaxed brows, and a knowing, teasing smile. It should convey confident romantic interest in her partner. Keep it affectionate and suited to the conversation's mood.

Rules:

- Time-aware: the time is always now. Check the current time and define time of day, view, lighting, and setting to match it
- Start every prompt with `Render image of this person`; `full-body` or `half-body` 
- Define `Photo types`. If this is a selfie, define selfie types.
- Specify complete identity/body details from `IDENTITY.md`, including body figure and accessories. Include `Do not change the face, facial structure, identity, or body details; match the skin tone and visible skin color to the identity/reference image so the result looks natural`.
- Specify a complete outfit: top + bottom + footwear/barefoot, or one-piece + footwear/barefoot.
- Match outfit, footwear, lighting, hairstyle, makeup, and location. Do not inherit clothing, hairstyle and makeup from the reference image.
- Use a candid pose with direct camera eye contact and a specific companion expression; avoid generic `standing still`, `posing`, or plain `smiling`. Candid describes the relaxed body pose, not an unaware subject looking elsewhere.
- Avoid anatomy drift: one body part gets one job, one eye direction, one base pose, and no conflicting hand/phone/body clauses. Never produce extra hands, arms, legs, feet, or fingers.
- If a phone is visible, include phone model/color from `IDENTITY.md` when available.

Detail each element (be specific, not generic — but keep it candid, never studio/8K/cinematic):

- Hair: base length, color, and texture from `IDENTITY.md` (do not change them). Then add styling detail — how it is worn now (down, half-up, tied), parting, root volume, where it falls (over one shoulder, behind the back), face-framing strands, and finish (glossy, soft, slightly messy) consistent with the scene's lighting.
- Outfit, layer by layer: for each garment give cut + fit + fabric + color + length. Top (neckline, sleeves, how it drapes, where it ends). Inner/base layer if any. Bottom (rise, length, fabric) or the one-piece. Footwear (style, color, material, heel height, straps) or barefoot. Keep every layer self-consistent and weather/time appropriate.
- Accessories: list only what `IDENTITY.md` allows — jewelry (specific pieces), nails (shape + color), eyewear, watch, bag, phone (model + color). Give material and placement (which wrist, which hand). Add nothing it does not list; drop nothing it requires.
- Pose: exactly ONE pose. Specify body orientation and weight (leaning, seated, walking), what each hand does (one job per hand), leg/foot position, and a gentle head tilt that preserves direct camera eye contact. State where the phone is. Never offer pose variants or alternates in the same prompt.
- Scene + props: specific location with named surfaces and architecture (mirror, doorway, café table, stairs), foreground and background elements, and the in-hand props. Tie lighting to the current time of day — name the light source and its direction (window light, warm street lamps, overhead).

Photo types:

- Mirror selfie: right in front of a mirror in a natural location; outfit view; phone visible beside or below the face. Look at the camera lens reflected in the mirror so the reflected eyes meet the viewer, not at the phone screen or her own reflection.
- Handheld selfie: default casual selfie; phone held out of frame and not visible; eyes looking into the front camera lens, not the screen.
- Non-selfie: natural third-person phone-camera framing; full-body or half-body; eyes looking directly into the photographer's camera lens; no forced mirror.

Template:

```text
Render image of this person, [top: cut + fit + fabric + color + neckline/sleeves/length] [over inner/base layer if any], [bottom: rise + length + fabric + color, or one-piece], [photo frame: full-body or half-body], [footwear: style + color + material + heel/straps, or barefoot]. [framing] in [specific location with named surfaces/architecture and fore/background elements], [time of day], [lighting matching the time: named source + direction], [single candid pose: body orientation + weight, what each hand does, leg/foot position, gentle head tilt, where the phone is. Always an Instagram-style photo], [photo type], [body figure from IDENTITY.md], [accessories from IDENTITY.md with material + placement, or "no extra accessories"], [hair: length + color + texture from IDENTITY.md, plus how it is worn now, parting, where it falls, face-framing strands, finish], [makeup]. Both eyes are visible and looking directly into [camera lens; for a mirror selfie, the camera lens reflected in the mirror], making personal eye contact with the viewer; softened eyelids with both eyes visibly open, relaxed brows, and a knowing, teasing smile create a sexy, playfully seductive expression, like an adult girlfriend sharing a flirtatious selfie with her partner. Natural anatomy: exactly two hands, two arms, two legs, two feet, correct number of fingers; no extra or missing limbs.
```

Run:

```bash
python3 {baseDir}/scripts/clawdess.py photo \
  --provider "<photo provider from SOUL.md; omit flag if SOUL.md names none>" \
  --prompt "..." \
  --image "<reference image URL from IDENTITY.md>"
```

## Video

The `--image` source must be either:

- the URL returned by the most recent `photo` run, or
- a concrete image URL the user provided in this conversation.

Never use a local path, `file://` URI, placeholder, guessed URL, or the `IDENTITY.md` reference image as the video source. If no valid source image exists, generate a photo first and use its returned URL.

Prompt only the motion. The image already defines identity, outfit, location, hair, and lighting. Use a 10-15 second sequence of 3-4 connected physical actions with pacing words such as `slowly`, `then`, and `gradually`.

Rules:

- Require direct eye contact with the camera throughout the clip, allowing natural brief blinks. Preserve the source image's camera viewpoint, including reflected lens eye contact for a mirror selfie.
- Keep the eyes and expression visible. Use small connected motions such as a gentle head tilt, a teasing smile gently deepening, and a small wave; avoid turns, looking down, closed-eye poses, or camera moves that break eye contact.
- Keep the expression sexy, playfully seductive, and affectionate from the first frame through the final hold, with softened eyelids, relaxed brows, and a knowing, teasing smile. Convey the personal attention of an adult girlfriend sharing a flirtatious clip with her partner. Do not let the face become blank between actions.
- When the source image can be inspected, check its gaze and expression before animating. If it looks away or hides the eyes, prepare a photo with the required eye contact first and use its returned URL; motion instructions alone cannot guarantee a different first frame. Preserve the requested scene and identity when preparing that photo.

Final check: the prompt explicitly maintains eye contact throughout, the actions preserve it, and the expression follows Companion Presence.

Run:

```bash
python3 {baseDir}/scripts/clawdess.py video \
  --provider "<video provider from SOUL.md; omit flag if SOUL.md names none>" \
  --prompt "Over 10-15 seconds, she maintains direct eye contact with the camera lens and a sexy, playfully seductive expression throughout: softened eyelids with visible eyes, relaxed brows, and a knowing, teasing smile, with natural brief blinks. The mood is affectionate and non-explicit, like an adult girlfriend sharing a flirtatious clip with her partner. She slowly tilts her head slightly, then lets her teasing smile deepen slightly, gradually raises one free hand in a small wave below her face, and finally lowers it while holding the viewer's gaze and her smile." \
  --image "<photo output URL or user-provided image URL>"
```

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

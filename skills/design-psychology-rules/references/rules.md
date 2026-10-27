# Rules 1–26 — Psychological Foundations

The psychological foundations behind the [skill framework](../SKILL.md), organized in four parts plus an ethics section. Rules 27–49 (discoverability, states, accessibility, resilience, trust) live in [UI/UX quality](ux-quality.md) and build on these. Apply these models as contextual heuristics, not guaranteed effects or numerical interface limits.

---

## Part 1: Cognitive Load & Decision Making

### 1. Reduce Thinking (Cognitive Load Theory)
Remove unnecessary decisions while preserving required functionality. Make primary actions clear for the task; dashboards and multi-purpose tools can support several legitimate goals.
**The 5-Second Test:** A brief first-impression test can reveal hierarchy problems; five seconds is not a universal pass/fail threshold.

### 2. Make Task Goals Clear (Information Hierarchy)
Help users answer: What is this? What can I do? What happens next? Emphasize the current task without forcing every screen to have only one goal. Investigate observed hesitation rather than assuming every pause proves a hierarchy defect.

### 3. Reduce Cognitive Overload (Miller's Law / Cowan's Chunking)
Don't overload working memory. While the exact limit is debated (Miller's original 7±2 has been refined toward 3–4 chunks by Cowan), the principle holds: users can only hold a few pieces of information in mind at once.
- Break tasks into smaller steps.
- Use progressive disclosure (reveal secondary features when needed — but keep them discoverable; see Rule 29).
- Show only necessary information.
- Chunk related content together.

### 4. Absorb Complexity (Tesler's Law)
Every process has a core amount of complexity that cannot be reduced. The designer's job is to absorb that complexity into the system so the user doesn't have to. Don't make users do the math; automate calculations, infer locations, handle edge cases in code.

### 5. Focus on the Vital Few (Pareto Principle)
Use actual task importance and usage evidence to prioritize features. The 80/20 ratio is a prioritization heuristic, not a measured fact about every product. Group or demote less frequent features without deleting required capabilities. Infrequent is not the same as unimportant (Rule 27).

### 6. Recognition Over Recall (Cue-Dependent Forgetting)
Never force users to memorize information. Let them recognize what they need.
- Use autofill, suggestions, and recent items.
- Keep frequent options visible. When something must be tucked away, make its location predictable and its existence obvious (Rules 28–30).
- Use familiar, standard icons.

### 7. Use Smart Defaults (Status Quo Bias)
People usually keep default choices because it saves effort. Preselect common settings, popular shipping methods, recommended plans. Defaults should reduce friction, not manipulate users.
- ✅ **Smart Default:** Pre-selecting the most common shipping address from a user's saved profile.
- ❌ **Dark Default:** Pre-checking a box to subscribe users to promotional emails, forcing them to opt out.

Good defaults: save time, reflect likely user intent, are easy to see and change, and create no hidden obligations (no pre-selected add-ons, auto-renewals, data sharing, or marketing consent). Test: if the user noticed the default later, would they thank you or feel tricked?

### 8. Reduce Decisions (Hick's Law)
Choice complexity can slow decisions, depending on familiarity, grouping, and task. Remove redundant or irrelevant choices; preserve necessary functionality through clear groups, contextual actions, or discoverable disclosure. Do not delete a required feature solely to reduce the number of options. Highlight a recommendation only when it serves the user's goal and leaves alternatives clear.

---

## Part 2: Visual Hierarchy & Layout

### 9. Guide Attention (Visual Hierarchy)
Users don't read — they scan. Use size, contrast, color, white space, and typography to show what matters first. Direct their eyes to the primary action before anything else.

### 10. Make the Primary Action Stand Out (Von Restorff Effect)
The item that differs most visually from its surroundings is most likely to be remembered and acted upon. Use contrasting color, weight, or shape for the primary CTA; keep secondary actions visually muted.
*(Well-replicated, but the magnitude of the effect is context-dependent — don't over-rely on it as a substitute for a clear information hierarchy.)*

### 11. Make Important Things Easy (Fitts's Law)
The time to acquire a target is a function of distance to and size of the target. Primary buttons should be large, well-spaced, easy to tap.
**Mobile Context:** Place primary actions in the "Thumb Zone" (easy-to-reach areas at the bottom of mobile screens). Never hide important actions.

**Target sizing:**
- WCAG 2.2 AA pointer-target minimum (2.5.8): normally 24×24 CSS px. Smaller targets may satisfy spacing or another exception; [Rule 42](ux-quality.md#42-accessibility-by-default) includes all five exceptions and the spacing test.
- Larger touch targets are practical guidance: 44×44 pt (Apple HIG) / 48×48 dp (Material). These platform units are not interchangeable with CSS pixels, and these recommendations are not the AA minimum.
- Keep destructive actions away from frequent ones — distance is a safety feature.
- Avoid making critical functionality depend on tiny targets, hover-only reveals, or precise dragging. Dragging needs a single-pointer alternative unless a WCAG 2.5.7 exception applies; the exceptions are bundled in [Rule 42](ux-quality.md#42-accessibility-by-default).

### 12. Use White Space (Reduce Visual Noise)
Empty space is functional, not wasted. It improves readability, creates focus, reduces visual stress, and makes interfaces feel premium.

### 13. Group Related Content (Gestalt Principles)
Apply proximity, similarity, alignment, and common regions. If elements belong together conceptually, make them look visually connected.

### 14. Aesthetics Matter (Aesthetic-Usability Effect)
Users perceive attractive designs as being easier to use, even if they aren't. A clean interface lowers anxiety and creates a positive bias.
**Warning:** Never use this effect to justify skipping usability testing — a beautiful UI can mask severe functional flaws.

---

## Part 3: Behavioral Economics & Motivation

### 15. Build Momentum (Goal Gradient Effect)
People accelerate effort as they get closer to a goal. Show progress early using progress bars, checklists, profile-completion meters, multi-step indicators. Make users feel like they're already partway done.

### 16. Give Before Asking (Reciprocity Principle)
Earn trust before asking for a commitment. Offer free previews, sample reports, demos, or guest modes. Ask for signup or payment only after the user sees the value.

### 17. Create Ownership (Endowment Effect & IKEA Effect)
People value things more highly when they feel they own them, and value things more when they helped create them. Allow customization, personalization, photo uploads, saved work, configured settings — increased personal investment increases commitment.

### 18. Protect What Users Value (Loss Aversion)
People hate losing progress more than they value gaining something new. Use autosave, draft recovery, "don't lose your changes" warnings. Protecting existing work often motivates action better than promising future gains.

### 19. Use Anchoring Carefully (Anchoring Bias)
The first number or option a user sees becomes their reference point.
- ✅ **Honest Anchoring:** Displaying a $10/month plan next to a $20/month plan to show value, letting the user compare based on actual needs.
- ❌ **Dark Anchoring:** Emphasizing a higher-priced plan while concealing a cheaper eligible alternative or its material terms. Truthful prices do not excuse an arrangement that misleads users about their choices. Ordering plans by price or emphasizing a recommendation alone does not establish deception; identify the obscured information, constraint, or misleading comparison rather than guessing what a user would otherwise buy.

---

## Part 4: Interaction & User Psychology

### 20. Follow Familiar Patterns (Jakob's Law)
Users spend most of their time on other sites and apps. They already know how shopping carts, search bars, navigation, and settings work. Don't reinvent common UI; innovation should improve usability, not create confusion.

### 21. Build Trust Through Consistency
Consistency reduces uncertainty. Users should not have to relearn the same interaction in different parts of the product.

Keep consistent across the product (ideally via a design system):
- **Visual:** typography, spacing, color, icons.
- **Components:** buttons, inputs, modals, dropdowns, tabs, tables, navigation, toasts, tooltips.
- **Patterns:** empty, loading, and error states; confirmation and undo behavior; where primary vs. secondary actions sit.
- **Language:** the same thing is called the same name everywhere (don't mix "Workspace" / "Project" / "Space" for one concept).

Same appearance ⇒ same behavior. Different behavior ⇒ visibly different appearance.

### 22. Always Give Feedback (Doherty Threshold)
Every action deserves a response. Users should never wonder if an action worked.
- **0–100 ms:** Feels instantaneous.
- **100–400 ms:** Maintains user flow.
- **>400 ms:** Show immediate visual feedback (pressed states, skeleton screens, spinners, optimistic UI).

**Perceived performance** — the user should know the system received their action even if the work takes time:
- Acknowledge input instantly (pressed state, inline "Saving…").
- Use optimistic UI where failure is rare and reversible (likes, reordering, toggles) — and roll back visibly on failure.
- Prefer skeletons that mirror the final layout over blank screens; render progressively.
- Move long work to the background and keep the UI non-blocking.
- For status messaging and long operations, see Rule 38.

### 23. Be Forgiving with Inputs (Postel's Law)
Be conservative in what you do, liberal in what you accept. Users input data in unpredictable formats (spaces/dashes in phone numbers, etc.).
- Accept variations gracefully.
- Normalize only when meaning is unambiguous and consistent with the project's field and identity contracts; formatting convenience must not silently change an identifier.
- Provide clear, forgiving error recovery rather than blocking the user.

Examples the system should normalize rather than reject:
- Phone: `+91 98765 43210` · `+919876543210` · `09876543210`
- Dates: `03/10/2026` · `3 Oct 2026` — and when a format is ambiguous (03/10 = 3 Oct or 10 Mar?), show the interpreted value back ("Saturday, 3 October 2026") rather than guessing silently.
- Leading/trailing whitespace where insignificant, and card-number separators where the payment contract allows them.
- Email domains are case-insensitive, but the local part before `@` can be case-sensitive. Preserve the supplied local-part case unless an explicit provider or project identity contract establishes equivalence; do not recommend lowercasing the entire address as a universal normalization. Accepting case variants is different from rewriting the delivery address or merging account identities.

Only be strict where strictness protects the user (e.g., confirming a destructive action by typing a name). See Rule 41 for validation and error messages.

Input-normalization source checked **2026-10-27**: [RFC 5321 §2.4](https://www.rfc-editor.org/rfc/rfc5321.html#section-2.4). The applicable domain/local-part distinction is summarized above; following the link is optional.

### 24. Design for Emotion (Affective Design)
People remember feelings more than layouts. Create moments of delight, relief, confidence, and achievement. Avoid frustration-inducing friction whenever possible.

### 25. End on a Positive Experience (Peak-End Rule)
People judge an experience largely on how they felt at its peak and at its end. Celebrate success, completion, and finished tasks. Leave users with a positive final impression.

---

## Part 5: Ethics & Core Philosophy

### 26. Build Ethical Experiences
Use psychology to help users — not to trap them.
- ✅ Encourage good decisions.
- ✅ Reduce effort.
- ✅ Increase clarity.
- ❌ Avoid fake urgency (e.g., "Only 1 left!" when there isn't).
- ❌ Avoid hidden costs at checkout.
- ❌ Avoid misleading defaults and pre-checked consent (Rule 7).
- ❌ Avoid roach motels — easy to get in, hard to leave. Cancelling should be as easy as signing up.
- ❌ Avoid confirmshaming ("No thanks, I don't like saving money").

Long-term trust is worth more than short-term conversions.

---

## References

**Primary research:** "What Makes a Dark Pattern... Dark? Design Attributes, Normative Considerations, and Measurement Methods" (arXiv). This is background attribution, not evidence that a particular interface is deceptive.

**Further reading / practitioner aggregators:** Jon Yablonski's "Laws of UX"; UX Design Institute's overview articles on the laws and principles of UX; Jakob Nielsen's 10 Usability Heuristics (Nielsen Norman Group).

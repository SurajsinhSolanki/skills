# Mobile Review (React Native · Flutter · native iOS/Android)

Mobile PRs carry failure modes web reviews do not: the app persists for weeks, ships behind a store review, and runs offline.

Contents: [Applicability and offline use](#applicability-and-offline-use) · [Release and compatibility](#release-and-compatibility) · [Permissions and privacy](#permissions-and-privacy) · [Lifecycle and background](#lifecycle-and-background) · [Network and offline](#network-and-offline) · [Rendering](#rendering) · [Platform parity and accessibility](#platform-parity-and-accessibility) · [Worked example and counterexample](#worked-example-and-counterexample) · [Sources and maintenance](#sources-and-maintenance)

## Applicability and offline use

React Native, Flutter, native Android/iOS. Inspect app/framework/SDK versions, supported OS range, storage schema, permissions, and release/deployment configuration. Evaluate only platforms actually changed; store-policy compliance cannot be assumed current without locally supplied evidence.

This file contains the review checks and examples needed offline. Source links are optional attribution. Verify a check against local code/configuration before reporting; unknown version-specific behavior remains unverified. Shared severity, gates, and opt-ins stay in the bundled skill.

## Release and compatibility
- Installed app versions can outlive a server deploy. Check which supported clients consume the changed response and whether compatibility, version negotiation, or a migration path is required. An added optional field does not inherently break existing builds.
- Persisted local state (DB, secure store, cached JSON) written by a previous version must still parse. A schema change needs a migration path, not just new code.
- Minimum OS version and permission declarations changed — verify the store requirements and that removed permissions are not still used.
- Deep-link and universal-link changes: an unregistered route sends users nowhere; an over-broad host pattern lets another app intercept.

**Evidence and correction:** List the installed client/server combinations and persisted data versions that must coexist. Test upgrade, cold start, older server response, and old deep links. Require an actual incompatible parse or route before asserting all installed builds break.

## Permissions and privacy
- Permission requested at the point of need, with the rationale string set, and the denied and "ask again" paths handled — not just granted.
- Data collected must match the store privacy declaration; a new analytics or crash-reporting field can make an existing declaration false.
- Secrets in the bundle are readable. API keys in the app are public; anything signing a privileged request must live server-side.
- Tokens in secure storage (Keychain / Keystore), never in plain preferences or async storage.
- Screenshots, logs, and clipboard containing personal data.

**Evidence and correction:** Test permission denied/restricted/revoked states and data leaving the device. Secure storage protects tokens at rest but cannot make a privileged server signing secret safe inside an app bundle. Public API identifiers are distinct from secret credentials.

## Lifecycle and background
- Work started in the foreground continuing after backgrounding — on iOS it is suspended, not paused. Long uploads need a background task or a resume path.
- State restoration after the OS kills the process; a flow that assumes in-memory state survives is a bug users hit constantly.
- Listeners, observers, and timers removed on unmount/dispose — a leak here drains battery, which users notice and report.
- Push notification handling in all three states: foreground, background, terminated.

**Evidence and correction:** Simulate background/foreground, process termination, and replayed notifications. Persist the minimum resumable state and make long work owned by an appropriate platform mechanism. A ViewModel or in-memory store alone does not survive process death.

## Network and offline
- Offline and flaky-network paths: retry with backoff, a visible error, and no infinite spinner.
- Requests cancelled on navigation away, so a late response does not overwrite fresh state.
- Cache invalidation after a mutation, and a pull-to-refresh that actually refetches.
- Payload size and image dimensions matter on cellular — flag full-resolution images in a list.

**Evidence and correction:** Exercise delayed/out-of-order responses, reconnect, and repeated submit. Define deduplication, retry, and visible failure states according to whether work is safe to repeat. Bound payloads and image decode size using device constraints.

## Rendering
- **React Native**: virtualize genuinely long lists and keep stable keys; measure JS/UI thread work. Animation driver support depends on the animated properties/library. Check the installed architecture/runtime and native-module compatibility; do not require deprecated scheduling APIs or a particular list library.
- **Flutter**: keep build free of side effects, bound rendering work, and dispose owned controllers/subscriptions. After an await, check mounted before using a context that may be invalid or calling setState. A mounted context can be used after await; const syntax alone is a style/performance consideration.
- Native: main-thread work, autolayout thrash, and view recycling correctness in list adapters.

**Evidence and correction:** Measure list scrolling, rebuild cost, and thread work in the relevant architecture. Apply only supported animation/list APIs. Flutter mounted checks and controller disposal need the correct owner, not blanket bans on await or setState.

## Platform parity and accessibility
- Both platforms verified, not just the reviewer's simulator. Safe-area insets, keyboard avoidance, back-gesture and hardware-back behavior, and text scaling at large font sizes.
- Accessibility labels on tappable elements, minimum touch target size, screen-reader order, and sufficient contrast.
- Localization: strings externalized, and layouts that survive longer translations and right-to-left.

**Evidence and correction:** Inspect screen-reader semantics, text scaling, focus, keyboard/back behavior, and locale layouts on changed platforms. Missing access to one device is an honest verification gap, not evidence that the code fails there.

## Worked example and counterexample

```dart
// Defect if the user leaves while the request is pending.
final result = await load();
setState(() => value = result);
// Correction inside State after the same await:
if (!mounted) return;
setState(() => value = result);
```

The first setState is the version to replace, not a call to keep before the guard. Cancellation and error handling may still be required for the actual operation.

## Sources and maintenance

[Android state persistence](https://developer.android.com/topic/libraries/architecture/saving-states); [Flutter background work](https://docs.flutter.dev/cookbook/networking/background-parsing); [React Native lists](https://reactnative.dev/docs/optimizing-flatlist-configuration). Source checks: **2026-10-26**. This is a review-focused summary in original wording, not a complete vendor manual or a guarantee for unlisted/newer versions. Recheck source claims when maintaining this file; ordinary reviews need no network.

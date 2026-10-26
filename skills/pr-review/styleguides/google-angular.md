# Google Angular Style Guide — Review Checklist

Source: [Angular Style Guide](https://angular.dev/style-guide) (linked from Google's style guide index). Optional attribution and maintenance reference; all review rules below are bundled locally and summarized in original wording.

Apply the shared opt-in, precedence, reporting, and bug-risk rules in the [style guide index](README.md#applying-guides).

Load on top of `google-typescript.md` for Angular code. Behavioral Angular issues (subscriptions, change detection) live in `frameworks/angular.md`; this file is about conventions.

Contents: [Scope and offline use](#scope-and-offline-use) · [Naming and structure](#naming-and-structure) · [Components and directives — to flag](#components-and-directives--to-flag) · [Additional local conventions](#additional-local-conventions) · [Example and review decision](#example-and-review-decision)

## Scope and offline use

Current Angular style snapshot; determine framework generation and whether signal or decorator APIs are used. Apply TypeScript conventions through the bundled TypeScript guide when opted in.

Apply only when opted in and on changed lines. Project rules/formatter output take precedence. Style observations are non-blocking; bug-risk markers need a concrete verified failure. No external page is required to apply this file. Source snapshot checked: **2026-10-26**.

## Naming and structure
- File names hyphenated (`user-profile.ts`); tests share the base name with `.spec.ts`. A component's TS, template, and styles share one base name.
- File names reflect the primary class they contain. One concept per file.
- Organize by feature, not by type — new `components/` or `services/` catch-all folders are a finding.

**Application and exceptions:** Feature grouping and matching test names improve discovery; do not force renaming a stable public/framework contract for cosmetic consistency.

## Components and directives — to flag
- Constructor injection where `inject()` is the project's pattern.
- Angular members (injected deps, inputs, outputs, queries) not grouped before methods.
- Template-only members left `public` instead of `protected`.
- Signal-based input/model/output/query references should not be reassigned. For decorator APIs, this applies to output/query properties, not Angular-assigned @Input properties.
- `ngClass` / `ngStyle` where `[class]` / `[style]` bindings would do.
- Event handlers named for the event (`onClick`) rather than the action (`saveDraft`).
- Lifecycle hooks without their interface (`implements OnInit`), or hook bodies holding logic instead of delegating to named methods.
- Business logic in components; complex logic in templates instead of TypeScript (computed values or signals).

**Application and exceptions:** Use readonly for references Angular should not have replaced, while decorator inputs may be assigned by Angular. A documented older project pattern overrides newer signal/inject preferences.

## Additional local conventions

Formatting/imports/documentation: use the project’s TypeScript formatter and normal module imports; preserve third-party import names. Document non-obvious public component inputs/outputs and lifecycle assumptions rather than adding comments to every template member.

## Example and review decision

```ts
export class UserProfile {
  readonly userId = input<string>(); // reference stays fixed; signal value can change
  protected saveDraft() { /* existing action */ }
}
```

For @Input() name = "", Angular’s assignment is expected; blanket readonly advice from signal inputs does not apply.

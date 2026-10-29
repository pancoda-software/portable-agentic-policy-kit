# Nuxt / Vue project profile

- For a **new** Nuxt project, prefer the current supported stable Nuxt major; for an **existing** project, preserve its pinned version until an upgrade is separately approved. Avoid forced Nuxt 3 → 4 migrations during unrelated feature work.
- Default stack when applicable: Nuxt, Nuxt UI, Vue, Tailwind CSS. Check actual versions and project conventions before generating code.
- Use Pinia for shared *domain/workflow state* across components; use local Vue refs/computeds for ephemeral component state. Keep server-fetched data in appropriate Nuxt data/composable flows (`useFetch`, `useAsyncData`) and avoid unnecessary duplication in stores.
- Read real backend contracts/OpenAPI before building typed API clients. Address loading, empty, error, validation, retry and stale-response/race states.
- Inspect SSR and hydration implications, bundle weight and accessibility before adding UI dependencies or animation packages.
- Prefer native Nuxt UI controls and Vue-compatible a11y patterns; skip React-specific suggestions from portable UI skills.
- Create/maintain focused Vitest tests for introduced logic and relevant integration paths. Use existing package scripts (e.g. `test`, `lint`, `typecheck`, `build`) only after checking their definitions and side effects.
- Validate the full user journey before and after the new action: pending state, error feedback, success state and re-entry/back-navigation.

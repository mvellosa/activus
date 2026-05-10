# AGENTS.md

This file gives new AI agents a quick mental model of the project so they can add features without needing to read the entire codebase first.

## Project Overview

This is a small Flet application structured around:

- a single app shell that owns shared state and navigation
- page modules that compose screen-level layouts
- reusable UI components for visual building blocks
- backend and model layers that keep data access separate from UI

The main goal when extending the app is to keep those boundaries clear.

## Directory Structure

- `src/main.py`
  Entry point. Creates the app and injects the backend.

- `src/pages/`
  Screen-level composition and navigation-aware containers.
  - `app_shell.py`: top-level app shell, shared state, tab switching
  - `competition_page.py`: competition/social screen
  - `profile_page.py`: logged-in user profile screen

- `src/components/`
  Reusable UI pieces.
  Examples:
  - `bottom_nav.py`: bottom navigation bar
  - `circular_metric.py`: reusable circular metric/progress component
  - `main_user_card.py`: main competition card
  - `profile_header.py`: top profile banner/avatar area
  - `metrics_grid.py` and `metric_tile.py`: profile metrics layout
  - `user_avatar.py`, `user_list_item.py`, `users_list.py`: user display/list components
  - `section_title.py`: section heading component
  - `metric_definitions.py`: transforms metric values into UI metric objects

- `src/models/`
  Shared domain/data contracts.
  - `candidates.py`: `UserDetails`, `Metric`, `MetricName`, and backend protocol

- `src/backends/`
  Data providers.
  - `mock_candidates.py`: mock backend used locally

- `src/app_state.py`
  Shared app state and tab enum.

- `src/theme.py`
  Shared colors, shadows, gradients, and theme tokens.

- `dist-web/`, `build/`
  Build outputs. Not the place to implement app logic.

## How Navigation Is Set Up

Navigation is centralized in `src/pages/app_shell.py`.

- `CompetitionApp` is the root app shell.
- It loads data from the backend once during startup.
- It stores shared state in `AppState`.
- The selected page is controlled by `AppTab`.
- It renders the active page based on the selected tab.
- `BottomNav` receives the current tab and a callback to switch tabs.

Important guideline:

- Do not implement global navigation logic inside page components.
- If a new page is added, register it in the app shell and extend the navigation model there.

## Basic Idea Behind Each Page

### `ProfilePage`

Purpose:

- shows the logged-in user's own data
- displays header, profile identity, metrics, and a general score

Data source:

- `state.logged_user`

Main building blocks:

- `ProfileHeader`
- `MetricsGrid`
- `CircularMetric`

### `CompetitionPage`

Purpose:

- shows competition/social-style information
- displays the currently selected candidate and the full candidate list

Data sources:

- `state.selected_candidate`
- `state.users`

Main building blocks:

- `MainUserCard`
- `UsersList`

Behavior:

- sends candidate selection changes back to the shell through a callback

## How the Code Is Separated

Use the following responsibility split when implementing features:

- `pages/`
  Use for screen-level layout and composition.
  Pages should assemble components and consume shared state, but avoid owning global app behavior.

- `components/`
  Use for reusable visual/UI blocks.
  If a piece of UI can appear in more than one page or has a clear isolated responsibility, it should usually live here.

- `models/`
  Use for data contracts and shared domain types.
  This keeps UI and data providers aligned on object shape.

- `backends/`
  Use for data retrieval and mocking.
  UI should depend on backend interfaces rather than embedding data-fetching behavior directly.

- `app_state.py`
  Use for app-wide runtime state.
  If multiple pages need the same state, put it here rather than duplicating local page state.

- `theme.py`
  Use for reusable colors, gradients, shadows, and other design tokens.
  Avoid repeating raw color strings in multiple files when they represent the same concept.

## Code Quality Expectations

Follow the patterns already present in the codebase.

### Type Hints

- Add type hints to public functions, methods, and constructor parameters.
- Prefer concrete types when they are clear and stable.
- Use protocol-based interfaces, like the backend contract, when the UI should depend on behavior rather than implementation.

### Class Structure

- Keep page classes focused on layout/composition.
- Keep component classes focused on one reusable UI responsibility.
- Prefer small classes with clear names over large multi-purpose classes.
- If two components are almost the same, prefer parameterizing one reusable component instead of duplicating it.

### Data Classes and Models

- Use `@dataclass` for plain data containers like state or domain models.
- Keep model objects simple and serializable in spirit.
- Add new shared data shapes in `models/` rather than inventing ad-hoc dictionaries inside UI code.

### State Management

- Shared state should live in `AppState` or in another clearly centralized state object.
- Local state inside components/pages is fine only when it is truly local UI behavior.
- Avoid hidden cross-page dependencies.

### Reuse and Modularity

- Reuse existing components before creating new ones.
- If a new variant is needed, first consider adding parameters to the existing component.
- Only split into a new component when the behavior or structure is meaningfully different.

### Theme and Styling

- Prefer shared constants from `theme.py` for reusable colors and shadows.
- Avoid hardcoding values that are likely to be reused across screens.
- Keep new UI visually aligned with the existing app theme unless a feature explicitly requires a new design direction.

### Page Safety

- Do not break existing pages when adding new ones.
- Keep navigation changes isolated to the app shell and bottom nav.
- When editing shared components, consider how both profile and competition screens use them.

### Backend Separation

- Avoid tying UI components directly to mock-specific assumptions.
- If user or page data needs to become globally available, expose it through shared state or the backend contract in a modular way.

## Recommended Workflow For New Features

1. Identify whether the change belongs in `pages/`, `components/`, `models/`, `backends/`, or shared state.
2. Reuse or extend an existing component if possible.
3. Add shared visual constants to `theme.py` when appropriate.
4. Update `app_shell.py` only if the feature changes navigation or global page composition.
5. Keep new code typed and modular.
6. Validate that existing screens still behave correctly after the change.

## Practical Notes

- The app currently uses `MockCandidatesBackend` for local data.
- Build artifacts in `dist-web/` should not be treated as source of truth.
- The source of truth for app behavior is under `src/`.
